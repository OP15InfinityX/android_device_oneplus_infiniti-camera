# SPDX-License-Identifier: Apache-2.0
"""Keep STDSP's OEM freeze-delay integration conditional on its actual API."""

from pathlib import Path
import re


def blob_fixup_stdsp_frozen_capabilities(ctx, file, file_path, *args, tmp_dir=None, **kwargs):
    if tmp_dir is None:
        raise ValueError('STDSP fixup requires decoded APK sources')
    root = Path(tmp_dir)
    specs = (
        ('com/nearme/common/frozen/FrozenHelper.smali', 'private static', 2),
        ('com/oplus/stdsp/platform/frozen/FrozenManager.smali', 'public final', 4),
    )
    prepared = []
    helper_cls = 'Lcom/nearme/common/frozen/FrozenHelper;'
    for suffix, flags, locals_count in specs:
        paths = list(root.glob('smali*/' + suffix))
        if len(paths) != 1:
            raise ValueError(f'STDSP: expected one {suffix}, found {len(paths)}')
        path = paths[0]
        data = path.read_text()
        if 'ixHasFrozenApi' in data:
            raise ValueError(f'{path}: capability guard already applied')
        pattern = rf'(?m)^(\.method {flags} isSupported\(\)Z\n    \.locals {locals_count}\n)'
        gate = f"""
    invoke-static {{}}, {helper_cls}->ixHasFrozenApi()Z
    move-result v0
    if-nez v0, :ix_frozen_api_present
    const/4 v0, 0x0
    return v0
    :ix_frozen_api_present
"""
        data, count = re.subn(pattern, lambda m: m[1] + gate, data)
        if count != 1:
            raise ValueError(f'{path}: unexpected original isSupported method')
        if suffix.endswith('FrozenHelper.smali'):
            data += """
# Version checks alone also match AOSP, which has no ColorOS freeze-delay service.
.method public static ixHasFrozenApi()Z
    .locals 1
    :ix_try_start
    const-string v0, "com.oplus.osense.OsenseResEventClient"
    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;
    const-string v0, "com.oplus.osense.task.FreezeDelayCallback"
    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;
    const-string v0, "com.oplus.osense.task.BgRunningCallback"
    invoke-static {v0}, Ljava/lang/Class;->forName(Ljava/lang/String;)Ljava/lang/Class;
    :ix_try_end
    .catch Ljava/lang/ReflectiveOperationException; {:ix_try_start .. :ix_try_end} :ix_missing
    .catch Ljava/lang/LinkageError; {:ix_try_start .. :ix_try_end} :ix_missing
    .catch Ljava/lang/SecurityException; {:ix_try_start .. :ix_try_end} :ix_missing
    const/4 v0, 0x1
    return v0
    :ix_missing
    move-exception v0
    const/4 v0, 0x0
    return v0
.end method
"""
        prepared.append((path, data))
    for path, data in prepared:
        path.write_text(data)
