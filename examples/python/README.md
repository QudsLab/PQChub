# Python Example - PQChub

Auto-downloading Python wrapper for Post-Quantum Cryptography.

## Installation

No installation needed! Just download `pqchub.py`:

```bash
# Download the wrapper
curl -O https://raw.githubusercontent.com/QudsLab/PQChub/main/examples/python/pqchub.py

# Or use wget
wget https://raw.githubusercontent.com/QudsLab/PQChub/main/examples/python/pqchub.py
```

## Requirements

- Python 3.6+
- No external dependencies (uses stdlib only: `ctypes`, `urllib`, `json`, `os`, `platform`)

## Quick Start

```python
import pqchub

# Falcon-512 (NIST Level 1)
falcon512 = pqchub.Falcon512()
pk, sk = falcon512.keypair()
signed = falcon512.sign(b"Hello World", sk)
message = falcon512.verify(signed, pk)

# Falcon-1024 (NIST Level 5)
falcon1024 = pqchub.Falcon1024()
pk, sk = falcon1024.keypair()
signed = falcon1024.sign(b"Top Secret", sk)
message = falcon1024.verify(signed, pk)
```

## Features

### Auto-Download
- Automatically detects your platform (OS + architecture)
- Downloads the correct binary from GitHub
- Caches binary locally at `~/.pqchub/binaries/`
- Only downloads once - subsequent runs use cached version

### Supported Platforms
- Linux (x86_64, aarch64)
- macOS (x86_64, ARM64)
- Windows (x64, x86)
- Android (arm64-v8a, armeabi-v7a, x86_64, x86)

## API Reference

### `Falcon512`

Fast, compact digital signatures (NIST Level 1).

**Methods:**

```python
# Generate keypair
public_key, secret_key = falcon512.keypair()
# Returns: (bytes, bytes) - 897 byte public key, 1281 byte secret key

# Sign message
signed_message = falcon512.sign(message: bytes, secret_key: bytes)
# Returns: bytes - signed message (original message + signature)

# Verify signature
original_message = falcon512.verify(signed_message: bytes, public_key: bytes)
# Returns: bytes - original message if signature valid, raises error if invalid
```

**Key Sizes:**
- Public Key: 897 bytes
- Secret Key: 1281 bytes
- Signature: ~666 bytes (variable)

### `Falcon1024`

High-security digital signatures (NIST Level 5).

**Methods:**

```python
# Generate keypair
public_key, secret_key = falcon1024.keypair()
# Returns: (bytes, bytes) - 1793 byte public key, 2305 byte secret key

# Sign message
signed_message = falcon1024.sign(message: bytes, secret_key: bytes)
# Returns: bytes - signed message (original message + signature)

# Verify signature
original_message = falcon1024.verify(signed_message: bytes, public_key: bytes)
# Returns: bytes - original message if signature valid, raises error if invalid
```

**Key Sizes:**
- Public Key: 1793 bytes
- Secret Key: 2305 bytes
- Signature: ~1280 bytes (variable)

## Complete Example

```python
import pqchub

def main():
    # Initialize Falcon-512
    falcon = pqchub.Falcon512()
    
    # Generate keypair
    print("Generating keypair...")
    public_key, secret_key = falcon.keypair()
    print(f"Public key: {len(public_key)} bytes")
    print(f"Secret key: {len(secret_key)} bytes")
    
    # Sign a message
    message = b"This is a confidential document."
    print(f"\nOriginal message: {message}")
    
    signed_message = falcon.sign(message, secret_key)
    print(f"Signed message: {len(signed_message)} bytes")
    
    # Verify signature
    verified_message = falcon.verify(signed_message, public_key)
    print(f"Verified message: {verified_message}")
    
    # Confirm authenticity
    assert message == verified_message
    print("\n✅ Signature verified successfully!")

if __name__ == "__main__":
    main()
```

## How It Works

1. **Platform Detection**: `detect_platform()` identifies your OS and architecture
2. **Metadata Fetch**: Downloads `binaries.json` with binary URLs and checksums
3. **Binary Download**: Downloads correct binary to `~/.pqchub/binaries/<platform>/`
4. **Library Loading**: Uses `ctypes.CDLL` to load the native library
5. **FFI Setup**: Configures function signatures for all PQC operations
6. **Ready to Use**: Call `keypair()`, `sign()`, `verify()` methods

## Caching

Binaries are cached at:
- **Linux/macOS**: `~/.pqchub/binaries/<platform>/`
- **Windows**: `C:\Users\<username>\.pqchub\binaries\<platform>\`

To re-download (e.g., after an update):
```bash
# Remove cache
rm -rf ~/.pqchub/binaries/

# Or on Windows
Remove-Item -Recurse -Force $env:USERPROFILE\.pqchub\binaries
```

## Error Handling

```python
try:
    falcon = pqchub.Falcon512()
    pk, sk = falcon.keypair()
except Exception as e:
    print(f"Error: {e}")
    # Common issues:
    # - Network error (can't download binary)
    # - Unsupported platform
    # - Corrupted binary (delete cache and retry)
```

## Troubleshooting

**Q: Binary download fails?**  
A: Check internet connection. GitHub raw URLs must be accessible.

**Q: "Unsupported platform" error?**  
A: Your OS/architecture might not be supported yet. Open a GitHub issue.

**Q: Signature verification fails?**  
A: Ensure you're using the same public key that generated the signature.

**Q: Slow first run?**  
A: Binary is downloaded on first use. Subsequent runs are instant (uses cache).

## Contributing

Want to improve this wrapper? See the main [CONTRIBUTING](../../CONTRIBUTING.md) guide.

Ideas:
- Add more algorithms (Kyber KEM)
- Improve error messages
- Add type hints
- Add async download support

## License

MIT License - see [LICENSE](../../LICENSE) file.
