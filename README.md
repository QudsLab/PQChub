# PQChub

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Support](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![PQClean](https://img.shields.io/badge/source-PQClean-green.svg)](https://github.com/PQClean/PQClean)
[![Build Status](https://github.com/QudsLab/PQChub/actions/workflows/build-bins.yml/badge.svg)](https://github.com/QudsLab/PQChub/actions/workflows/build-bins.yml)

Universal binary distribution for Post-Quantum Cryptography (PQC). Pre-compiled, ready-to-use binaries for multiple platforms. No compilation required—just download and use!

## Quick Start

### Python

```python
from wrappers.python import Kyber512, Dilithium2

# Key Encapsulation (Kyber)
kyber = Kyber512()
public_key, secret_key = kyber.keypair()
ciphertext, shared_secret = kyber.encapsulate(public_key)
decrypted_secret = kyber.decapsulate(ciphertext, secret_key)

# Digital Signatures (Dilithium)
dilithium = Dilithium2()
pk, sk = dilithium.keypair()
message = b"Hello, post-quantum world!"
signature = dilithium.sign(message, sk)
assert dilithium.verify(message, signature, pk)
```

### Node.js

```javascript
const { Kyber512, Dilithium2 } = require('./wrappers/nodejs');

// Key Encapsulation
const kyber = new Kyber512();
const { publicKey, secretKey } = kyber.keypair();
const { ciphertext, sharedSecret } = kyber.encapsulate(publicKey);
const decryptedSecret = kyber.decapsulate(ciphertext, secretKey);

// Digital Signatures
const dilithium = new Dilithium2();
const keys = dilithium.keypair();
const message = Buffer.from("Hello, post-quantum world!");
const signature = dilithium.sign(message, keys.secretKey);
const isValid = dilithium.verify(message, signature, keys.publicKey);
```

## Supported Platforms

| Platform | Architecture | Status | Binary |
|----------|-------------|--------|---------|
| Linux | x86_64 | ✅ | `libpqc.so` |
| Linux | aarch64 | ✅ | `libpqc.so` |
| macOS | x86_64 (Intel) | ✅ | `libpqc.dylib` |
| macOS | arm64 (Apple Silicon) | ✅ | `libpqc.dylib` |
| Windows | x64 | ✅ | `pqc.dll` |
| Windows | x86 | ✅ | `pqc.dll` |
| Android | arm64-v8a | ✅ | `libpqc.so` |
| Android | armeabi-v7a | ✅ | `libpqc.so` |
| Android | x86_64 | ✅ | `libpqc.so` |
| Android | x86 | ✅ | `libpqc.so` |

## Supported Algorithms

All algorithms sourced from [PQClean](https://github.com/PQClean/PQClean), providing NIST-approved post-quantum cryptography implementations.

### Key Encapsulation Mechanisms (KEM)

| Algorithm | Security Level | Public Key | Secret Key | Ciphertext | Shared Secret |
|-----------|---------------|------------|------------|------------|---------------|
| Kyber512 | 1 | 800 bytes | 1632 bytes | 768 bytes | 32 bytes |
| Kyber768 | 3 | 1184 bytes | 2400 bytes | 1088 bytes | 32 bytes |
| Kyber1024 | 5 | 1568 bytes | 3168 bytes | 1568 bytes | 32 bytes |

### Digital Signature Schemes

| Algorithm | Security Level | Public Key | Secret Key | Signature |
|-----------|---------------|------------|------------|-----------|
| Dilithium2 | 1 | 1312 bytes | 2528 bytes | ~2420 bytes |
| Dilithium3 | 3 | 1952 bytes | 4000 bytes | ~3293 bytes |
| Dilithium5 | 5 | 2592 bytes | 4864 bytes | ~4595 bytes |
| Falcon-512 | 1 | 897 bytes | 1281 bytes | ~690 bytes |
| Falcon-1024 | 5 | 1793 bytes | 2305 bytes | ~1330 bytes |

## How It Works

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PQClean       │───▶│   GitHub        │───▶│   Pre-compiled  │
│   (upstream)    │    │   Actions       │    │   Binaries      │
│                 │    │   (weekly)      │    │   (committed)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                               ┌───────▼───────┐
                                               │  Language     │
                                               │  Wrappers     │
                                               │  (FFI)        │
                                               └───────────────┘
```
**Build Once, Use Anywhere** — Native binaries compiled weekly via GitHub Actions. Language-agnostic FFI wrappers provide zero-compilation deployment. Simply clone and use pre-built binaries with automated updates from PQClean upstream.

## Binary Update Schedule

Binaries are automatically updated:
- **Weekly**: Every Sunday at 00:00 UTC
- **Manual**: Via GitHub Actions workflow dispatch
- **Source**: Latest commit from [PQClean master branch](https://github.com/PQClean/PQClean)

Check `bins/BUILD_INFO.txt` for latest build information.

## Contributing

Contributions welcome! Areas for contribution:
- Adding more algorithms
- Language wrappers for additional platforms
- Performance optimizations
- Documentation improvements

See [GitHub Issues](https://github.com/QudsLab/PQChub/issues) for current tasks.

## Security Notice

This is a research and educational project. For production use:
- Review code carefully
- Test thoroughly in your environment
- Consider official NIST-standardized implementations
- Keep binaries updated
- Consult with cryptography experts

To report security vulnerabilities, see [SECURITY.md](SECURITY.md).

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- **PQClean** — Clean, portable implementations of post-quantum cryptography
- **NIST PQC** — Standardization project for post-quantum cryptography
  
## Links

- [GitHub Repository](https://github.com/QudsLab/PQChub)
- [Issue Tracker](https://github.com/QudsLab/PQChub/issues)
- [PQClean Project](https://github.com/PQClean/PQClean)
- [NIST PQC](https://csrc.nist.gov/projects/post-quantum-cryptography)

---

**Made with ❤️ by [QudsLab](https://github.com/QudsLab)**
