# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
import shutil


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
