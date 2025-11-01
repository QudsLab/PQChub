# PQChub Build Scripts

This directory contains scripts for downloading PQClean source code and building native libraries for all supported platforms.

## Scripts Overview

### Download Scripts

- **`download_pqclean.py`** - Python script to download PQClean source
- **`download_pqclean.sh`** - Bash script to download PQClean source (Unix/Linux/macOS)

### Build Scripts

- **`build_native.sh`** - Unix/Linux/macOS native library build script
- **`build_native.py`** - Windows native library build script
- **`build_android.sh`** - Android NDK build script for all ABIs

## Usage

### 1. Download PQClean Source

```bash
# Using Python script (cross-platform)
python download_pqclean.py --ref master --output pqclean

# Using Bash script (Unix/Linux/macOS)
./download_pqclean.sh master pqclean
```

### 2. Build Native Libraries

#### Linux/macOS

```bash
# Build for current platform
./build_native.sh linux-x86_64 pqclean
./build_native.sh macos-arm64 pqclean

# Cross-compile for other architectures
CC=aarch64-linux-gnu-gcc ./build_native.sh linux-aarch64 pqclean
```

#### Windows

```bash
# Requires Visual Studio Build Tools
python build_native.py windows-x64 pqclean
python build_native.py windows-x86 pqclean
```

#### Android

```bash
# Requires Android NDK
export ANDROID_NDK_ROOT=/path/to/android-ndk
./build_android.sh arm64-v8a pqclean
./build_android.sh armeabi-v7a pqclean
./build_android.sh x86_64 pqclean
./build_android.sh x86 pqclean
```

## Supported Platforms

| Platform | Target | Compiler | Output |
|----------|--------|----------|--------|
| Linux x86_64 | `linux-x86_64` | gcc/clang | `libpqc.so` |
| Linux ARM64 | `linux-aarch64` | aarch64-linux-gnu-gcc | `libpqc.so` |
| macOS Intel | `macos-x86_64` | clang | `libpqc.dylib` |
| macOS Apple Silicon | `macos-arm64` | clang | `libpqc.dylib` |
| Windows x64 | `windows-x64` | MSVC cl.exe | `pqc.dll` |
| Windows x86 | `windows-x86` | MSVC cl.exe | `pqc.dll` |
| Android ARM64 | `android-arm64-v8a` | NDK clang | `libpqc.so` |
| Android ARMv7 | `android-armeabi-v7a` | NDK clang | `libpqc.so` |
| Android x86_64 | `android-x86_64` | NDK clang | `libpqc.so` |
| Android x86 | `android-x86` | NDK clang | `libpqc.so` |

## Supported Algorithms

All scripts build the following algorithms from PQClean:

### Key Encapsulation Mechanisms (KEM)
- Kyber512
- Kyber768
- Kyber1024

### Digital Signatures
- Dilithium2
- Dilithium3
- Dilithium5
- Falcon-512
- Falcon-1024

## Prerequisites

### All Platforms
- Python 3.8+ (for Python scripts)
- Git (for downloading)
- Build tools for target platform

### Linux/macOS
- GCC or Clang
- Make
- CMake (optional)
- Cross-compilation toolchain (for ARM builds)

### Windows
- Visual Studio 2019+ or Build Tools for Visual Studio
- Windows 10 SDK

### Android
- Android NDK r21+
- CMake 3.18+

## Environment Variables

### Linux Cross-Compilation
```bash
export CC=aarch64-linux-gnu-gcc
export CXX=aarch64-linux-gnu-g++
```

### Android NDK
```bash
export ANDROID_NDK_ROOT=/path/to/android-ndk
export ANDROID_NDK_HOME=/path/to/android-ndk  # Legacy
```

### Windows MSVC
The build script will automatically detect and use MSVC if available.

## Build Output

All scripts generate:

1. **Native library file** - The compiled PQC library
2. **README.txt** - Build information and metadata
3. **Build logs** - Compilation output and status

Output structure:
```
bins/
├── linux-x86_64/
│   ├── libpqc.so
│   └── README.txt
├── windows-x64/
│   ├── pqc.dll
│   └── README.txt
└── android-arm64-v8a/
    ├── libpqc.so
    └── README.txt
```

## Troubleshooting

### Common Issues

1. **Download fails**: Check internet connection and GitHub access
2. **Build fails**: Verify compiler installation and PATH
3. **Missing algorithms**: Some PQClean versions may not include all algorithms
4. **Cross-compilation**: Ensure toolchain is properly installed

### Debug Information

Enable verbose output:
```bash
# Bash scripts
set -x
./build_native.sh target pqclean

# Python scripts
python -v build_native.py target pqclean
```

### Platform-Specific Notes

#### macOS
- Xcode Command Line Tools required
- Universal binaries not yet supported

#### Windows
- Use Developer Command Prompt or PowerShell with MSVC environment
- Windows Defender may flag build output

#### Android
- NDK r23+ recommended for best compatibility
- Some algorithms may have performance differences across ABIs

## CI/CD Integration

These scripts are used by GitHub Actions workflows:

- **`.github/workflows/build-bins.yml`** - Main build workflow
- **`.github/workflows/test-wrappers.yml`** - Wrapper testing

## Contributing

When modifying build scripts:

1. Test on all supported platforms
2. Maintain compatibility with GitHub Actions runners
3. Update documentation for new features
4. Follow shell scripting best practices

## Security Considerations

- Scripts download from official PQClean repository
- No external dependencies beyond build tools
- Build outputs should be verified before use
- Consider using signed/verified PQClean releases

## License

These build scripts are part of PQChub and licensed under MIT License.