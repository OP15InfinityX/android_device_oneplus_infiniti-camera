// SPDX-License-Identifier: Apache-2.0

#include <jni.h>
#include <stddef.h>
#include <stdint.h>

// C entry points exported by the OP15 COS17 encoder and buffer-exchange helpers.
extern "C" void heifProcess(int32_t, int32_t, int32_t, int32_t, int32_t, int32_t,
                           void*, void*, int32_t, void*, int32_t, int32_t, void*);
extern "C" int32_t setBufferQAllocEnable(void*, bool, void*);
extern "C" int32_t exchangeHardwareBufferBetweenBufferQ(void*, void*, int32_t, int32_t, void*);
extern "C" int32_t attachHardwareBufferToBufferQ(void*, void*, void*);

namespace {
// Packet ABI verified against COS17 libHeifWinBufExchg-jni.so
// SHA-256: 633f94c7f4099ca43a717baba0353936ebab00c647f55bbf5bf0d93cfb5908db.
// The original JNI reads exactly these offsets.
struct HeifPacket {
    int32_t width, height, stride, scanline;
    int32_t format, rotation;
    void* image;
    void* exif;
    int32_t exifSize;
    uint32_t padding;
    void* debugData;
    int32_t debugSize, fd;
};
static_assert(sizeof(void*) == 8);
static_assert(sizeof(HeifPacket) == 0x40);
static_assert(offsetof(HeifPacket, format) == 0x10);
static_assert(offsetof(HeifPacket, image) == 0x18);
static_assert(offsetof(HeifPacket, exifSize) == 0x28);
static_assert(offsetof(HeifPacket, debugData) == 0x30);
static_assert(offsetof(HeifPacket, fd) == 0x3c);

template <typename T>
T readAt(jlong packet, uintptr_t offset) {
    return *reinterpret_cast<const T*>(static_cast<uintptr_t>(packet) + offset);
}

void* tailAt(jlong packet, uintptr_t offset) {
    return reinterpret_cast<void*>(static_cast<uintptr_t>(packet) + offset);
}
}  // namespace

extern "C" JNIEXPORT void JNICALL
Java_android_hardware_camera2_OplusCameraManager_nativtSendToProcessHeif(
        JNIEnv*, jobject, jlong packet) {
    const auto& p = *reinterpret_cast<const HeifPacket*>(static_cast<uintptr_t>(packet));
    // The APS handoff carries NV21 chroma, but labels it as NV12 (3).
    // Correct only this camera handoff. P010 (1) and other formats retain their
    // original value; the generic OnePlus HEIF writer is left unchanged.
    const int32_t format = p.format == 3 ? 4 : p.format;
    heifProcess(p.width, p.height, p.stride, p.scanline, format, p.rotation,
                p.image, p.exif, p.exifSize, p.debugData, p.debugSize, p.fd,
                tailAt(packet, sizeof(HeifPacket)));
}

extern "C" JNIEXPORT jint JNICALL
Java_android_hardware_camera2_OplusCameraManager_nativeSendToBufQAllocEnableEvent(
        JNIEnv*, jobject, jlong packet) {
    return setBufferQAllocEnable(readAt<void*>(packet, 0),
                                readAt<uint8_t>(packet, 8), tailAt(packet, 0x10));
}

extern "C" JNIEXPORT jint JNICALL
Java_android_hardware_camera2_OplusCameraManager_nativeSendToExchgHWBufBtwBufQEvent(
        JNIEnv*, jobject, jlong packet) {
    return exchangeHardwareBufferBetweenBufferQ(
            readAt<void*>(packet, 0), readAt<void*>(packet, 8),
            readAt<int32_t>(packet, 0x10), readAt<int32_t>(packet, 0x14),
            tailAt(packet, 0x18));
}

extern "C" JNIEXPORT jint JNICALL
Java_android_hardware_camera2_OplusCameraManager_nativeSendToAttachHWBufToBufQEvent(
        JNIEnv*, jobject, jlong packet) {
    return attachHardwareBufferToBufferQ(readAt<void*>(packet, 0),
                                        readAt<void*>(packet, 8), tailAt(packet, 0x10));
}
