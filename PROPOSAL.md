# PQChub - Universal Post-Quantum Cryptography Binary Distribution

**Repository**: https://github.com/QudsLab/PQChub

## 🎯 Project Overview

PQChub is a universal binary distribution system for post-quantum cryptography algorithms from the PQClean project. It provides pre-compiled native libraries for all major platforms, enabling developers to use post-quantum cryptography from any programming language without compilation hassles.

## 🏗️ Architecture

### Core Concept
- **Build Once, Use Anywhere**: Native binaries compiled weekly via GitHub Actions
- **Language Agnostic**: FFI wrappers for Python, Node.js, Go, Rust, Java, C#, and more
- **Zero Compilation**: Users clone the repo and immediately use pre-built binaries
- **Automated Updates**: CI/CD pipeline auto-updates binaries from PQClean upstream

## 📁 Repository Structure

```
PQChub/
├── bins/                              # Pre-compiled binaries (committed to Git)
│   ├── linux-x86_64/
│   │   ├── libpqc.so
│   │   └── README.txt
│   ├── linux-aarch64/
│   │   └── libpqc.so
│   ├── macos-x86_64/
│   │   └── libpqc.dylib
│   ├── macos-arm64/
│   │   └── libpqc.dylib
│   ├── windows-x64/
│   │   └── pqc.dll
│   ├── windows-x86/
│   │   └── pqc.dll
│   ├── android-arm64-v8a/
│   │   └── libpqc.so
│   ├── android-armeabi-v7a/
│   │   └── libpqc.so
│   ├── android-x86_64/
│   │   └── libpqc.so
│   ├── android-x86/
│   │   └── libpqc.so
│   ├── BUILD_INFO.txt
│   └── BINARIES.txt
│
├── wrappers/                          # Language-specific FFI wrappers
│   ├── python/
│   │   ├── __init__.py
│   │   ├── pqc.py                   # Main wrapper
│   │   ├── kyber.py                 # KEM algorithms
│   │   ├── dilithium.py             # Signature algorithms
│   │   └── README.md
│   ├── nodejs/
│   │   ├── package.json
│   │   ├── index.js
│   │   ├── lib/
│   │   └── README.md
│   ├── go/
│   │   ├── go.mod
│   │   ├── pqc.go
│   │   └── README.md
│   ├── rust/
│   │   ├── Cargo.toml
│   │   ├── src/lib.rs
│   │   └── README.md
│   ├── java/
│   │   ├── PQC.java
│   │   └── README.md
│   └── csharp/
│       ├── PQC.cs
│       └── README.md
│
├── scripts/                           # Build automation
│   ├── download_pqclean.sh
│   ├── download_pqclean.py
│   ├── build_native.sh
│   ├── build_native.py
│   ├── build_android.sh
│   └── README.md
│
├── .github/
│   └── workflows/
│       ├── build-bins.yml           # Main build workflow
│       └── test-wrappers.yml        # Test wrappers
│
├── examples/                          # Usage examples
│   ├── python/
│   │   ├── kyber_demo.py
│   │   └── dilithium_demo.py
│   ├── nodejs/
│   │   └── kyber_demo.js
│   ├── go/
│   │   └── main.go
│   └── rust/
│       └── main.rs
│
├── docs/                              # Documentation
│   ├── API.md
│   ├── BUILDING.md
│   ├── CONTRIBUTING.md
│   └── ALGORITHMS.md
│
├── tests/                             # Integration tests
│   ├── test_binaries.sh
│   └── test_wrappers/
│
├── README.md
├── LICENSE
├── .gitignore
└── .gitattributes                    # Git LFS config
```

## 🔧 Technical Implementation

### Phase 1: Infrastructure Setup
1. **Download Scripts**: Bash/Python scripts to fetch PQClean source
2. **Build Scripts**: Platform-specific compilation scripts
3. **GitHub Actions**: Automated weekly builds with matrix strategy
4. **Git LFS**: Track binary files efficiently

### Phase 2: Core Binaries
Build native libraries for:
- **Linux**: x86_64, aarch64
- **macOS**: x86_64 (Intel), arm64 (Apple Silicon)
- **Windows**: x64, x86
- **Android**: arm64-v8a, armeabi-v7a, x86_64, x86

### Phase 3: Language Wrappers
Implement thin FFI wrappers for:
- **Python**: ctypes/cffi with automatic platform detection
- **Node.js**: ffi-napi with TypeScript definitions
- **Go**: cgo bindings
- **Rust**: bindgen with safe wrappers
- **Java**: JNA bindings
- **C#**: P/Invoke wrappers

