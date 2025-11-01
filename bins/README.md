# Directory for pre-compiled PQChub binaries

This directory contains platform-specific pre-compiled native libraries for PQChub. Binaries are built automatically via GitHub Actions and distributed via Git LFS.

## Structure

- `bins/<platform>/` — Contains binaries for each supported platform and architecture.
- Example platforms:
  - `linux-x86_64/`
  - `linux-aarch64/`
  - `macos-x86_64/`
  - `macos-arm64/`
  - `windows-x64/`
  - `windows-x86/`
  - `android-arm64-v8a/`
  - `android-armeabi-v7a/`
  - `android-x86_64/`
  - `android-x86/`

## Example Contents

- `libpqc.so` (Linux, Android)
- `libpqc.dylib` (macOS)
- `pqc.dll` (Windows)
- `metadata.json` (build info, version, hash)

## Notes
- Binaries are managed via Git LFS. Run `git lfs install` and `git lfs pull` after cloning.
- See [BUILDING.md](../docs/BUILDING.md) for instructions to build locally.
- See [API.md](../docs/API.md) for usage details.
