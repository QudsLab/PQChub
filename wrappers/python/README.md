# PQChub Python Wrapper

This directory contains the Python wrapper for PQChub, providing easy access to post-quantum cryptography algorithms.

## Installation

From the repository root:

```bash
cd wrappers/python
pip install -e .
```

## Quick Start

```python
from pqchub import Kyber512, Dilithium2

# Key Encapsulation Mechanism (KEM)
kyber = Kyber512()
public_key, secret_key = kyber.keypair()
ciphertext, shared_secret = kyber.encapsulate(public_key)
decrypted_secret = kyber.decapsulate(ciphertext, secret_key)
assert shared_secret == decrypted_secret

# Digital Signatures
dilithium = Dilithium2()
pk, sk = dilithium.keypair()
message = b"Hello, post-quantum world!"
signature = dilithium.sign(message, sk)
assert dilithium.verify(message, signature, pk)
```

## Supported Algorithms

### Key Encapsulation Mechanisms (KEM)

| Algorithm | Security Level | Public Key | Secret Key | Ciphertext | Shared Secret |
|-----------|----------------|------------|------------|------------|---------------|
| `Kyber512` | 1 (AES-128) | 800 bytes | 1632 bytes | 768 bytes | 32 bytes |
| `Kyber768` | 3 (AES-192) | 1184 bytes | 2400 bytes | 1088 bytes | 32 bytes |
| `Kyber1024` | 5 (AES-256) | 1568 bytes | 3168 bytes | 1568 bytes | 32 bytes |

### Digital Signatures

| Algorithm | Security Level | Public Key | Secret Key | Signature (max) |
|-----------|----------------|------------|------------|-----------------|
| `Dilithium2` | 1 (AES-128) | 1312 bytes | 2528 bytes | ~2420 bytes |
| `Dilithium3` | 3 (AES-192) | 1952 bytes | 4000 bytes | ~3293 bytes |
| `Dilithium5` | 5 (AES-256) | 2592 bytes | 4864 bytes | ~4595 bytes |
| `Falcon512` | 1 (AES-128) | 897 bytes | 1281 bytes | ~690 bytes |
| `Falcon1024` | 5 (AES-256) | 1793 bytes | 2305 bytes | ~1330 bytes |

## API Reference

### Key Encapsulation (Kyber)

All Kyber classes (`Kyber512`, `Kyber768`, `Kyber1024`) provide:

#### `keypair() -> Tuple[bytes, bytes]`
Generate a new key pair.

**Returns:** `(public_key, secret_key)`

#### `encapsulate(public_key: bytes) -> Tuple[bytes, bytes]`
Encapsulate a shared secret.

**Args:**
- `public_key`: Recipient's public key

**Returns:** `(ciphertext, shared_secret)`

#### `decapsulate(ciphertext: bytes, secret_key: bytes) -> bytes`
Decapsulate the shared secret.

**Args:**
- `ciphertext`: Ciphertext from encapsulation
- `secret_key`: Recipient's secret key

**Returns:** `shared_secret`

### Digital Signatures (Dilithium, Falcon)

All signature classes provide:

#### `keypair() -> Tuple[bytes, bytes]`
Generate a new key pair.

**Returns:** `(public_key, secret_key)`

#### `sign(message: bytes, secret_key: bytes) -> bytes`
Sign a message.

**Args:**
- `message`: Message to sign
- `secret_key`: Signer's secret key

**Returns:** `signature`

#### `verify(message: bytes, signature: bytes, public_key: bytes) -> bool`
Verify a signature.

**Args:**
- `message`: Original message
- `signature`: Signature to verify
- `public_key`: Signer's public key

**Returns:** `True` if valid, `False` otherwise

## Exception Handling

The wrapper provides specific exceptions for different error types:

```python
from pqchub import (
    PQCError,              # Base exception
    PQCLibraryError,       # Library loading/calling errors
    PQCKeyGenerationError, # Key generation failures
    PQCEncryptionError,    # Encapsulation failures
    PQCDecryptionError,    # Decapsulation failures
    PQCSignatureError,     # Signature generation failures
    PQCVerificationError,  # Signature verification failures
)

try:
    kyber = Kyber512()
    pk, sk = kyber.keypair()
except PQCLibraryError as e:
    print(f"Library error: {e}")
except PQCKeyGenerationError as e:
    print(f"Key generation failed: {e}")
```

## Platform Detection

The wrapper automatically detects your platform and loads the appropriate binary:

```python
from pqchub import get_platform_info, find_binary_path

# Get platform information
system, arch = get_platform_info()
print(f"Platform: {system} {arch}")

# Find binary path
binary_path = find_binary_path()
print(f"Using binary: {binary_path}")
```

## Custom Binary Path

You can specify a custom path to the native library:

```python
from pqchub import Kyber512

# Use custom binary
kyber = Kyber512(binary_path="/path/to/custom/libpqc.so")
```

## Library Information

Get information about the loaded library:

```python
from pqchub import get_library, get_info

# Get library instance
lib = get_library()
print(f"Version: {lib.get_version()}")
print(f"Algorithms: {lib.get_algorithms()}")

# Get comprehensive info
info = get_info()
print(info)
```

## Testing

Test all algorithms:

```python
from pqchub import test_algorithms

results = test_algorithms()
for algorithm, result in results.items():
    status = "✓" if result is True else "✗"
    print(f"{status} {algorithm}: {result}")
```

## Performance Considerations

- All operations use pre-compiled native libraries for optimal performance
- Key generation is the most expensive operation
- Signature sizes vary (Falcon produces smaller signatures than Dilithium)
- Memory is automatically managed by Python's garbage collector

## Security Notes

- This wrapper provides reference implementations for research/education
- Always validate inputs in production applications
- Consider side-channel attack mitigations for sensitive deployments
- Regularly update to the latest PQClean implementations

## Thread Safety

The underlying native library operations are thread-safe, but Python's GIL may limit parallelism. For high-performance applications, consider using multiprocessing.

## Troubleshooting

### Common Issues

1. **ImportError**: Library not found
   - Ensure Git LFS is enabled and binaries are downloaded
   - Check platform support in the main README

2. **PQCLibraryError**: Function not found
   - Verify you have the correct binary for your platform
   - Check that all required algorithms are included in the build

3. **Key/Signature length errors**
   - Ensure you're using the correct algorithm constants
   - Validate input data types (must be bytes)

### Debug Information

```python
import pqchub

# Get debug information
try:
    info = pqchub.get_info()
    print("Library loaded successfully:")
    print(f"  Version: {info['version']}")
    print(f"  Platform: {info['platform']}")
    print(f"  Binary: {info['binary_path']}")
except Exception as e:
    print(f"Error loading library: {e}")
```

## Contributing

When contributing to the Python wrapper:

1. Follow PEP 8 style guidelines
2. Add type hints to public APIs
3. Include comprehensive docstrings
4. Add tests for new functionality
5. Update this README for API changes

## Dependencies

- Python 3.8+
- ctypes (built-in)
- No external dependencies

## License

This Python wrapper is part of PQChub and licensed under MIT License.