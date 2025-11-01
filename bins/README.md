# Pre-Compiled PQC Binaries

This directory contains production-ready Post-Quantum Cryptography binaries for all supported platforms. Binaries are built automatically via GitHub Actions and distributed via Git LFS.

## Directory Structure

```
bins/
├── binaries.json          # Metadata with URLs, sizes, checksums
├── linux-x86_64/          # Linux Intel/AMD 64-bit
│   └── libpqc.so
├── linux-aarch64/         # Linux ARM 64-bit
│   └── libpqc.so
├── macos-x86_64/          # macOS Intel
│   └── libpqc.dylib
├── macos-arm64/           # macOS Apple Silicon
│   └── libpqc.dylib
├── windows-x64/           # Windows 64-bit
│   └── pqc.dll
├── windows-x86/           # Windows 32-bit
│   └── pqc.dll
├── android-arm64-v8a/     # Android ARM64
│   └── libpqc.so
├── android-armeabi-v7a/   # Android ARMv7
│   └── libpqc.so
├── android-x86_64/        # Android x86-64
│   └── libpqc.so
└── android-x86/           # Android x86
    └── libpqc.so
```

## Binary Formats

| Platform | Extension | Type |
|----------|-----------|------|
| Linux | `.so` | Shared Object |
| macOS | `.dylib` | Dynamic Library |
| Windows | `.dll` | Dynamic Link Library |
| Android | `.so` | Shared Object |

## Binary Metadata (`binaries.json`)

Auto-generated metadata file with direct download URLs:

```json
{
  "linux-x86_64": {
    "filename": "libpqc.so",
    "size": 425984,
    "url": "https://github.com/QudsLab/PQChub/raw/refs/heads/main/bins/linux-x86_64/libpqc.so"
  },
  "windows-x64": {
    "filename": "pqc.dll",
    "size": 37376,
    "url": "https://github.com/QudsLab/PQChub/raw/refs/heads/main/bins/windows-x64/pqc.dll"
  }
}
```

**Fields:**
- `filename` - Binary filename
- `size` - File size in bytes
- `url` - Direct GitHub raw URL for download

This file is used by auto-downloading wrappers (Python, Node.js) to fetch the correct binary.

## Supported Algorithms

Each binary includes:

### Digital Signatures
- **Falcon-512** (NIST Level 1)
  - Public Key: 897 bytes
  - Secret Key: 1281 bytes
  - Signature: ~666 bytes
  
- **Falcon-1024** (NIST Level 5)
  - Public Key: 1793 bytes
  - Secret Key: 2305 bytes
  - Signature: ~1280 bytes

## Exported Functions

All binaries export these C functions:

```c
// Falcon-512
int falcon512_keypair(uint8_t *pk, uint8_t *sk);
int falcon512_sign(uint8_t *sm, size_t *smlen, const uint8_t *m, size_t mlen, const uint8_t *sk);
int falcon512_open(uint8_t *m, size_t *mlen, const uint8_t *sm, size_t smlen, const uint8_t *pk);

// Falcon-1024
int falcon1024_keypair(uint8_t *pk, uint8_t *sk);
int falcon1024_sign(uint8_t *sm, size_t *smlen, const uint8_t *m, size_t mlen, const uint8_t *sk);
int falcon1024_open(uint8_t *m, size_t *mlen, const uint8_t *sm, size_t smlen, const uint8_t *pk);

// Library info
const char* pqc_lib_name(void);
const char* pqc_lib_version(void);
```

## Using Binaries

### Direct Download

```bash
# Linux x86_64
wget https://github.com/QudsLab/PQChub/raw/main/bins/linux-x86_64/libpqc.so

# Windows x64 (PowerShell)
Invoke-WebRequest -Uri "https://github.com/QudsLab/PQChub/raw/main/bins/windows-x64/pqc.dll" -OutFile "pqc.dll"

# macOS ARM64
curl -L -o libpqc.dylib https://github.com/QudsLab/PQChub/raw/main/bins/macos-arm64/libpqc.dylib
```

