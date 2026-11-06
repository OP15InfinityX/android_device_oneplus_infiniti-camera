# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
import re


def blob_fixup_camera_heif_completion(ctx, file, file_path, *args, tmp_dir=None, **kwargs):
    """Deliver COS17's completed HEIF/YUV callback without treating it as raw YUV.

    APS encodes the image into .RENAME_TMP, then reports message 3, format 35
    and heif_encode_in_aps=true without a pixel buffer. The SDK's format switch
    drops format 35, leaving the quick JPEG under the final .heic name. Forward
    this completion to its existing HEIC handler so Camera promotes the file.
    """
    candidates = list(Path(tmp_dir).glob(
        'smali*/com/oplus/ocs/camera/consumer/apsAdapter/adapter/ApsAdapterImpl.smali'))
    if len(candidates) != 1:
        raise ValueError(f'Expected one APS adapter, found {len(candidates)}')
    path = candidates[0]
    data = path.read_text()
    pattern = (r'(?ms)^\.method public onCaptureReceived\('
               r'Lcom/oplus/ocs/camera/consumer/apsAdapter/adapter/ApsResult;\)V\n'
               r'.*?^\.end method')
    matches = list(re.finditer(pattern, data))
    if len(matches) != 1:
        raise ValueError('APS capture dispatch signature changed')
    match = matches[0]
    body = match.group()
    if ':ix_heif_original_format_dispatch' in body:
        return
    result = 'Lcom/oplus/ocs/camera/consumer/apsAdapter/adapter/ApsResult;'
    adapter = 'Lcom/oplus/ocs/camera/consumer/apsAdapter/adapter/ApsAdapterImpl;'
    capture = 'Lcom/oplus/ocs/camera/consumer/apsAdapter/adapter/ApsCaptureAdapterImpl;'
    anchor = f'    iget v0, p1, {result}->mBufferType:I\n'
    if (body.count(anchor) != 1 or '->onHeicReceived(' not in body
            or re.search(r'const(?:/16)?\s+v\d+, 0x23\b', body)):
        raise ValueError('APS format dispatch changed; review its HEIF handling')
    insertion = f'''
    const/16 v1, 0x23
    if-ne v0, v1, :ix_heif_original_format_dispatch
    iget-boolean v1, p1, {result}->mbHeifProcessInAps:Z
    if-eqz v1, :ix_heif_unhandled_yuv
    iget v0, p1, {result}->mMessageType:I
    const/4 v1, 0x3
    if-ne v0, v1, :ix_heif_unhandled_yuv
    iget-object v0, p0, {adapter}->mCaptureImpl:{capture}
    invoke-virtual {{v0, p1}}, {capture}->onHeicReceived({result})V
    :ix_heif_unhandled_yuv
    return-void
    :ix_heif_original_format_dispatch
'''
    fixed = body.replace(anchor, anchor + insertion, 1)
    path.write_text(data[:match.start()] + fixed + data[match.end():])
