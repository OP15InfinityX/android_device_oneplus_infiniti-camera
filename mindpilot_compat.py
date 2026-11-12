# SPDX-License-Identifier: Apache-2.0
"""Keep Mind Pilot's COUI renderer probe out of its full primary DEX."""

from pathlib import Path
import re


def blob_fixup_mindpilot_dex_layout(ctx, file, file_path, *args, tmp_dir=None, **kwargs):
    if tmp_dir is None:
        raise ValueError('Mind Pilot DEX fixup requires decoded APK sources')
    root = Path(tmp_dir)
    relative = Path('com/coui/appcompat/COUIEffectVersionUtil.smali')
    source = root / 'smali' / relative
    if not source.is_file():
        raise ValueError('Mind Pilot primary COUI utility changed; review the DEX layout')
    data = source.read_text()
    if not all(name in data for name in (
            'ixHasMaterialRendererCache', 'ixHasCausticRendererCache')):
        raise ValueError('Apply the COUI renderer capability guard before DEX relocation')
    # The stock primary DEX has no room for the reflection method references.
    # Move only this utility to a new DEX; preserve its class name and callers.
    numbers = [1]
    for directory in root.glob('smali_classes*'):
        match = re.fullmatch(r'smali_classes(\d+)', directory.name)
        if match:
            numbers.append(int(match.group(1)))
    target = root / f'smali_classes{max(numbers) + 1}' / relative
    if target.exists():
        raise ValueError('Mind Pilot COUI destination already exists')
    target.parent.mkdir(parents=True)
    source.rename(target)