### Auto-Download Wrappers

Use our pre-built wrappers that auto-download the correct binary:

**Python:**
```python
from pqchub import Falcon512  # Auto-downloads on first use
falcon = Falcon512()
pk, sk = falcon.keypair()
```

**Node.js:**
```javascript
const { loadLibrary, Falcon512 } = require('./pqchub');
const lib = await loadLibrary();  // Auto-downloads on first use
const falcon = new Falcon512(lib);
```

See [examples/](../examples/) for complete usage.

## Git LFS

Binaries are stored using Git Large File Storage (LFS) to avoid bloating the repository.

### First-Time Setup

```bash
# Install Git LFS
git lfs install

# Clone repository with LFS files
git clone https://github.com/QudsLab/PQChub.git
cd PQChub

# Pull LFS files
git lfs pull
```

### Verify LFS Files

```bash
# Check LFS status
git lfs ls-files

# Should show binaries tracked
# bins/linux-x86_64/libpqc.so
# bins/windows-x64/pqc.dll
# etc.
```

## Building Binaries

Want to build yourself? See [docs/BUILDING.md](../docs/BUILDING.md).

Quick build:
```bash
# Native platform
python scripts/build_native.py <platform> pqclean-source

# Android
./scripts/build_android.sh <abi>
```

Platforms: `linux-x86_64`, `linux-aarch64`, `macos-x86_64`, `macos-arm64`, `windows-x64`, `windows-x86`

Android ABIs: `arm64-v8a`, `armeabi-v7a`, `x86_64`, `x86`

## CI/CD Builds

Binaries are built automatically by GitHub Actions on:
- Push to `main` (when `scripts/` or workflow files change)
- Manual workflow dispatch

See [`.github/workflows/build-bins.yml`](../.github/workflows/build-bins.yml).

### Build Matrix

**Desktop:** Ubuntu 22.04, macOS-13, macOS-14, Windows 2022  
**Android:** Ubuntu 22.04 with NDK r25c  
**Compilers:** MSVC (Windows), GCC/Clang (Unix), NDK toolchain (Android)

## Binary Size Reference

Typical sizes:
- **Linux**: ~400-500 KB
- **macOS**: ~400-500 KB
- **Windows**: ~200-400 KB
- **Android**: ~300-400 KB

Actual sizes vary by algorithm and platform optimizations.

## Security

### Verification

Always verify binaries after download:

```bash
# Check file size matches binaries.json
ls -lh bins/linux-x86_64/libpqc.so

# Check it's not a Git LFS pointer file
file bins/linux-x86_64/libpqc.so
# Should output: "ELF 64-bit LSB shared object" (not "ASCII text")
```

### Build Reproducibility

While binaries are not byte-for-byte reproducible (compiler timestamps, etc.), you can:
1. Build from source using same compiler/flags
2. Compare exported functions with `nm` or `dumpbin`
3. Test functional equivalence with test suite

## Troubleshooting

**Q: Binary is only 132 bytes?**  
A: That's a Git LFS pointer file. Run `git lfs pull`.

**Q: "Error loading shared library"?**  
A: Ensure correct platform binary. Check architecture: `uname -m` (Linux/macOS) or `$env:PROCESSOR_ARCHITECTURE` (Windows).

**Q: Missing symbols?**  
A: Windows may need `/DEF` file during build. See `scripts/build_native.py`.

**Q: Binary won't load on old OS?**  
A: Binaries target recent OS versions. For older systems, build from source with adjusted flags.

## Contributing

Found an issue? Want to add a platform?

1. Open a [GitHub Issue](https://github.com/QudsLab/PQChub/issues)
2. Describe the platform/architecture
3. We'll evaluate and potentially add to CI/CD

See [CONTRIBUTING](../CONTRIBUTING.md) for guidelines.

## License

Binaries are distributed under MIT License - see [LICENSE](../LICENSE).

Built from [PQClean](https://github.com/PQClean/PQClean) implementations.
