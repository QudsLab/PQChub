# Building PQChub

This guide explains how to build PQChub binaries locally and set up a development environment.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Build Scripts](#build-scripts)
- [Development Setup](#development-setup)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### All Platforms

- **Git** with LFS support
- **Python** 3.8+ (for build scripts)
- **Internet connection** (to download PQClean)

### Linux/macOS

- **GCC** or **Clang** compiler
- **Make** build system
- **CMake** 3.15+ (optional, for advanced builds)

#### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install build-essential cmake git git-lfs python3
```

#### macOS

```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install cmake git git-lfs python3
```

### Windows

- **Visual Studio 2019+** or **Build Tools for Visual Studio**
- **Windows SDK** 10.0.19041.0+
- **Git for Windows** with LFS
- **Python** 3.8+

#### Installation

1. Install [Visual Studio Community](https://visualstudio.microsoft.com/vs/community/)
   - Select "C++ build tools" workload
   - Include Windows 10/11 SDK

2. Install [Git for Windows](https://git-scm.com/download/win)
   - Enable Git LFS during installation

3. Install [Python](https://www.python.org/downloads/windows/)

### Android (Optional)

- **Android NDK** r21+ 
- **CMake** 3.18+

```bash
# Download Android NDK
wget https://dl.google.com/android/repository/android-ndk-r25c-linux.zip
unzip android-ndk-r25c-linux.zip
export ANDROID_NDK_ROOT=$PWD/android-ndk-r25c
```

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/QudsLab/PQChub.git
cd PQChub

# Ensure LFS files are downloaded
git lfs pull
```

### 2. Download PQClean Source

```bash
# Using Python script (cross-platform)
python scripts/download_pqclean.py

# Or using Bash script (Linux/macOS)
chmod +x scripts/download_pqclean.sh
./scripts/download_pqclean.sh
```

### 3. Build for Your Platform

#### Linux/macOS

```bash
# Detect your platform automatically
chmod +x scripts/build_native.sh
./scripts/build_native.sh $(uname -s | tr '[:upper:]' '[:lower:]')-$(uname -m) pqclean
```

#### Windows

```powershell
# Open Developer Command Prompt for VS 2019/2022
python scripts/build_native.py windows-x64 pqclean
```

### 4. Test the Build

#### Python

```bash
cd wrappers/python
pip install -e .
python -c "
from pqchub import Kyber512
k = Kyber512()
pk, sk = k.keypair()
print('✅ Build successful!')
"
```

#### Node.js

```bash
cd wrappers/nodejs
npm install
node -e "
const { Kyber512 } = require('./index.js');
const k = new Kyber512();
const keys = k.keypair();
console.log('✅ Build successful!');
"
```

## Platform-Specific Instructions

### Linux

#### x86_64 (Native)

```bash
./scripts/build_native.sh linux-x86_64 pqclean
```

#### ARM64/AArch64 (Cross-compile)

```bash
# Install cross-compilation toolchain
sudo apt-get install gcc-aarch64-linux-gnu g++-aarch64-linux-gnu

# Build with cross-compiler
CC=aarch64-linux-gnu-gcc CXX=aarch64-linux-gnu-g++ \
./scripts/build_native.sh linux-aarch64 pqclean
```

#### Output

- Location: `bins/linux-x86_64/libpqc.so` or `bins/linux-aarch64/libpqc.so`
- Type: Shared library (.so)

### macOS

#### Intel x86_64

```bash
./scripts/build_native.sh macos-x86_64 pqclean
```

#### Apple Silicon (ARM64)

```bash
./scripts/build_native.sh macos-arm64 pqclean
```

#### Universal Binary (Both architectures)

```bash
# Build both architectures
./scripts/build_native.sh macos-x86_64 pqclean
./scripts/build_native.sh macos-arm64 pqclean

# Create universal binary
lipo -create \
  bins/macos-x86_64/libpqc.dylib \
  bins/macos-arm64/libpqc.dylib \
  -output bins/macos-universal/libpqc.dylib
```

#### Output

- Location: `bins/macos-x86_64/libpqc.dylib` or `bins/macos-arm64/libpqc.dylib`
- Type: Dynamic library (.dylib)

### Windows

#### x64 (64-bit)

```cmd
python scripts\build_native.py windows-x64 pqclean
```

#### x86 (32-bit)

```cmd
python scripts\build_native.py windows-x86 pqclean
```

#### Output

- Location: `bins\windows-x64\pqc.dll` or `bins\windows-x86\pqc.dll`
- Type: Dynamic link library (.dll)

### Android

#### All ABIs

```bash
export ANDROID_NDK_ROOT=/path/to/android-ndk

# Build for all supported ABIs
./scripts/build_android.sh arm64-v8a pqclean
./scripts/build_android.sh armeabi-v7a pqclean
./scripts/build_android.sh x86_64 pqclean
./scripts/build_android.sh x86 pqclean
```

#### Output

- Location: `bins/android-{ABI}/libpqc.so`
- Type: Shared library (.so)

## Build Scripts

### download_pqclean.py

Downloads and extracts PQClean source code.

```bash
python scripts/download_pqclean.py [options]

Options:
  --ref REF         Git reference to download (default: master)
  --output OUTPUT   Output directory (default: pqclean)

Examples:
  python scripts/download_pqclean.py --ref v0.8.0 --output pqclean-0.8.0
  python scripts/download_pqclean.py --ref main
```

### build_native.sh (Unix)

Builds native libraries for Unix-like systems.

```bash
./scripts/build_native.sh TARGET PQCLEAN_SOURCE

Arguments:
  TARGET           Platform target (e.g., linux-x86_64, macos-arm64)
  PQCLEAN_SOURCE   Path to PQClean source directory

Environment Variables:
  CC               C compiler (default: gcc/clang)
  CXX              C++ compiler (default: g++/clang++)
  CFLAGS           Additional C compiler flags
  LDFLAGS          Additional linker flags
```

### build_native.py (Windows)

Builds native libraries for Windows.

```cmd
python scripts\build_native.py TARGET PQCLEAN_SOURCE

Arguments:
  TARGET           Platform target (windows-x64 or windows-x86)
  PQCLEAN_SOURCE   Path to PQClean source directory
```

### build_android.sh

Builds native libraries for Android.

```bash
./scripts/build_android.sh ABI PQCLEAN_SOURCE

Arguments:
  ABI              Android ABI (arm64-v8a, armeabi-v7a, x86_64, x86)
  PQCLEAN_SOURCE   Path to PQClean source directory

Environment Variables:
  ANDROID_NDK_ROOT Path to Android NDK installation
```

## Development Setup

### 1. Repository Structure

```
PQChub/
├── bins/                    # Pre-compiled binaries (committed)
├── scripts/                 # Build scripts
├── wrappers/               # Language wrappers
│   ├── python/
│   ├── nodejs/
│   ├── go/
│   └── rust/
├── examples/               # Usage examples
├── docs/                   # Documentation
└── tests/                  # Integration tests
```

### 2. Environment Setup

#### Python Development

```bash
cd wrappers/python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest pytest-cov black isort mypy
```

#### Node.js Development

```bash
cd wrappers/nodejs

# Install dependencies
npm install

# Install development dependencies
npm install --save-dev eslint prettier jest
```

#### Go Development

```bash
cd wrappers/go

# Download dependencies
go mod tidy

# Run tests
go test -v ./...
```

#### Rust Development

```bash
cd wrappers/rust

# Build project
cargo build

# Run tests
cargo test

# Install development tools
cargo install cargo-fmt cargo-clippy
```

### 3. Testing

#### Run All Tests

```bash
# From repository root
./scripts/run_tests.sh
```

#### Python Tests

```bash
cd wrappers/python
python -m pytest tests/ -v --cov=pqchub
```

#### Node.js Tests

```bash
cd wrappers/nodejs
npm test
```

#### Go Tests

```bash
cd wrappers/go
go test -v -race ./...
```

#### Rust Tests

```bash
cd wrappers/rust
cargo test --release
```

### 4. Code Quality

#### Python

```bash
# Format code
black wrappers/python/
isort wrappers/python/

# Type checking
mypy wrappers/python/

# Linting
flake8 wrappers/python/
```

#### Node.js

```bash
# Format code
npx prettier --write wrappers/nodejs/

# Linting
npx eslint wrappers/nodejs/
```

#### Go

```bash
# Format code
go fmt ./...

# Linting
golangci-lint run
```

#### Rust

```bash
# Format code
cargo fmt

# Linting
cargo clippy
```

## Troubleshooting

### Common Issues

#### Build Failures

**Problem**: Compiler not found
```
Solution: Install build tools for your platform (see Prerequisites)
```

**Problem**: PQClean source not found
```
Solution: Run download_pqclean.py script first
```

**Problem**: Permission denied on build scripts
```bash
# Solution: Make scripts executable
chmod +x scripts/*.sh
```

#### Library Loading Issues

**Problem**: Library not found at runtime
```
Solution: 
1. Ensure Git LFS is enabled: git lfs install
2. Pull LFS files: git lfs pull
3. Check bins/ directory contains your platform
```

**Problem**: Architecture mismatch
```
Solution: Build for correct architecture or use cross-compilation
```

#### Cross-Compilation Issues

**Problem**: Cross-compiler not found
```bash
# Linux ARM64 example
sudo apt-get install gcc-aarch64-linux-gnu g++-aarch64-linux-gnu
```

**Problem**: Android NDK not found
```bash
# Set NDK path
export ANDROID_NDK_ROOT=/path/to/android-ndk
```

### Debug Build

For debugging, build with debug symbols:

#### Linux/macOS

```bash
CFLAGS="-g -O0" ./scripts/build_native.sh linux-x86_64 pqclean
```

#### Windows

```cmd
python scripts\build_native.py windows-x64 pqclean
# Edit script to add /Zi flag for debug symbols
```

### Verbose Output

Enable verbose output for debugging:

```bash
# Bash scripts
set -x
./scripts/build_native.sh linux-x86_64 pqclean

# Python scripts
python -v scripts/build_native.py windows-x64 pqclean
```

### Performance Profiling

#### Linux

```bash
# Build with profiling
CFLAGS="-pg" ./scripts/build_native.sh linux-x86_64 pqclean

# Profile application
valgrind --tool=callgrind python examples/python/kyber_demo.py
```

#### Windows

```cmd
# Use Visual Studio Diagnostic Tools or Intel VTune
```

### Memory Debugging

#### Linux

```bash
# Check for memory leaks
valgrind --leak-check=full python examples/python/kyber_demo.py
```

#### Address Sanitizer

```bash
# Build with AddressSanitizer
CFLAGS="-fsanitize=address" ./scripts/build_native.sh linux-x86_64 pqclean
```

## Advanced Configuration

### Custom Algorithms

To build with specific algorithms only:

1. Edit build scripts to include/exclude algorithms
2. Modify algorithm lists in `build_native.sh`
3. Update wrapper constants accordingly

### Optimization Flags

#### Performance Optimization

```bash
# Maximum optimization
CFLAGS="-O3 -march=native -mtune=native" ./scripts/build_native.sh linux-x86_64 pqclean
```

#### Size Optimization

```bash
# Optimize for size
CFLAGS="-Os -flto" LDFLAGS="-s" ./scripts/build_native.sh linux-x86_64 pqclean
```

### Static Linking

To create statically linked libraries:

```bash
# Modify build script to use -static flag
LDFLAGS="-static" ./scripts/build_native.sh linux-x86_64 pqclean
```

### Custom PQClean Version

To use a specific PQClean version:

```bash
# Download specific version
python scripts/download_pqclean.py --ref v0.8.0 --output pqclean-0.8.0

# Build with specific version
./scripts/build_native.sh linux-x86_64 pqclean-0.8.0
```

## Continuous Integration

For CI/CD pipelines, see `.github/workflows/build-bins.yml` for reference.

### Docker Builds

Create reproducible builds using Docker:

```dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    git-lfs \
    python3

WORKDIR /build
COPY . .
RUN python scripts/download_pqclean.py
RUN ./scripts/build_native.sh linux-x86_64 pqclean
```

### Build Matrix

For testing multiple configurations:

```yaml
strategy:
  matrix:
    platform: [linux-x86_64, linux-aarch64, macos-x86_64, macos-arm64]
    compiler: [gcc, clang]
    optimization: ["-O2", "-O3"]
```

This comprehensive building guide should help developers set up their environment and build PQChub for any supported platform.