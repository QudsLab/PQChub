# Troubleshooting PQChub

This guide provides solutions to common problems encountered when building, installing, or using PQChub.

## Table of Contents
- [General Issues](#general-issues)
- [Build Problems](#build-problems)
- [Library Loading Issues](#library-loading-issues)
- [Platform-Specific Issues](#platform-specific-issues)
- [Wrapper-Specific Issues](#wrapper-specific-issues)
- [Git LFS Issues](#git-lfs-issues)
- [Contact & Support](#contact--support)

---

## General Issues

### Problem: Missing Dependencies
**Solution:**
- Ensure all prerequisites are installed (see [BUILDING.md](./BUILDING.md)).
- For Python: `pip install -r requirements.txt`
- For Node.js: `npm install`
- For Go: `go mod tidy`
- For Rust: `cargo build`

### Problem: Outdated Submodules or Source
**Solution:**
- Run `python scripts/download_pqclean.py` to update PQClean source.
- Pull latest changes: `git pull --rebase`

---

## Build Problems

### Problem: Compiler Not Found
**Solution:**
- Install build tools for your platform (see [BUILDING.md](./BUILDING.md)).
- On Linux: `sudo apt-get install build-essential`
- On macOS: `xcode-select --install`
- On Windows: Install Visual Studio Build Tools.

### Problem: Permission Denied on Scripts
**Solution:**
- Make scripts executable: `chmod +x scripts/*.sh`
- Run as administrator if needed (Windows).

### Problem: PQClean Source Not Found
**Solution:**
- Run `python scripts/download_pqclean.py` before building.
- Check that `pqclean/` directory exists.

---

## Library Loading Issues

### Problem: Library Not Found at Runtime
**Solution:**
- Ensure `bins/` directory contains binaries for your platform.
- Run `git lfs install` and `git lfs pull` to fetch binaries.
- Check wrapper configuration for correct library path.

### Problem: Architecture Mismatch
**Solution:**
- Build for the correct architecture (e.g., x86_64 vs. arm64).
- Use cross-compilation tools if needed.

### Problem: DLL Load Failure (Windows)
**Solution:**
- Ensure Visual C++ Redistributable is installed.
- Check that `pqc.dll` is in the expected location.
- Run in "Developer Command Prompt for VS".

---

## Platform-Specific Issues

### Linux/macOS
- **Problem:** `libpqc.so` or `libpqc.dylib` not found
  - **Solution:** Build for your platform and check `bins/` directory.
- **Problem:** Segmentation fault
  - **Solution:** Run with `valgrind` to diagnose memory issues.

### Windows
- **Problem:** `pqc.dll` not found
  - **Solution:** Build with `python scripts/build_native.py windows-x64 pqclean`.
- **Problem:** DLL load error
  - **Solution:** Ensure all dependencies are present and correct architecture is used.

### Android
- **Problem:** NDK not found
  - **Solution:** Set `ANDROID_NDK_ROOT` environment variable.
- **Problem:** ABI mismatch
  - **Solution:** Build for correct ABI (e.g., arm64-v8a).

---

## Wrapper-Specific Issues

### Python
- **Problem:** `OSError: cannot load library`
  - **Solution:** Check library path and platform detection logic.
- **Problem:** `ModuleNotFoundError`
  - **Solution:** Run `pip install -e .` in `wrappers/python`.

### Node.js
- **Problem:** `Error: Dynamic library not found`
  - **Solution:** Check `platform.js` for correct path.
- **Problem:** `ffi-napi` or `ref-napi` not installed
  - **Solution:** Run `npm install` in `wrappers/nodejs`.

### Go
- **Problem:** `undefined: C.pqc_*`
  - **Solution:** Ensure CGO is enabled and library is built.
- **Problem:** `go build` fails
  - **Solution:** Check library path and build flags.

### Rust
- **Problem:** `cannot find library`
  - **Solution:** Check `build.rs` and library path.
- **Problem:** `cargo build` fails
  - **Solution:** Ensure correct platform and dependencies.

---

## Git LFS Issues

### Problem: Large Binary Files Not Downloaded
**Solution:**
- Run `git lfs install` and `git lfs pull` after cloning.
- Check `.gitattributes` for correct LFS configuration.

### Problem: Push Fails Due to LFS Quota
**Solution:**
- Check GitHub LFS quota and upgrade if needed.
- Remove unnecessary binaries from history.

---

## Contact & Support

- For unresolved issues, open a [GitHub Issue](https://github.com/QudsLab/PQChub/issues).
- For security concerns, email [security@qudslab.org](mailto:security@qudslab.org).
- For general questions, use [GitHub Discussions](https://github.com/QudsLab/PQChub/discussions).

---

For more details, see [BUILDING.md](./BUILDING.md), [CONTRIBUTING.md](./CONTRIBUTING.md), and [API.md](./API.md).