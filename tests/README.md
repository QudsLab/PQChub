# PQChub Binary Tests

This directory contains tests for the pre-compiled PQC binaries.

## Test Files

- **`test_python.py`** - Python test using ctypes to load and test the binary
- **`test_c.c`** - C test for direct library usage

## Running Tests

### Python Test

Works on all platforms (Windows, Linux, macOS):

```bash
# From repository root
python tests/test_python.py
```

The Python test will automatically detect your platform and load the appropriate binary from `bins/`.

### C Test

Compile and run on each platform:

**Linux/macOS:**
```bash
# x86_64
gcc tests/test_c.c -o test_c -L./bins/linux-x86_64 -lpqc -Wl,-rpath,./bins/linux-x86_64
./test_c

# macOS
gcc tests/test_c.c -o test_c -L./bins/macos-x86_64 -lpqc
DYLD_LIBRARY_PATH=./bins/macos-x86_64 ./test_c
```

**Windows:**
```cmd
# x64
cl tests\test_c.c /link bins\windows-x64\pqc.lib
test_c.exe

# Or with MSVC
cl tests\test_c.c bins\windows-x64\pqc.lib
```

## What Tests Do

Both tests verify:

1. **Library Loading** - Can load the binary successfully
2. **Library Info** - Version and platform information
3. **Falcon-512** - Digital signature algorithm
   - Generate keypair
   - Sign a message
   - Verify the signature
4. **Falcon-1024** - Larger security parameter (Python only)
5. **Double Signature** - Verify randomness and consistency (Python only)

## Expected Output

```
==========================================================
Testing Post-Quantum Cryptography Algorithms
==========================================================

[TEST] Falcon-512 Digital Signature
  [OK] Keypair generated
  [OK] Message signed (signature size: XXX bytes)
  [OK] Signature verified
  [SUCCESS] Falcon-512 test passed

[TEST] Falcon-1024 Digital Signature
  [OK] Keypair generated
  [OK] Message signed (signature size: XXX bytes)
  [OK] Signature verified
  [SUCCESS] Falcon-1024 test passed

==========================================================
Test Summary
==========================================================
Tests passed: 3
Tests failed: 0
Total tests: 3

[SUCCESS] All tests passed!
```

## CI/CD Testing

Tests are automatically run in GitHub Actions after binaries are built and committed.
