# API Reference

This document provides a comprehensive API reference for all PQChub language wrappers.

## Table of Contents

- [Python API](#python-api)
- [Node.js API](#nodejs-api)
- [Go API](#go-api)
- [Rust API](#rust-api)
- [Algorithm Specifications](#algorithm-specifications)
- [Error Handling](#error-handling)

## Python API

### Installation

```bash
cd wrappers/python
pip install -e .
```

### Import

```python
from pqchub import Kyber512, Kyber768, Kyber1024, Dilithium2, Dilithium3, Dilithium5
```

### Key Encapsulation Mechanisms (KEM)

#### Kyber512

```python
class Kyber512:
    PUBLIC_KEY_BYTES = 800
    SECRET_KEY_BYTES = 1632
    CIPHERTEXT_BYTES = 768
    SHARED_SECRET_BYTES = 32
    
    def __init__(self, binary_path: Optional[str] = None):
        """Initialize Kyber512 with optional custom binary path"""
    
    def keypair(self) -> Tuple[bytes, bytes]:
        """Generate a key pair
        
        Returns:
            Tuple of (public_key, secret_key)
        
        Raises:
            PQCKeyGenerationError: If key generation fails
        """
    
    def encapsulate(self, public_key: bytes) -> Tuple[bytes, bytes]:
        """Encapsulate a shared secret
        
        Args:
            public_key: Recipient's public key (800 bytes)
            
        Returns:
            Tuple of (ciphertext, shared_secret)
            
        Raises:
            PQCEncryptionError: If encapsulation fails
        """
    
    def decapsulate(self, ciphertext: bytes, secret_key: bytes) -> bytes:
        """Decapsulate the shared secret
        
        Args:
            ciphertext: Ciphertext to decapsulate (768 bytes)
            secret_key: Recipient's secret key (1632 bytes)
            
        Returns:
            The shared secret (32 bytes)
            
        Raises:
            PQCDecryptionError: If decapsulation fails
        """
```

#### Kyber768

```python
class Kyber768:
    PUBLIC_KEY_BYTES = 1184
    SECRET_KEY_BYTES = 2400
    CIPHERTEXT_BYTES = 1088
    SHARED_SECRET_BYTES = 32
    
    # Same methods as Kyber512 with different sizes
```

#### Kyber1024

```python
class Kyber1024:
    PUBLIC_KEY_BYTES = 1568
    SECRET_KEY_BYTES = 3168
    CIPHERTEXT_BYTES = 1568
    SHARED_SECRET_BYTES = 32
    
    # Same methods as Kyber512 with different sizes
```

### Digital Signatures

#### Dilithium2

```python
class Dilithium2:
    PUBLIC_KEY_BYTES = 1312
    SECRET_KEY_BYTES = 2528
    SIGNATURE_BYTES = 2420  # Maximum size
    
    def keypair(self) -> Tuple[bytes, bytes]:
        """Generate a key pair for signatures"""
    
    def sign(self, message: bytes, secret_key: bytes) -> bytes:
        """Sign a message
        
        Args:
            message: Message to sign
            secret_key: Signer's secret key
            
        Returns:
            Signature bytes (variable length, ≤ 2420 bytes)
        """
    
    def verify(self, message: bytes, signature: bytes, public_key: bytes) -> bool:
        """Verify a signature
        
        Args:
            message: Original message
            signature: Signature to verify
            public_key: Signer's public key
            
        Returns:
            True if signature is valid, False otherwise
        """
```

#### Dilithium3

```python
class Dilithium3:
    PUBLIC_KEY_BYTES = 1952
    SECRET_KEY_BYTES = 4000
    SIGNATURE_BYTES = 3293  # Maximum size
    
    # Same methods as Dilithium2
```

#### Dilithium5

```python
class Dilithium5:
    PUBLIC_KEY_BYTES = 2592
    SECRET_KEY_BYTES = 4864
    SIGNATURE_BYTES = 4595  # Maximum size
    
    # Same methods as Dilithium2
```

### Utility Functions

```python
def get_platform_info() -> Tuple[str, str]:
    """Get current platform information
    
    Returns:
        Tuple of (system, architecture)
    """

def find_binary_path(custom_path: Optional[str] = None) -> str:
    """Find the native library path
    
    Args:
        custom_path: Optional custom binary path
        
    Returns:
        Path to the native library
    """

def get_info() -> dict:
    """Get comprehensive library information"""

def test_algorithms() -> dict:
    """Test all available algorithms"""
```

### Exception Classes

```python
class PQCError(Exception):
    """Base exception for PQC operations"""

class PQCLibraryError(PQCError):
    """Error loading or calling PQC library"""

class PQCKeyGenerationError(PQCError):
    """Error during key generation"""

class PQCEncryptionError(PQCError):
    """Error during encryption/encapsulation"""

class PQCDecryptionError(PQCError):
    """Error during decryption/decapsulation"""

class PQCSignatureError(PQCError):
    """Error during signature operations"""

class PQCVerificationError(PQCError):
    """Error during signature verification"""
```

## Node.js API

### Installation

```bash
cd wrappers/nodejs
npm install
```

### Import

```javascript
const { Kyber512, Kyber768, Kyber1024, Dilithium2, Dilithium3, Dilithium5 } = require('pqchub');
```

### Key Encapsulation Mechanisms

#### Kyber512

```javascript
class Kyber512 {
    static PUBLIC_KEY_BYTES = 800;
    static SECRET_KEY_BYTES = 1632;
    static CIPHERTEXT_BYTES = 768;
    static SHARED_SECRET_BYTES = 32;
    
    constructor(binaryPath = null) {
        // Initialize with optional custom binary path
    }
    
    keypair() {
        // Returns: { publicKey: Buffer, secretKey: Buffer }
    }
    
    encapsulate(publicKey) {
        // Args: publicKey (Buffer, 800 bytes)
        // Returns: { ciphertext: Buffer, sharedSecret: Buffer }
    }
    
    decapsulate(ciphertext, secretKey) {
        // Args: ciphertext (Buffer), secretKey (Buffer)
        // Returns: sharedSecret (Buffer)
    }
}
```

### Digital Signatures

#### Dilithium2

```javascript
class Dilithium2 {
    static PUBLIC_KEY_BYTES = 1312;
    static SECRET_KEY_BYTES = 2528;
    static SIGNATURE_BYTES = 2420;
    
    keypair() {
        // Returns: { publicKey: Buffer, secretKey: Buffer }
    }
    
    sign(message, secretKey) {
        // Args: message (Buffer), secretKey (Buffer)
        // Returns: signature (Buffer)
    }
    
    verify(message, signature, publicKey) {
        // Args: message (Buffer), signature (Buffer), publicKey (Buffer)
        // Returns: boolean
    }
}
```

### Utility Functions

```javascript
function getPlatformInfo() {
    // Returns: { system: string, architecture: string }
}

function findBinaryPath(customPath = null) {
    // Returns: string (path to binary)
}

function getInfo() {
    // Returns: object with library information
}

function testAlgorithms() {
    // Returns: object with test results
}
```

## Go API

### Installation

```bash
cd wrappers/go
go mod tidy
```

### Import

```go
import "github.com/QudsLab/PQChub/wrappers/go/pqc"
```

### Key Encapsulation Mechanisms

#### Kyber512

```go
type Kyber512 struct{}

const (
    Kyber512PublicKeyBytes = 800
    Kyber512SecretKeyBytes = 1632
    Kyber512CiphertextBytes = 768
    Kyber512SharedSecretBytes = 32
)

func NewKyber512() *Kyber512

func (k *Kyber512) Keypair() (publicKey, secretKey []byte, err error)

func (k *Kyber512) Encapsulate(publicKey []byte) (ciphertext, sharedSecret []byte, err error)

func (k *Kyber512) Decapsulate(ciphertext, secretKey []byte) (sharedSecret []byte, err error)
```

### Digital Signatures

```go
type Dilithium2 struct{}

const (
    Dilithium2PublicKeyBytes = 1312
    Dilithium2SecretKeyBytes = 2528
    Dilithium2SignatureBytes = 2420
)

func NewDilithium2() *Dilithium2

func (d *Dilithium2) Keypair() (publicKey, secretKey []byte, err error)

func (d *Dilithium2) Sign(message, secretKey []byte) (signature []byte, err error)

func (d *Dilithium2) Verify(message, signature, publicKey []byte) (bool, error)
```

### Error Types

```go
var (
    ErrKeyGeneration   = errors.New("key generation failed")
    ErrEncapsulation   = errors.New("encapsulation failed")
    ErrDecapsulation   = errors.New("decapsulation failed")
    ErrSigning         = errors.New("signing failed")
    ErrVerification    = errors.New("verification failed")
    ErrInvalidKeySize  = errors.New("invalid key size")
    ErrLibraryNotFound = errors.New("PQC library not found")
)
```

## Rust API

### Installation

```toml
[dependencies]
pqchub = { path = "../rust" }
```

### Import

```rust
use pqchub::{Kyber512, Kyber768, Kyber1024, Dilithium2, Dilithium3, Dilithium5};
```

### Key Encapsulation Mechanisms

#### Kyber512

```rust
pub struct Kyber512;

impl Kyber512 {
    pub const PUBLIC_KEY_BYTES: usize = 800;
    pub const SECRET_KEY_BYTES: usize = 1632;
    pub const CIPHERTEXT_BYTES: usize = 768;
    pub const SHARED_SECRET_BYTES: usize = 32;
    
    pub fn new() -> PqcResult<Self>;
    
    pub fn keypair(&self) -> PqcResult<(Vec<u8>, Vec<u8>)>;
    
    pub fn encapsulate(&self, public_key: &[u8]) -> PqcResult<(Vec<u8>, Vec<u8>)>;
    
    pub fn decapsulate(&self, ciphertext: &[u8], secret_key: &[u8]) -> PqcResult<Vec<u8>>;
}
```

### Error Types

```rust
#[derive(Error, Debug)]
pub enum PqcError {
    #[error("Library not found: {0}")]
    LibraryNotFound(String),
    
    #[error("Key generation failed with code {0}")]
    KeyGeneration(i32),
    
    #[error("Encapsulation failed with code {0}")]
    Encapsulation(i32),
    
    #[error("Decapsulation failed with code {0}")]
    Decapsulation(i32),
    
    #[error("Signature generation failed with code {0}")]
    Signing(i32),
    
    #[error("Invalid key size: expected {expected}, got {actual}")]
    InvalidKeySize { expected: usize, actual: usize },
}

pub type PqcResult<T> = Result<T, PqcError>;
```

## Algorithm Specifications

### Key Encapsulation Mechanisms

| Algorithm | Security Level | Public Key | Secret Key | Ciphertext | Shared Secret |
|-----------|----------------|------------|------------|------------|---------------|
| **Kyber512** | NIST Level 1 | 800 bytes | 1632 bytes | 768 bytes | 32 bytes |
| **Kyber768** | NIST Level 3 | 1184 bytes | 2400 bytes | 1088 bytes | 32 bytes |
| **Kyber1024** | NIST Level 5 | 1568 bytes | 3168 bytes | 1568 bytes | 32 bytes |

### Digital Signatures

| Algorithm | Security Level | Public Key | Secret Key | Max Signature |
|-----------|----------------|------------|------------|---------------|
| **Dilithium2** | NIST Level 1 | 1312 bytes | 2528 bytes | 2420 bytes |
| **Dilithium3** | NIST Level 3 | 1952 bytes | 4000 bytes | 3293 bytes |
| **Dilithium5** | NIST Level 5 | 2592 bytes | 4864 bytes | 4595 bytes |

**Notes:**
- Signature sizes are variable and represent maximum possible size
- Actual signature sizes are typically smaller
- All algorithms use deterministic signatures

## Error Handling

### Common Error Patterns

#### Python

```python
try:
    kyber = Kyber512()
    pk, sk = kyber.keypair()
except PQCLibraryError as e:
    print(f"Library error: {e}")
except PQCKeyGenerationError as e:
    print(f"Key generation failed: {e}")
```

#### Node.js

```javascript
try {
    const kyber = new Kyber512();
    const { publicKey, secretKey } = kyber.keypair();
} catch (error) {
    if (error instanceof PQCLibraryError) {
        console.error('Library error:', error.message);
    }
}
```

#### Go

```go
kyber := pqc.NewKyber512()
publicKey, secretKey, err := kyber.Keypair()
if err != nil {
    if errors.Is(err, pqc.ErrLibraryNotFound) {
        log.Fatal("Library not found:", err)
    }
    log.Fatal("Keypair generation failed:", err)
}
```

#### Rust

```rust
let kyber = Kyber512::new()?;
let (public_key, secret_key) = kyber.keypair().map_err(|e| {
    match e {
        PqcError::LibraryNotFound(_) => {
            eprintln!("Library not found: {}", e);
        }
        PqcError::KeyGeneration(code) => {
            eprintln!("Key generation failed with code: {}", code);
        }
        _ => eprintln!("Other error: {}", e),
    }
    e
})?;
```

### Return Codes

Native library functions return the following codes:

- **0**: Success
- **Non-zero**: Error (specific meaning depends on the algorithm)

The wrappers translate these into appropriate exceptions/errors for each language.

## Performance Notes

### Benchmarks

Approximate performance on modern x86_64 hardware:

| Operation | Kyber512 | Kyber768 | Kyber1024 |
|-----------|----------|----------|-----------|
| **Keypair** | ~50μs | ~90μs | ~150μs |
| **Encapsulate** | ~70μs | ~110μs | ~170μs |
| **Decapsulate** | ~80μs | ~120μs | ~190μs |

| Operation | Dilithium2 | Dilithium3 | Dilithium5 |
|-----------|------------|------------|------------|
| **Keypair** | ~150μs | ~300μs | ~600μs |
| **Sign** | ~400μs | ~700μs | ~1400μs |
| **Verify** | ~200μs | ~350μs | ~700μs |

**Notes:**
- Times are approximate and vary by platform
- Key generation is typically the most expensive operation
- Verification is faster than signing for signature algorithms

### Memory Usage

- All operations use stack-allocated buffers where possible
- No dynamic allocation in the native library
- Language wrappers may allocate for return values

### Thread Safety

- Native library functions are thread-safe
- No global state is maintained
- Multiple instances can be used concurrently

## Migration Guide

### From Other Libraries

If migrating from other post-quantum cryptography libraries:

1. **Key Format**: Keys are raw bytes, no ASN.1 or other encoding
2. **Signatures**: Variable length, use actual returned length
3. **Error Handling**: Check language-specific error types
4. **Binary Distribution**: No compilation needed, uses pre-built binaries

### Version Updates

When updating PQChub:

1. Pull latest changes: `git pull`
2. Update Git LFS files: `git lfs pull`
3. Reinstall language-specific packages if needed
4. Check for API changes in release notes

## Security Considerations

### Production Use

- **Algorithm Selection**: Choose security level appropriate for your use case
- **Key Management**: Implement secure key storage and distribution
- **Side Channels**: Consider side-channel attack mitigations
- **Randomness**: Ensure secure random number generation
- **Updates**: Keep algorithms updated to latest implementations

### Threat Model

- **Quantum Resistance**: Algorithms resist known quantum attacks
- **Classical Security**: Algorithms also provide classical security
- **Implementation**: Based on reference implementations from PQClean
- **Validation**: Algorithms are NIST-approved standards

### Best Practices

1. Use appropriate security levels for your threat model
2. Implement proper key lifecycle management
3. Validate all inputs and handle errors gracefully
4. Use authenticated encryption for confidentiality
5. Consider hybrid approaches during transition periods