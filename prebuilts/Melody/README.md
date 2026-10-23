# Melody 17.6.6 source snapshot

Complete Google Play release of `com.oplus.melody`, including native ARM64,
xxhdpi resources and all supplied language splits. See SOURCE.json for exact
hashes and provenance. Every original APK signature was verified before merging;
the base is byte-identical to the APK captured directly from Google Play.

The merged input is unpatched and is not claimed to retain a valid OEM APK
signature. Extraction substitutes this pinned input for COS17 17.0.0.102's
17.5.0 APK, applies the existing framework/permission and whitelist compatibility
fixups, and leaves platform signing to the normal ROM build. An unexpected OTA
input fails explicitly so a future stock update cannot be silently downgraded.

The ROM signing strategy and Android signature checks are unchanged. Consequently
stock Google Play updates still cannot replace the patched ROM APK. A newer
release requires the same review and porting procedure. No app data reset is part
of the update.
