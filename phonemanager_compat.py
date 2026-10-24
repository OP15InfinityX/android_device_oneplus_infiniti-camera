# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
import re
import shutil


def blob_fixup_phonemanager_oplus_log(ctx, file, file_path, *args, tmp_dir=None, **kwargs):
    """Supply the OEM logger used by the first-run consent dialog.

    Keep the dialog and the logging calls intact. The stock helper only uses
    Android/Java APIs and preserves the original messages, gates and overloads.
    """
    if tmp_dir is None:
        raise ValueError('PhoneManager logging fix requires decoded sources')
    root = Path(tmp_dir)
    callers = list(root.glob(
        'smali*/com/oplus/phonemanager/common/helper/COUIUserStatementDialogV2.smali'))
    if len(callers) != 1:
        raise ValueError('PhoneManager consent dialog class changed')
    required = set(re.findall(
        r'Lcom/oplus/util/OplusLog;->([^\s,]+)', callers[0].read_text()))
    if not required:
        raise ValueError('PhoneManager consent dialog logging dependency changed')

    existing = list(root.glob('smali*/com/oplus/util/OplusLog.smali'))
    if len(existing) > 1:
        raise ValueError('Duplicate PhoneManager OplusLog classes')
    source = (existing[0] if existing else Path(__file__).resolve().parent /
              'compat-smali/com/oplus/util/OplusLog.smali')
    provided = set(re.findall(
        r'(?m)^\.method public static[^\n]* ([^\s]+)\s*$', source.read_text()))
    if not required.issubset(provided):
        raise ValueError('PhoneManager consent dialog OplusLog API changed')
    if existing:
        return

    # Several stock dex files are within a few method IDs of the 65535 limit.
    # Keep this self-contained helper in its own dex instead of overflowing one.
    dex_numbers = [1]
    for folder in root.glob('smali_classes*'):
        match = re.fullmatch(r'smali_classes(\d+)', folder.name)
        if folder.is_dir() and match:
            dex_numbers.append(int(match[1]))
    target = root / f'smali_classes{max(dex_numbers) + 1}/com/oplus/util/OplusLog.smali'
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
