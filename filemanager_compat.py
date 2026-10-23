# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
from copy import deepcopy
import re
import shutil
import xml.etree.ElementTree as ET


def blob_fixup_filemanager_atlas_debug_log(ctx, file, file_path, *args, tmp_dir=None, **kwargs):
    """Supply the stock logging helper used by FileBag's configuration callback.

    Preserve the OEM debug-property gate, messages, return values and exception
    handling. This only supplies a missing dependency, not a service fallback.
    """
    if tmp_dir is None:
        raise ValueError('FileManager compatibility fix requires decoded sources')
    root = Path(tmp_dir)
    if list(root.glob('smali*/com/oplus/atlas/DebugLog.smali')):
        return
    callers = list(root.glob('smali*/com/filemanager/filebag/PriorityService*.smali'))
    if not callers or not any('Lcom/oplus/atlas/DebugLog;' in p.read_text() for p in callers):
        raise ValueError('FileManager PriorityService logging dependency changed')
    source = Path(__file__).resolve().parent / 'compat-smali/com/oplus/atlas/DebugLog.smali'
    target = root / 'smali/com/oplus/atlas/DebugLog.smali'
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def blob_fixup_filemanager_text_metrics(ctx, file, file_path, *args, tmp_dir=None, **kwargs):
    """Match metrics enforced for apps targeting API 36 or later.

    COUI repeatedly requests compact text metrics from styles. Android ignores
    that request and warns on every TextView inflation. Request the already
    enforced value in versioned styles instead. Keep the complete original
    style bags and all resources used on older Android versions unchanged.
    """
    if tmp_dir is None:
        raise ValueError('FileManager text metrics fix requires decoded resources')
    root = Path(tmp_dir)
    android = '{http://schemas.android.com/apk/res/android}'
    manifest = ET.parse(root / 'AndroidManifest.xml').getroot()
    sdk = manifest.find('uses-sdk')
    if sdk is not None:
        target_sdk = int(sdk.get(android + 'targetSdkVersion', '0'))
    else:
        # Apktool moves uses-sdk into this metadata during a full decode.
        match = re.search(r'(?m)^  targetSdkVersion: (\d+)$',
                          (root / 'apktool.yml').read_text())
        target_sdk = int(match[1]) if match else 0
    if target_sdk not in (36, 37):
        raise ValueError('Review FileManager text metrics for the changed target SDK')

    expected = {'values': 9, 'values-ldrtl': 1, 'values-my-rMM': 1}
    for qualifier, count in expected.items():
        styles = ET.parse(root / 'res' / qualifier / 'styles.xml').getroot()
        overrides = ET.Element('resources')
        for style in styles.findall('style'):
            items = [item for item in style.findall('item')
                     if item.get('name') == 'android:elegantTextHeight']
            if not items:
                continue
            if len(items) != 1 or items[0].text not in (
                    'false', '@bool/coui_support_elegant_text_height'):
                raise ValueError('FileManager COUI text metrics style changed')
            override = deepcopy(style)
            for item in override.findall('item'):
                if item.get('name') == 'android:elegantTextHeight':
                    item.text = 'true'
            overrides.append(override)
        if len(overrides) != count:
            raise ValueError(f'FileManager text metrics styles changed in {qualifier}')
        target = root / 'res' / (qualifier + '-v36') / 'filemanager_text_metrics.xml'
        target.parent.mkdir(parents=True, exist_ok=True)
        ET.indent(overrides, space='    ')
        ET.ElementTree(overrides).write(target, encoding='utf-8', xml_declaration=True)
