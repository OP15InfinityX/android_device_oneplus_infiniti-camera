# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
import re


def blob_fixup_gallery_backlight_capability(ctx, file, file_path, *args, tmp_dir=None, **kwargs):
    """Probe the OEM Display extension once, retaining Gallery's own fallback.

    AOSP does not expose Display.getBacklightType. Do not repeatedly throw a
    reflection exception for every HDR/SDR update, or invent a display API.
    """
    candidates = []
    for path in Path(tmp_dir).glob('smali*/com/oplus/aiunit/vision/*.smali'):
        data = path.read_text()
        if '.source "HdrSdrManagerOs14.kt"' in data and '"getBacklightType"' in data:
            candidates.append((path, data))
    if len(candidates) != 1:
        raise ValueError(f'Expected one Gallery backlight implementation, got {len(candidates)}')
    path, data = candidates[0]
    if 'ixBacklightApiAvailable' in data:
        return
    cls = re.search(r'^\.class .* (L[^;]+;)$', data, re.M)[1]
    # v0 is the existing boxed EDR_TYPE_NORMAL fallback; preserve it exactly.
    anchor = ('    invoke-static {v0}, Ljava/lang/Integer;->valueOf(I)Ljava/lang/Integer;\n'
              '\n    move-result-object v0\n')
    if data.count(anchor) != 1:
        raise ValueError('Gallery backlight default changed')
    data = data.replace(anchor, anchor + f'''
    invoke-static {{}}, {cls}->ixHasBacklightApi()Z
    move-result v2
    if-nez v2, :ix_backlight_supported
    return-object v0
    :ix_backlight_supported
''', 1)
    data = data.replace('# instance fields\n',
                        '.field private static volatile ixBacklightApiAvailable:Ljava/lang/Boolean;\n\n# instance fields\n', 1)
    data += f'''
.method private static ixHasBacklightApi()Z
    .locals 3
    sget-object v0, {cls}->ixBacklightApiAvailable:Ljava/lang/Boolean;
    if-eqz v0, :ix_probe_backlight
    invoke-virtual {{v0}}, Ljava/lang/Boolean;->booleanValue()Z
    move-result v0
    return v0
    :ix_probe_backlight
    :ix_probe_start
    const-class v0, Landroid/view/Display;
    const-string v1, "getBacklightType"
    const/4 v2, 0x0
    new-array v2, v2, [Ljava/lang/Class;
    invoke-virtual {{v0, v1, v2}}, Ljava/lang/Class;->getMethod(Ljava/lang/String;[Ljava/lang/Class;)Ljava/lang/reflect/Method;
    :ix_probe_end
    .catch Ljava/lang/NoSuchMethodException; {{:ix_probe_start .. :ix_probe_end}} :ix_no_backlight
    .catch Ljava/lang/SecurityException; {{:ix_probe_start .. :ix_probe_end}} :ix_no_backlight
    const/4 v0, 0x1
    goto :ix_store_backlight
    :ix_no_backlight
    move-exception v0
    const/4 v0, 0x0
    :ix_store_backlight
    invoke-static {{v0}}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;
    move-result-object v1
    sput-object v1, {cls}->ixBacklightApiAvailable:Ljava/lang/Boolean;
    return v0
.end method
'''
    path.write_text(data)


def blob_fixup_camera_result_capabilities(ctx, file, file_path, *args, tmp_dir=None, **kwargs):
    """Skip face synthesis when this result has a mode but lacks required arrays.

    Keep standard no-face/null behavior. Never cache missing arrays across
    results; partial metadata and later frames can contain different fields.
    """
    path = next(Path(tmp_dir).glob(
        'smali*/com/oplus/ocs/camera/metadata/captureresult/OplusCaptureResultImpl.smali'))
    data = path.read_text()
    if 'ixReadResult' in data:
        return
    cls = 'Lcom/oplus/ocs/camera/metadata/captureresult/OplusCaptureResultImpl;'
    anchor = ('    iget-object p0, p0, ' + cls + '->mCaptureResult:Landroid/hardware/camera2/CaptureResult;\n'
              '\n    invoke-virtual {p0, p1}, Landroid/hardware/camera2/CaptureResult;->get(Landroid/hardware/camera2/CaptureResult$Key;)Ljava/lang/Object;')
    if data.count(anchor) != 1:
        raise ValueError('Camera result getter changed')
    data = data.replace(anchor,
        f'    invoke-direct {{p0, p1}}, {cls}->ixReadResult(Landroid/hardware/camera2/CaptureResult$Key;)Ljava/lang/Object;', 1)
    data += f'''
.method private ixReadResult(Landroid/hardware/camera2/CaptureResult$Key;)Ljava/lang/Object;
    .locals 3
    iget-object v0, p0, {cls}->mCaptureResult:Landroid/hardware/camera2/CaptureResult;
    if-eqz v0, :ix_result_absent
    sget-object v1, Landroid/hardware/camera2/CaptureResult;->STATISTICS_FACES:Landroid/hardware/camera2/CaptureResult$Key;
    invoke-virtual {{v1, p1}}, Landroid/hardware/camera2/CaptureResult$Key;->equals(Ljava/lang/Object;)Z
    move-result v1
    if-eqz v1, :ix_read_value
    sget-object v1, Landroid/hardware/camera2/CaptureResult;->STATISTICS_FACE_DETECT_MODE:Landroid/hardware/camera2/CaptureResult$Key;
    invoke-virtual {{v0, v1}}, Landroid/hardware/camera2/CaptureResult;->get(Landroid/hardware/camera2/CaptureResult$Key;)Ljava/lang/Object;
    move-result-object v1
    if-eqz v1, :ix_read_value
    sget-object v1, Landroid/hardware/camera2/CaptureResult;->STATISTICS_FACE_SCORES:Landroid/hardware/camera2/CaptureResult$Key;
    invoke-virtual {{v0, v1}}, Landroid/hardware/camera2/CaptureResult;->get(Landroid/hardware/camera2/CaptureResult$Key;)Ljava/lang/Object;
    move-result-object v1
    if-eqz v1, :ix_faces_absent
    sget-object v1, Landroid/hardware/camera2/CaptureResult;->STATISTICS_FACE_RECTANGLES:Landroid/hardware/camera2/CaptureResult$Key;
    invoke-virtual {{v0, v1}}, Landroid/hardware/camera2/CaptureResult;->get(Landroid/hardware/camera2/CaptureResult$Key;)Ljava/lang/Object;
    move-result-object v1
    if-eqz v1, :ix_faces_absent
    :ix_read_value
    invoke-virtual {{v0, p1}}, Landroid/hardware/camera2/CaptureResult;->get(Landroid/hardware/camera2/CaptureResult$Key;)Ljava/lang/Object;
    move-result-object v0
    return-object v0
    :ix_faces_absent
    const/4 v1, 0x0
    new-array v1, v1, [Landroid/hardware/camera2/params/Face;
    return-object v1
    :ix_result_absent
    const/4 v1, 0x0
    return-object v1
.end method
'''
    path.write_text(data)
