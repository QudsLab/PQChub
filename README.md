# PQChub# PQChub - Universal Post-Quantum Cryptography Binary Distribution



**Universal Binary Distribution for Post-Quantum Cryptography**[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Python Support](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

PQChub provides pre-compiled, ready-to-use Post-Quantum Cryptography (PQC) binaries for multiple platforms. No compilation required - just download and use![![PQClean](https://img.shields.io/badge/source-PQClean-green.svg)](https://github.com/PQClean/PQClean)



[![Build Status](https://github.com/QudsLab/PQChub/actions/workflows/build-bins.yml/badge.svg)](https://github.com/QudsLab/PQChub/actions/workflows/build-bins.yml)> **⚠️ Current Status: Python Wrapper Only**  

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)> This repository currently provides a complete Python wrapper for post-quantum cryptography algorithms.  

> Pre-compiled binaries and other language wrappers are under development.

## 🚀 Quick Start

**PQChub** is a universal binary distribution system for post-quantum cryptography (PQC) algorithms. It provides pre-compiled native libraries and easy-to-use language wrappers for Python, with planned support for Node.js, Go, Rust, Java, and C#.

### Python

```python## 🚀 Quick Start

# Download pqchub.py from examples/python/

import pqchub### Installation



# Auto-downloads correct binary for your platformSimply clone the repository and start using PQC algorithms immediately:

falcon = pqchub.Falcon512()

pk, sk = falcon.keypair()```bash

signed = falcon.sign(b"Hello World", sk)git clone https://github.com/QudsLab/PQChub.git

verified = falcon.verify(signed, pk)cd PQChub

``````



### Node.js### Python Example

```javascript

// Install dependencies: npm install```python

const { loadLibrary, Falcon512 } = require('./pqchub');from wrappers.python import Kyber512, Dilithium2



// Auto-downloads correct binary for your platform# Key Encapsulation (Kyber)

const lib = await loadLibrary();kyber = Kyber512()

const falcon = new Falcon512(lib);public_key, secret_key = kyber.keypair()

const { publicKey, secretKey } = falcon.keypair();ciphertext, shared_secret = kyber.encapsulate(public_key)

```decrypted_secret = kyber.decapsulate(ciphertext, secret_key)

assert shared_secret == decrypted_secret

## 📦 Supported Platforms

# Digital Signatures (Dilithium)

| Platform | Architecture | Status |dilithium = Dilithium2()

|----------|-------------|--------|pk, sk = dilithium.keypair()

| Linux | x86_64 | ✅ Ready |message = b"Hello, post-quantum world!"

| Linux | aarch64 | ✅ Ready |signature = dilithium.sign(message, sk)

| macOS | x86_64 (Intel) | ✅ Ready |assert dilithium.verify(message, signature, pk)

| macOS | ARM64 (Apple Silicon) | ✅ Ready |```

| Windows | x64 | ✅ Ready |

| Windows | x86 | ✅ Ready |### Node.js Example

| Android | arm64-v8a | ✅ Ready |

| Android | armeabi-v7a | ✅ Ready |```javascript

| Android | x86_64 | ✅ Ready |const { Kyber512, Dilithium2 } = require('./wrappers/nodejs');

| Android | x86 | ✅ Ready |

// Key Encapsulation

## 🔐 Supported Algorithmsconst kyber = new Kyber512();

const { publicKey, secretKey } = kyber.keypair();

### Digital Signaturesconst { ciphertext, sharedSecret } = kyber.encapsulate(publicKey);

- **Falcon-512** - Fast, compact signatures (NIST Level 1)const decryptedSecret = kyber.decapsulate(ciphertext, secretKey);

- **Falcon-1024** - High security signatures (NIST Level 5)

// Digital Signatures

### Coming Soonconst dilithium = new Dilithium2();

- **Kyber** - Key Encapsulation Mechanism (KEM)const keys = dilithium.keypair();

- **Dilithium** - Alternative digital signaturesconst message = Buffer.from("Hello, post-quantum world!");

const signature = dilithium.sign(message, keys.secretKey);

## 📚 Documentationconst isValid = dilithium.verify(message, signature, keys.publicKey);

```

- **[Examples](examples/)** - Ready-to-use code examples

  - [Python Example](examples/python/) - Auto-downloading Python wrapper### Go Example

  - [Node.js Example](examples/nodejs/) - Auto-downloading Node.js wrapper

- **[Binaries](bins/)** - Pre-compiled binaries for all platforms```go

- **[Tests](tests/)** - Test suite and validationpackage main



## 🏗️ How It Worksimport (

    "github.com/QudsLab/PQChub/wrappers/go/pqc"

1. **Auto-Detection**: Automatically detects your platform (OS + architecture))

2. **Smart Caching**: Downloads binaries once, caches locally (`~/.pqchub/`)

3. **Direct Usage**: Loads binary via FFI/ctypes - no compilation neededfunc main() {

    // Key Encapsulation

### Binary Metadata    kyber := pqc.NewKyber512()

    publicKey, secretKey, _ := kyber.Keypair()

All binaries are tracked in [`bins/binaries.json`](bins/binaries.json):    ciphertext, sharedSecret, _ := kyber.Encapsulate(publicKey)

```json    decryptedSecret, _ := kyber.Decapsulate(ciphertext, secretKey)

{    

  "windows-x64": {    // Digital Signatures

    "filename": "pqc.dll",    dilithium := pqc.NewDilithium2()

    "size": 37376,    pk, sk, _ := dilithium.Keypair()

    "url": "https://github.com/QudsLab/PQChub/raw/refs/heads/main/bins/windows-x64/pqc.dll"    message := []byte("Hello, post-quantum world!")

  }    signature, _ := dilithium.Sign(message, sk)

}    isValid, _ := dilithium.Verify(message, signature, pk)

```}

```

## 🔧 Building From Source

### Rust Example

Want to build binaries yourself?

```rust

```bashuse pqchub::{Kyber512, Dilithium2};

# Clone repository

git clone https://github.com/QudsLab/PQChub.gitfn main() -> Result<(), Box<dyn std::error::Error>> {

cd PQChub    // Key Encapsulation

    let kyber = Kyber512::new()?;

# Build for your platform    let (public_key, secret_key) = kyber.keypair()?;

python scripts/build_native.py <platform> pqclean-source    let (ciphertext, shared_secret) = kyber.encapsulate(&public_key)?;

    let decrypted_secret = kyber.decapsulate(&ciphertext, &secret_key)?;

# Platforms: windows-x64, windows-x86, linux-x86_64, linux-aarch64,     

#            macos-x86_64, macos-arm64    // Digital Signatures

```    let dilithium = Dilithium2::new()?;

    let (pk, sk) = dilithium.keypair()?;

## 🧪 Testing    let message = b"Hello, post-quantum world!";

    let signature = dilithium.sign(message, &sk)?;

```bash    let is_valid = dilithium.verify(message, &signature, &pk)?;

# Run Python tests    

python tests/test_python.py    Ok(())

}

# Tests automatically use correct binary for your platform```

```

## 🏗️ Architecture

## 📖 Usage Examples

### Core Concept

### Python - Digital Signature

```python- **Build Once, Use Anywhere**: Native binaries compiled weekly via GitHub Actions

from pqchub import Falcon512- **Language Agnostic**: FFI wrappers for multiple programming languages

- **Zero Compilation**: Users clone the repo and immediately use pre-built binaries

# Create instance- **Automated Updates**: CI/CD pipeline auto-updates binaries from [PQClean](https://github.com/PQClean/PQClean) upstream

falcon = Falcon512()

### How It Works

# Generate keypair

public_key, secret_key = falcon.keypair()```

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐

# Sign message│   PQClean       │───▶│   GitHub        │───▶│   Pre-compiled  │

message = b"Important document"│   (upstream)    │    │   Actions       │    │   Binaries      │

signed_message = falcon.sign(message, secret_key)│                 │    │   (weekly)      │    │   (committed)   │

└─────────────────┘    └─────────────────┘    └─────────────────┘

# Verify signature                                                       │

original_message = falcon.verify(signed_message, public_key)                                               ┌───────▼───────┐

assert message == original_message  # Success!                                               │  Language     │

```                                               │  Wrappers     │

                                               │  (FFI)        │

### Node.js - Digital Signature                                               └───────────────┘

```javascript```

const { loadLibrary, Falcon512 } = require('./pqchub');

## 📦 Supported Platforms

async function main() {

    // Load library| Platform | Architecture | Status | Binary |

    const lib = await loadLibrary();|----------|-------------|--------|---------|

    const falcon = new Falcon512(lib);| **Linux** | x86_64 | ✅ | `libpqc.so` |

    | **Linux** | aarch64 | ✅ | `libpqc.so` |

    // Generate keypair| **macOS** | x86_64 (Intel) | ✅ | `libpqc.dylib` |

    const { publicKey, secretKey } = falcon.keypair();| **macOS** | arm64 (Apple Silicon) | ✅ | `libpqc.dylib` |

    | **Windows** | x64 | ✅ | `pqc.dll` |

    // Sign message| **Windows** | x86 | ✅ | `pqc.dll` |

    const message = Buffer.from('Important document');| **Android** | arm64-v8a | ✅ | `libpqc.so` |

    const signed = falcon.sign(message, secretKey);| **Android** | armeabi-v7a | ✅ | `libpqc.so` |

    | **Android** | x86_64 | ✅ | `libpqc.so` |

    // Verify signature| **Android** | x86 | ✅ | `libpqc.so` |

    const verified = falcon.verify(signed, publicKey);

    console.log('Verified:', verified.toString());## 🔐 Supported Algorithms

}

All algorithms are sourced from the [PQClean](https://github.com/PQClean/PQClean) project, which provides reference implementations of NIST-approved post-quantum cryptography algorithms.

main();

```### Key Encapsulation Mechanisms (KEM)



## 🤝 Contributing| Algorithm | Security Level | Public Key | Secret Key | Ciphertext | Shared Secret |

|-----------|---------------|------------|------------|------------|---------------|

Contributions welcome! See our [GitHub Issues](https://github.com/QudsLab/PQChub/issues).| **Kyber512** | 1 | 800 bytes | 1632 bytes | 768 bytes | 32 bytes |

| **Kyber768** | 3 | 1184 bytes | 2400 bytes | 1088 bytes | 32 bytes |

### Areas for Contribution| **Kyber1024** | 5 | 1568 bytes | 3168 bytes | 1568 bytes | 32 bytes |

- Adding more algorithms (Kyber, Dilithium)

- Language wrappers (Rust, Go, C#, Java)### Digital Signature Schemes

- Performance optimizations

- Documentation improvements| Algorithm | Security Level | Public Key | Secret Key | Signature |

|-----------|---------------|------------|------------|-----------|

## 📄 License| **Dilithium2** | 1 | 1312 bytes | 2528 bytes | ~2420 bytes |

| **Dilithium3** | 3 | 1952 bytes | 4000 bytes | ~3293 bytes |

MIT License - see the [LICENSE](LICENSE) file for details.| **Dilithium5** | 5 | 2592 bytes | 4864 bytes | ~4595 bytes |

| **Falcon-512** | 1 | 897 bytes | 1281 bytes | ~690 bytes |

## 🙏 Acknowledgments| **Falcon-1024** | 5 | 1793 bytes | 2305 bytes | ~1330 bytes |



- **PQClean** - Clean, portable implementations of post-quantum cryptography## 🌍 Language Support

- **NIST PQC** - Standardization project for post-quantum cryptography

| Language | Status | Package Manager | Import |

## 🔗 Links|----------|--------|----------------|---------|

| **Python** | ✅ | `pip install -e .` | `from pqchub import Kyber512` |

- [GitHub Repository](https://github.com/QudsLab/PQChub)| **Node.js** | ✅ | `npm install` | `const { Kyber512 } = require('pqchub')` |

- [Issue Tracker](https://github.com/QudsLab/PQChub/issues)| **Go** | ✅ | `go mod tidy` | `import "github.com/QudsLab/PQChub/wrappers/go/pqc"` |

- [PQClean Project](https://github.com/PQClean/PQClean)| **Rust** | ✅ | `cargo add pqchub` | `use pqchub::Kyber512;` |

| **Java** | ✅ | Maven/Gradle | `import com.qudslab.pqchub.Kyber512;` |

## ⚠️ Security Notice| **C#** | ✅ | NuGet | `using PQChub;` |



This is a research and educational project. For production use:## 📖 Documentation

- Review the code carefully

- Test thoroughly in your environment- [**API Reference**](docs/API.md) - Complete API documentation for all languages

- Consider official NIST-standardized implementations- [**Building Guide**](docs/BUILDING.md) - How to build binaries locally

- Keep binaries updated- [**Algorithm Details**](docs/ALGORITHMS.md) - Detailed information about supported algorithms

- [**Contributing**](docs/CONTRIBUTING.md) - How to contribute to the project

---- [**Troubleshooting**](docs/TROUBLESHOOTING.md) - Common issues and solutions



Made with ❤️ by [QudsLab](https://github.com/QudsLab)## 🚀 Getting Started


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