### Phase 4: Documentation & Examples
- Comprehensive API documentation
- Quick start guides per language
- Working examples for each algorithm
- Performance benchmarks

## 🎯 Supported Algorithms

### Key Encapsulation Mechanisms (KEM)
- Kyber512, Kyber768, Kyber1024

### Digital Signatures
- Dilithium2, Dilithium3, Dilithium5
- Falcon-512, Falcon-1024
- SPHINCS+ variants

## 🚀 Workflow

```
┌─────────────────┐
│  Weekly Cron    │
│  GitHub Actions │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Download        │
│ PQClean Source  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Parallel Build  │
│ All Platforms   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Organize into   │
│ bins/<platform> │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Git Commit      │
│ Push to Repo    │
└─────────────────┘
```

## 💡 Key Features

### For Users
- ✅ **No Compilation Required**: Clone and use immediately
- ✅ **Cross-Platform**: Automatic platform detection
- ✅ **Language Agnostic**: Use from any language with FFI
- ✅ **Always Updated**: Weekly rebuilds from upstream
- ✅ **Battle-Tested**: Based on PQClean reference implementations

### For Maintainers
- ✅ **Fully Automated**: CI handles everything
- ✅ **Easy Updates**: Just trigger workflow
- ✅ **Version Controlled**: Binaries tracked in Git with LFS
- ✅ **Reproducible Builds**: Consistent build environment

## 📊 Repository Size Management

- **Source Code**: ~5 MB
- **Binaries (all platforms)**: ~100-150 MB
- **With Git LFS**: ~10 MB clone size
- **Cache Strategy**: Aggressive caching for PQClean source

## 🔒 Security Considerations

- Binaries built in isolated GitHub Actions runners
- Reproducible builds from known PQClean commits
- Build provenance tracked in BUILD_INFO.txt
- Optional: Sign binaries with GPG
- Optional: Provide checksums (SHA256)

## 📈 Success Metrics

- Number of platforms supported: 10+
- Number of language wrappers: 6+
- Build success rate: >95%
- Average build time: <45 minutes
- Repository clone size (with LFS): <20 MB

## 🛠️ Development Roadmap

### Week 1: Foundation
- [ ] Repository setup
- [ ] Download scripts
- [ ] Basic build scripts
- [ ] GitHub Actions workflow (Linux only)

### Week 2: Multi-Platform
- [ ] Add macOS builds
- [ ] Add Windows builds
- [ ] Add Android builds
- [ ] Git LFS setup

### Week 3: Wrappers
- [ ] Python wrapper
- [ ] Node.js wrapper
- [ ] Go wrapper
- [ ] Basic examples

### Week 4: Polish
- [ ] Rust wrapper
- [ ] Java wrapper
- [ ] C# wrapper
- [ ] Comprehensive documentation
- [ ] Testing suite

## 🎓 Usage Example

```python
# Python
from pqchub import Kyber

# Library auto-detects platform
kyber = Kyber.Kyber512()
public_key, secret_key = kyber.keypair()
ciphertext, shared_secret = kyber.encapsulate(public_key)
decrypted_secret = kyber.decapsulate(ciphertext, secret_key)
```

```javascript
// Node.js
const { Kyber } = require('pqchub');

const kyber = new Kyber.Kyber512();
const { publicKey, secretKey } = kyber.keypair();
const { ciphertext, sharedSecret } = kyber.encapsulate(publicKey);
const decryptedSecret = kyber.decapsulate(ciphertext, secretKey);
```

```go
// Go
import "github.com/QudsLab/PQChub/wrappers/go/pqc"

kyber := pqc.NewKyber512()
publicKey, secretKey := kyber.Keypair()
ciphertext, sharedSecret := kyber.Encapsulate(publicKey)
decryptedSecret := kyber.Decapsulate(ciphertext, secretKey)
```

## 🤝 Contributing

- Build scripts welcome for additional platforms
- Language wrapper contributions encouraged
- Documentation improvements appreciated
- Bug reports and feature requests via GitHub Issues

## 📄 License

MIT License - Use freely in commercial and open-source projects

## 🔗 Links

- **Repository**: https://github.com/QudsLab/PQChub
- **PQClean Upstream**: https://github.com/PQClean/PQClean
- **NIST PQC**: https://csrc.nist.gov/projects/post-quantum-cryptography

## 📞 Contact

- **Organization**: QudsLab
- **Issues**: https://github.com/QudsLab/PQChub/issues
- **Discussions**: https://github.com/QudsLab/PQChub/discussions

---

**Note**: This project provides reference implementations. For production use, consult with cryptography experts and follow security best practices.