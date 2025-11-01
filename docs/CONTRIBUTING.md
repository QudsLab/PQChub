# Contributing to PQChub

Thank you for your interest in contributing to PQChub! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Contribution Types](#contribution-types)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Standards](#documentation-standards)
- [Submission Process](#submission-process)
- [Review Process](#review-process)
- [Community](#community)

## Code of Conduct

### Our Pledge

We are committed to making participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behaviors include:**

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behaviors include:**

- The use of sexualized language or imagery
- Personal attacks or insulting/derogatory comments
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at [security@qudslab.org](mailto:security@qudslab.org). All complaints will be reviewed and investigated promptly and fairly.

## Getting Started

### Prerequisites

- **Git** with LFS support
- **GitHub account** with SSH keys configured
- **Development environment** for your target language
- **Basic knowledge** of post-quantum cryptography concepts

### Development Setup

1. **Fork the repository**

   ```bash
   # Visit https://github.com/QudsLab/PQChub/fork
   # Then clone your fork
   git clone git@github.com:YOUR_USERNAME/PQChub.git
   cd PQChub
   ```

2. **Set up upstream remote**

   ```bash
   git remote add upstream git@github.com:QudsLab/PQChub.git
   git remote -v
   ```

3. **Install dependencies**

   ```bash
   # Download PQClean source
   python scripts/download_pqclean.py
   
   # Build native libraries
   ./scripts/build_native.sh $(uname -s | tr '[:upper:]' '[:lower:]')-$(uname -m) pqclean
   ```

4. **Set up development environment**

   ```bash
   # Python
   cd wrappers/python
   python -m venv venv
   source venv/bin/activate
   pip install -e .[dev]
   
   # Node.js
   cd ../nodejs
   npm install
   
   # Go
   cd ../go
   go mod tidy
   
   # Rust
   cd ../rust
   cargo build
   ```

### Running Tests

```bash
# Run all tests
./scripts/run_tests.sh

# Language-specific tests
cd wrappers/python && python -m pytest
cd wrappers/nodejs && npm test
cd wrappers/go && go test ./...
cd wrappers/rust && cargo test
```

## Development Process

### Workflow

1. **Check existing issues** before starting work
2. **Create an issue** for new features or bugs
3. **Create a branch** from `main` for your work
4. **Make changes** following coding standards
5. **Write tests** for new functionality
6. **Update documentation** as needed
7. **Submit a pull request** for review

### Branching Strategy

- **`main`**: Stable, production-ready code
- **`develop`**: Integration branch for new features
- **Feature branches**: `feature/description` or `feature/issue-number`
- **Bug fix branches**: `fix/description` or `fix/issue-number`
- **Documentation**: `docs/description`

### Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

**Examples:**

```bash
git commit -m "feat(python): add Falcon signature algorithm support"
git commit -m "fix(nodejs): resolve memory leak in kyber operations"
git commit -m "docs(api): update encryption function documentation"
git commit -m "test(go): add comprehensive unit tests for dilithium"
```

## Contribution Types

### 1. Algorithm Support

**Adding new PQC algorithms:**

- Update build scripts to include new algorithms
- Add algorithm constants to all language wrappers
- Implement wrapper classes following existing patterns
- Add comprehensive tests
- Update documentation

**Example: Adding Sphincs+**

```python
# wrappers/python/pqchub/sphincs.py
class SphincsPlus128:
    """SPHINCS+ signature algorithm (128-bit security)"""
    
    CRYPTO_PUBLICKEYBYTES = 32
    CRYPTO_SECRETKEYBYTES = 64
    CRYPTO_BYTES = 7856
    
    def __init__(self):
        self._lib = get_pqc_library()
        # Implementation...
```

### 2. Platform Support

**Adding new platforms:**

- Update build scripts for new platform
- Add platform detection logic
- Test on target platform
- Update CI/CD workflows
- Document platform-specific requirements

**Example: Adding FreeBSD support**

```bash
# scripts/build_native.sh
case "$target" in
    freebsd-*)
        CC=${CC:-clang}
        SHARED_LIB_EXT=".so"
        SHARED_LIB_FLAGS="-shared -fPIC"
        ;;
esac
```

### 3. Language Wrappers

**Adding new language support:**

- Create wrapper directory structure
- Implement core classes and functions
- Add platform detection
- Write comprehensive tests
- Update build system
- Document usage patterns

**Wrapper requirements:**
- Support all available algorithms
- Consistent error handling
- Memory safety
- Platform independence
- Comprehensive documentation

### 4. Performance Improvements

**Optimization areas:**

- Build system efficiency
- Memory usage optimization
- Cryptographic operation speed
- Binary size reduction
- Wrapper overhead minimization

**Benchmarking:**

```python
# Always include benchmarks for performance changes
import time

def benchmark_kyber_operations(iterations=1000):
    kyber = Kyber512()
    
    # Benchmark key generation
    start = time.time()
    for _ in range(iterations):
        pk, sk = kyber.keypair()
    keygen_time = time.time() - start
    
    # Continue for encaps/decaps...
```

### 5. Security Enhancements

**Security contributions:**

- Vulnerability fixes
- Side-channel attack mitigations
- Memory protection improvements
- Secure coding practices
- Security audit findings

**Security considerations:**

- Clear memory after use
- Constant-time operations where possible
- Proper error handling
- Input validation
- Documentation of security assumptions

## Coding Standards

### General Principles

- **Consistency**: Follow existing code patterns
- **Clarity**: Write self-documenting code
- **Safety**: Prioritize memory and type safety
- **Performance**: Optimize critical paths
- **Maintainability**: Write code that's easy to understand and modify

### Python Standards

**Style Guide**: Follow PEP 8

```python
# Good
class Kyber512:
    """Kyber-512 KEM implementation."""
    
    CRYPTO_PUBLICKEYBYTES = 800
    CRYPTO_SECRETKEYBYTES = 1632
    
    def __init__(self):
        self._lib = get_pqc_library()
    
    def keypair(self) -> Tuple[bytes, bytes]:
        """Generate a new keypair.
        
        Returns:
            Tuple of (public_key, secret_key)
            
        Raises:
            PQCError: If key generation fails
        """
        # Implementation...
```

**Tools:**
- **Formatter**: `black`
- **Import sorter**: `isort`
- **Type checker**: `mypy`
- **Linter**: `flake8`

```bash
# Format code
black wrappers/python/
isort wrappers/python/

# Check types
mypy wrappers/python/

# Lint
flake8 wrappers/python/
```

### Node.js Standards

**Style Guide**: Airbnb JavaScript Style Guide

```javascript
// Good
class Kyber512 {
  constructor() {
    this.lib = getPqcLibrary();
    this.CRYPTO_PUBLICKEYBYTES = 800;
    this.CRYPTO_SECRETKEYBYTES = 1632;
  }

  /**
   * Generate a new keypair
   * @returns {Object} Object with publicKey and secretKey properties
   * @throws {PQCError} If key generation fails
   */
  keypair() {
    // Implementation...
  }
}
```

**Tools:**
- **Formatter**: `prettier`
- **Linter**: `eslint`
- **Testing**: `jest`

```bash
# Format code
npx prettier --write wrappers/nodejs/

# Lint
npx eslint wrappers/nodejs/

# Test
npm test
```

### Go Standards

**Style Guide**: Go Code Review Comments

```go
// Package pqc provides post-quantum cryptography primitives.
package pqc

// Kyber512 implements the Kyber-512 KEM algorithm.
type Kyber512 struct {
    lib *C.pqc_lib
}

// NewKyber512 creates a new Kyber-512 instance.
func NewKyber512() (*Kyber512, error) {
    lib, err := getPqcLibrary()
    if err != nil {
        return nil, fmt.Errorf("failed to load PQC library: %w", err)
    }
    
    return &Kyber512{lib: lib}, nil
}

// Keypair generates a new keypair.
// Returns the public key, secret key, and any error.
func (k *Kyber512) Keypair() ([]byte, []byte, error) {
    // Implementation...
}
```

**Tools:**
- **Formatter**: `go fmt`
- **Linter**: `golangci-lint`
- **Testing**: `go test`

```bash
# Format code
go fmt ./...

# Lint
golangci-lint run

# Test
go test -v ./...
```

### Rust Standards

**Style Guide**: Rust Style Guide

```rust
//! Post-quantum cryptography library bindings.

use std::ffi::CStr;
use std::os::raw::{c_char, c_int};

/// Kyber-512 KEM implementation.
pub struct Kyber512 {
    lib: *const PqcLib,
}

impl Kyber512 {
    /// Creates a new Kyber-512 instance.
    pub fn new() -> Result<Self, PqcError> {
        let lib = get_pqc_library()?;
        Ok(Self { lib })
    }
    
    /// Generates a new keypair.
    /// 
    /// # Returns
    /// 
    /// A tuple containing (public_key, secret_key).
    /// 
    /// # Errors
    /// 
    /// Returns `PqcError` if key generation fails.
    pub fn keypair(&self) -> Result<(Vec<u8>, Vec<u8>), PqcError> {
        // Implementation...
    }
}
```

**Tools:**
- **Formatter**: `cargo fmt`
- **Linter**: `cargo clippy`
- **Testing**: `cargo test`

```bash
# Format code
cargo fmt

# Lint
cargo clippy

# Test
cargo test
```

### Documentation Standards

**All code must include:**

- **API documentation** for public functions/classes
- **Usage examples** for complex functionality
- **Error documentation** explaining when/why errors occur
- **Security notes** for cryptographic functions
- **Performance notes** for optimization-critical code

**Example:**

```python
def encapsulate(self, public_key: bytes) -> Tuple[bytes, bytes]:
    """Encapsulate a secret using the given public key.
    
    This function generates a random shared secret and encapsulates it
    using the provided public key. The resulting ciphertext can be sent
    to the holder of the corresponding secret key for decapsulation.
    
    Args:
        public_key: The recipient's public key (800 bytes for Kyber-512)
        
    Returns:
        Tuple of (ciphertext, shared_secret):
        - ciphertext: Encapsulated secret (768 bytes for Kyber-512)
        - shared_secret: Random shared secret (32 bytes)
        
    Raises:
        PQCError: If public key is invalid or encapsulation fails
        ValueError: If public key has incorrect length
        
    Example:
        >>> kyber = Kyber512()
        >>> pk, sk = kyber.keypair()
        >>> ct, ss = kyber.encapsulate(pk)
        >>> len(ct), len(ss)
        (768, 32)
        
    Security Note:
        The shared secret should be used immediately for deriving
        encryption keys and then securely erased from memory.
        
    Performance Note:
        This operation takes approximately 0.1ms on modern hardware.
    """
```

## Testing Guidelines

### Test Categories

1. **Unit Tests**: Test individual functions/classes
2. **Integration Tests**: Test wrapper-to-library interaction
3. **Cross-Platform Tests**: Verify behavior across platforms
4. **Performance Tests**: Benchmark critical operations
5. **Security Tests**: Validate cryptographic properties

### Test Requirements

**All contributions must include:**

- **Unit tests** for new functionality
- **Integration tests** for API changes
- **Documentation tests** (doctests) for examples
- **Performance regression tests** for optimizations

### Test Structure

```python
# Python test example
import pytest
from pqchub import Kyber512, PQCError

class TestKyber512:
    """Test suite for Kyber512 implementation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.kyber = Kyber512()
    
    def test_keypair_generation(self):
        """Test basic keypair generation."""
        pk, sk = self.kyber.keypair()
        
        assert len(pk) == self.kyber.CRYPTO_PUBLICKEYBYTES
        assert len(sk) == self.kyber.CRYPTO_SECRETKEYBYTES
        assert pk != sk  # Sanity check
    
    def test_encaps_decaps_roundtrip(self):
        """Test encryption/decryption roundtrip."""
        pk, sk = self.kyber.keypair()
        ct, ss1 = self.kyber.encapsulate(pk)
        ss2 = self.kyber.decapsulate(ct, sk)
        
        assert ss1 == ss2
        assert len(ct) == self.kyber.CRYPTO_CIPHERTEXTBYTES
        assert len(ss1) == 32  # Shared secret length
    
    def test_invalid_public_key(self):
        """Test handling of invalid public key."""
        with pytest.raises(ValueError):
            self.kyber.encapsulate(b"invalid_key")
    
    @pytest.mark.performance
    def test_performance_benchmark(self):
        """Benchmark key operations."""
        import time
        
        # Benchmark keypair generation
        start = time.time()
        for _ in range(100):
            self.kyber.keypair()
        keygen_time = time.time() - start
        
        # Should be reasonable (adjust threshold as needed)
        assert keygen_time < 1.0  # 100 keypairs in under 1 second
```

### Cross-Platform Testing

```python
# Test platform-specific behavior
@pytest.mark.parametrize("platform", ["linux", "macos", "windows"])
def test_library_loading(platform):
    """Test library loading on different platforms."""
    # Mock platform detection
    with patch("pqchub.utils.detect_platform", return_value=platform):
        kyber = Kyber512()
        pk, sk = kyber.keypair()
        assert len(pk) == 800
```

### Security Testing

```python
def test_key_uniqueness(self):
    """Ensure generated keys are unique."""
    keys = set()
    for _ in range(100):
        pk, sk = self.kyber.keypair()
        key_pair = (pk, sk)
        assert key_pair not in keys
        keys.add(key_pair)

def test_shared_secret_uniqueness(self):
    """Ensure shared secrets are unique."""
    pk, sk = self.kyber.keypair()
    secrets = set()
    
    for _ in range(100):
        ct, ss = self.kyber.encapsulate(pk)
        assert ss not in secrets
        secrets.add(ss)
```

## Documentation Standards

### Required Documentation

1. **README updates** for new features
2. **API documentation** for all public interfaces
3. **Usage examples** for complex functionality
4. **Building instructions** for new platforms
5. **Migration guides** for breaking changes

### Documentation Format

- **Markdown** for general documentation
- **Docstrings** for inline API documentation
- **Type hints** for Python code
- **JSDoc** for JavaScript code
- **Rustdoc** for Rust code
- **Go doc** for Go code

### Example Updates

When adding a new algorithm:

1. **Update README.md**:
   ```markdown
   ### Supported Algorithms
   
   #### Key Encapsulation Mechanisms (KEMs)
   - **Kyber512**: 128-bit security, 800-byte public keys
   - **Kyber768**: 192-bit security, 1184-byte public keys
   - **Kyber1024**: 256-bit security, 1568-byte public keys
   - **NewAlgorithm**: 128-bit security, XXX-byte public keys ← ADD THIS
   ```

2. **Update API.md**:
   ```markdown
   ## NewAlgorithm Class
   
   ### Constructor
   ```python
   NewAlgorithm()
   ```
   
   ### Methods
   [Detailed documentation...]
   ```

3. **Add examples**:
   ```python
   # examples/python/new_algorithm_demo.py
   from pqchub import NewAlgorithm
   
   def main():
       # Demonstration code...
   ```

## Submission Process

### Before Submitting

1. **Run all tests**: `./scripts/run_tests.sh`
2. **Check code style**: Run formatters and linters
3. **Update documentation**: Include relevant docs updates
4. **Rebase on main**: Ensure clean commit history
5. **Test on multiple platforms**: If possible

### Pull Request Template

```markdown
## Description

Brief description of changes.

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Performance impact assessed

## Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Code is commented, particularly in hard-to-understand areas
- [ ] Corresponding documentation updates made
- [ ] Changes generate no new warnings
- [ ] Tests pass locally

## Platform Testing

- [ ] Linux x86_64
- [ ] Linux ARM64
- [ ] macOS x86_64
- [ ] macOS ARM64
- [ ] Windows x64
- [ ] Android (if applicable)

## Additional Notes

Any additional information for reviewers.
```

### Commit Checklist

```bash
# Before committing
git add .
git status                    # Review staged changes
./scripts/run_tests.sh       # Run tests
git commit -m "feat: ..."    # Use conventional commits
git push origin feature-branch
```

## Review Process

### Review Criteria

**Code Quality:**
- Follows coding standards
- Includes appropriate tests
- Has clear documentation
- Handles errors properly
- Is maintainable

**Security:**
- No security vulnerabilities
- Proper input validation
- Secure memory handling
- Cryptographic best practices

**Performance:**
- No performance regressions
- Efficient algorithms
- Minimal memory usage
- Benchmarks for critical paths

**Compatibility:**
- Works across platforms
- Maintains API compatibility
- Follows semantic versioning
- Includes migration guides for breaking changes

### Review Timeline

- **Initial review**: Within 2-3 business days
- **Follow-up reviews**: Within 1-2 business days
- **Security reviews**: May require additional time
- **Large features**: May be split into multiple PRs

### Review Process

1. **Automated checks**: CI/CD pipeline runs tests
2. **Code review**: Maintainers review code quality
3. **Security review**: Security-critical changes get extra review
4. **Platform testing**: Changes tested on multiple platforms
5. **Documentation review**: Docs are accurate and complete
6. **Final approval**: Maintainer approves and merges

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Email**: security@qudslab.org (security issues only)

### Getting Help

1. **Check existing documentation** first
2. **Search existing issues** before creating new ones
3. **Provide minimal reproducible examples** for bugs
4. **Include platform/version information** in reports

### Reporting Issues

**Bug Report Template:**

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment:**
- OS: [e.g. Ubuntu 22.04]
- Architecture: [e.g. x86_64]
- Python version: [e.g. 3.9.0]
- PQChub version: [e.g. 1.0.0]

**Additional context**
Add any other context about the problem here.
```

### Feature Requests

**Feature Request Template:**

```markdown
**Is your feature request related to a problem?**
A clear and concise description of what the problem is.

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions.

**Additional context**
Add any other context or screenshots about the feature request.
```

### Recognition

Contributors will be recognized in:

- **CONTRIBUTORS.md**: List of all contributors
- **Release notes**: Major contributions highlighted
- **Commit history**: Permanent record of contributions
- **Social media**: Significant contributions may be highlighted

Thank you for contributing to PQChub! Your efforts help advance post-quantum cryptography adoption and security.