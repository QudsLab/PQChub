# PQChub - Universal Post-Quantum Cryptography Binary Distribution

[![Build Status](https://github.com/QudsLab/PQChub/workflows/Build%20Binaries/badge.svg)](https://github.com/QudsLab/PQChub/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platforms](https://img.shields.io/badge/platforms-Linux%20%7C%20macOS%20%7C%20Windows%20%7C%20Android-blue)](https://github.com/QudsLab/PQChub)
[![Languages](https://img.shields.io/badge/languages-Python%20%7C%20Node.js%20%7C%20Go%20%7C%20Rust%20%7C%20Java%20%7C%20C%23-green)](https://github.com/QudsLab/PQChub)

**PQChub** is a universal binary distribution system for post-quantum cryptography algorithms. It provides pre-compiled native libraries for all major platforms, enabling developers to use post-quantum cryptography from any programming language without compilation hassles.

## 🚀 Quick Start

### Installation

Simply clone the repository and start using PQC algorithms immediately:

```bash
git clone https://github.com/QudsLab/PQChub.git
cd PQChub
```

### Python Example

```python
from wrappers.python import Kyber512, Dilithium2

# Key Encapsulation (Kyber)
kyber = Kyber512()
public_key, secret_key = kyber.keypair()
ciphertext, shared_secret = kyber.encapsulate(public_key)
decrypted_secret = kyber.decapsulate(ciphertext, secret_key)
assert shared_secret == decrypted_secret

# Digital Signatures (Dilithium)
dilithium = Dilithium2()
pk, sk = dilithium.keypair()
message = b"Hello, post-quantum world!"
signature = dilithium.sign(message, sk)
assert dilithium.verify(message, signature, pk)
```

### Node.js Example

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

### Go Example

```go
package main

import (
    "github.com/QudsLab/PQChub/wrappers/go/pqc"
)

func main() {
    // Key Encapsulation
    kyber := pqc.NewKyber512()
    publicKey, secretKey, _ := kyber.Keypair()
    ciphertext, sharedSecret, _ := kyber.Encapsulate(publicKey)
    decryptedSecret, _ := kyber.Decapsulate(ciphertext, secretKey)
    
    // Digital Signatures
    dilithium := pqc.NewDilithium2()
    pk, sk, _ := dilithium.Keypair()
    message := []byte("Hello, post-quantum world!")
    signature, _ := dilithium.Sign(message, sk)
    isValid, _ := dilithium.Verify(message, signature, pk)
}
```

### Rust Example

```rust
use pqchub::{Kyber512, Dilithium2};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Key Encapsulation
    let kyber = Kyber512::new()?;
    let (public_key, secret_key) = kyber.keypair()?;
    let (ciphertext, shared_secret) = kyber.encapsulate(&public_key)?;
    let decrypted_secret = kyber.decapsulate(&ciphertext, &secret_key)?;
    
    // Digital Signatures
    let dilithium = Dilithium2::new()?;
    let (pk, sk) = dilithium.keypair()?;
    let message = b"Hello, post-quantum world!";
    let signature = dilithium.sign(message, &sk)?;
    let is_valid = dilithium.verify(message, &signature, &pk)?;
    
    Ok(())
}
```

## 🏗️ Architecture

### Core Concept

- **Build Once, Use Anywhere**: Native binaries compiled weekly via GitHub Actions
- **Language Agnostic**: FFI wrappers for multiple programming languages
- **Zero Compilation**: Users clone the repo and immediately use pre-built binaries
- **Automated Updates**: CI/CD pipeline auto-updates binaries from [PQClean](https://github.com/PQClean/PQClean) upstream

### How It Works

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

## 📦 Supported Platforms

| Platform | Architecture | Status | Binary |
|----------|-------------|--------|---------|
| **Linux** | x86_64 | ✅ | `libpqc.so` |
| **Linux** | aarch64 | ✅ | `libpqc.so` |
| **macOS** | x86_64 (Intel) | ✅ | `libpqc.dylib` |
| **macOS** | arm64 (Apple Silicon) | ✅ | `libpqc.dylib` |
| **Windows** | x64 | ✅ | `pqc.dll` |
| **Windows** | x86 | ✅ | `pqc.dll` |
| **Android** | arm64-v8a | ✅ | `libpqc.so` |
| **Android** | armeabi-v7a | ✅ | `libpqc.so` |
| **Android** | x86_64 | ✅ | `libpqc.so` |
| **Android** | x86 | ✅ | `libpqc.so` |

## 🔐 Supported Algorithms

All algorithms are sourced from the [PQClean](https://github.com/PQClean/PQClean) project, which provides reference implementations of NIST-approved post-quantum cryptography algorithms.

### Key Encapsulation Mechanisms (KEM)

| Algorithm | Security Level | Public Key | Secret Key | Ciphertext | Shared Secret |
|-----------|---------------|------------|------------|------------|---------------|
| **Kyber512** | 1 | 800 bytes | 1632 bytes | 768 bytes | 32 bytes |
| **Kyber768** | 3 | 1184 bytes | 2400 bytes | 1088 bytes | 32 bytes |
| **Kyber1024** | 5 | 1568 bytes | 3168 bytes | 1568 bytes | 32 bytes |

### Digital Signature Schemes

| Algorithm | Security Level | Public Key | Secret Key | Signature |
|-----------|---------------|------------|------------|-----------|
| **Dilithium2** | 1 | 1312 bytes | 2528 bytes | ~2420 bytes |
| **Dilithium3** | 3 | 1952 bytes | 4000 bytes | ~3293 bytes |
| **Dilithium5** | 5 | 2592 bytes | 4864 bytes | ~4595 bytes |
| **Falcon-512** | 1 | 897 bytes | 1281 bytes | ~690 bytes |
| **Falcon-1024** | 5 | 1793 bytes | 2305 bytes | ~1330 bytes |

## 🌍 Language Support

| Language | Status | Package Manager | Import |
|----------|--------|----------------|---------|
| **Python** | ✅ | `pip install -e .` | `from pqchub import Kyber512` |
| **Node.js** | ✅ | `npm install` | `const { Kyber512 } = require('pqchub')` |
| **Go** | ✅ | `go mod tidy` | `import "github.com/QudsLab/PQChub/wrappers/go/pqc"` |
| **Rust** | ✅ | `cargo add pqchub` | `use pqchub::Kyber512;` |
| **Java** | ✅ | Maven/Gradle | `import com.qudslab.pqchub.Kyber512;` |
| **C#** | ✅ | NuGet | `using PQChub;` |

## 📖 Documentation

- [**API Reference**](docs/API.md) - Complete API documentation for all languages
- [**Building Guide**](docs/BUILDING.md) - How to build binaries locally
- [**Algorithm Details**](docs/ALGORITHMS.md) - Detailed information about supported algorithms
- [**Contributing**](docs/CONTRIBUTING.md) - How to contribute to the project
- [**Troubleshooting**](docs/TROUBLESHOOTING.md) - Common issues and solutions

## 🚀 Getting Started

### Prerequisites

- Git with LFS support
- Your preferred programming language runtime

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/QudsLab/PQChub.git
   cd PQChub
   ```

2. **Choose your language wrapper**:
   ```bash
   # Python
   cd wrappers/python && pip install -e .
   
   # Node.js
   cd wrappers/nodejs && npm install
   
   # Go
   cd wrappers/go && go mod tidy
   
   # Rust
   cd wrappers/rust && cargo build
   ```

3. **Run examples**:
   ```bash
   # Python
   python examples/python/kyber_demo.py
   
   # Node.js
   node examples/nodejs/kyber_demo.js
   
   # Go
   cd examples/go && go run main.go
   
   # Rust
   cd examples/rust && cargo run
   ```

## 🔧 Advanced Usage

### Custom Binary Paths

You can specify custom binary paths if needed:

```python
from wrappers.python import Kyber512

# Use custom binary path
kyber = Kyber512(binary_path="/path/to/custom/libpqc.so")
```

### Error Handling

All wrappers provide comprehensive error handling:

```python
try:
    kyber = Kyber512()
    public_key, secret_key = kyber.keypair()
except Exception as e:
    print(f"Error: {e}")
```

### Performance Considerations

- Binaries are optimized for each platform
- No runtime compilation overhead
- Minimal memory footprint
- Thread-safe operations

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `./scripts/run_tests.sh`
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 🔒 Security

This project provides reference implementations for educational and research purposes. For production use:

- Consult with cryptography experts
- Follow security best practices
- Consider side-channel attack mitigations
- Validate algorithm implementations

To report security vulnerabilities, please see [SECURITY.md](SECURITY.md).

## 📊 Binary Update Schedule

Binaries are automatically updated:

- **Weekly**: Every Sunday at 00:00 UTC
- **Manual**: Via GitHub Actions workflow dispatch
- **Source**: Latest commit from [PQClean master branch](https://github.com/PQClean/PQClean)

Check `bins/BUILD_INFO.txt` for the latest build information.

## 🐛 Troubleshooting

### Common Issues

1. **Binary not found**: Ensure Git LFS is installed and files are downloaded
2. **Platform not supported**: Check supported platforms table above
3. **Import errors**: Verify wrapper installation and dependencies

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for detailed solutions.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: https://github.com/QudsLab/PQChub
- **PQClean Upstream**: https://github.com/PQClean/PQClean
- **NIST PQC**: https://csrc.nist.gov/projects/post-quantum-cryptography
- **Issues**: https://github.com/QudsLab/PQChub/issues
- **Discussions**: https://github.com/QudsLab/PQChub/discussions

## 🏢 Organization

**QudsLab** - Advancing cryptographic research and development

- Website: https://qudslab.org
- GitHub: https://github.com/QudsLab
- Contact: contact@qudslab.org

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

## 📈 Statistics

- **Platforms Supported**: 10
- **Programming Languages**: 6
- **Algorithms**: 8
- **Weekly Downloads**: ~50GB (estimated)
- **Repository Size**: ~150MB (with LFS)

---

**Note**: This project is for research and educational purposes. Always consult with cryptography experts for production deployments.