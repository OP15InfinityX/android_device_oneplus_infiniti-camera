# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
import re
import zipfile

from extract_utils.tools import apktool_path, java_path
from extract_utils.utils import run_cmd


def blob_fixup_appfeature_provider(ctx, file, file_path, *args, tmp_dir=None, **kwargs):
    """Package ONLY the original AppFeature provider and its helpers from COS17.

    Never expose stock com.android.server classes on Infinity-X's boot classpath.
    The provider keeps its original SQLite/query contract and uses the existing
    port's AppFeature configuration through OplusCfgFilePolicy.
    """
    if tmp_dir is None:
        raise ValueError('AppFeature extraction requires a temporary directory')
    root = Path(ctx.module_dir).resolve().parents[2]
    work = Path(tmp_dir)
    decoded = work / 'stock-services'
    selected = work / 'provider-smali'
    run_cmd([java_path, '-jar', apktool_path, 'd', file_path,
             '-o', str(decoded), '--no-res', '-f'])
    classes = []
    for package in decoded.glob('smali*/com/oplus/customize/appfeature'):
        for source in package.rglob('*.smali'):
            dest = selected / 'com/oplus/customize/appfeature' / source.relative_to(package)
            dest.parent.mkdir(parents=True, exist_ok=True)
            # Hidden-API DEX flags apply to boot jars, not this application DEX.
            data = source.read_text()
            data = re.sub(r'(?m)^(\.(?:field|method) .*?)\b(?:whitelist|blacklist|greylist|test-api) ', r'\1', data)
            data = re.sub(r'(?m)^(\.(?:field|method) .*?)\b(?:whitelist|blacklist|greylist|test-api) ', r'\1', data)
            dest.write_text(data)
            classes.append(dest)
    if len(classes) != 29:
        raise ValueError(f'Unexpected COS17 AppFeature class set: {len(classes)}')
    smali = root / 'prebuilts/extract-tools/common/smali/smali.jar'
    dex = work / 'classes.dex'
    run_cmd([java_path, '-jar', str(smali), 'assemble', '--api', '37', str(selected), '-o', str(dex)])
    if not dex.is_file():
        raise ValueError('AppFeature provider DEX assembly failed')
    manifest = Path(ctx.module_dir) / 'configs/appfeature/AndroidManifest.xml'
    apk = work / 'provider.apk'
    run_cmd([str(root / 'prebuilts/sdk/tools/linux/bin/aapt2'), 'link',
             '-I', str(root / 'prebuilts/sdk/37.0/public/android.jar'),
             '--manifest', str(manifest), '-o', str(apk)])
    # AAPT2 adds ZIP alignment extra fields unknown to the extraction stripzip.
    # Normalize those container fields; the build signs/aligns the final APK.
    with zipfile.ZipFile(apk) as source, zipfile.ZipFile(file_path, 'w') as archive:
        for member in source.infolist():
            info = zipfile.ZipInfo(member.filename, (2009, 1, 1, 0, 0, 0))
            archive.writestr(info, source.read(member))
        info = zipfile.ZipInfo('classes.dex', (2009, 1, 1, 0, 0, 0))
        archive.writestr(info, dex.read_bytes())
