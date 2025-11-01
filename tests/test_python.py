#!/usr/bin/env python3
"""
PQChub Python Binary Test
Tests all PQC algorithms for basic functionality
"""

import os
import sys
import platform
import ctypes
from pathlib import Path

# Detect platform and find binary
def find_binary():
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        lib_name = "pqc.dll"
        if "64" in machine or "amd64" in machine:
            platform_dir = "windows-x64"
        else:
            platform_dir = "windows-x86"
    elif system == "darwin":
        lib_name = "libpqc.dylib"
        if "arm" in machine or "aarch64" in machine:
            platform_dir = "macos-arm64"
        else:
            platform_dir = "macos-x86_64"
    elif system == "linux":
        lib_name = "libpqc.so"
        if "aarch64" in machine or "arm64" in machine:
            platform_dir = "linux-aarch64"
        else:
            platform_dir = "linux-x86_64"
    else:
        print(f"[ERROR] Unsupported platform: {system} {machine}")
        return None
    
    # Try to find binary relative to test location
    test_dir = Path(__file__).parent
    repo_root = test_dir.parent
    binary_path = repo_root / "bins" / platform_dir / lib_name
    
    if not binary_path.exists():
        print(f"[ERROR] Binary not found: {binary_path}")
        return None
    
    print(f"[INFO] Using binary: {binary_path}")
    return str(binary_path)

# Load library
binary_path = find_binary()
if not binary_path:
    sys.exit(1)

try:
    lib = ctypes.CDLL(binary_path)
    print("[OK] Library loaded successfully")
except Exception as e:
    print(f"[ERROR] Failed to load library: {e}")
    sys.exit(1)

# Test library info functions
try:
    lib.pqchub_get_version.restype = ctypes.c_char_p
    version = lib.pqchub_get_version().decode('utf-8')
    print(f"[OK] Version: {version}")
    
    lib.pqchub_get_platform.restype = ctypes.c_char_p
    platform_info = lib.pqchub_get_platform().decode('utf-8')
    print(f"[OK] Platform: {platform_info}")
except Exception as e:
    print(f"[WARN] Library info functions not available: {e}")

print("\n" + "="*60)
print("Testing Post-Quantum Cryptography Algorithms")
print("="*60)

# Test counters
tests_passed = 0
tests_failed = 0

# Test Falcon-512 (Digital Signature)
print("\n[TEST] Falcon-512 Digital Signature")
try:
    # Generate keypair
    public_key = ctypes.create_string_buffer(897)
    secret_key = ctypes.create_string_buffer(1281)
    
    result = lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair(public_key, secret_key)
    if result != 0:
        raise Exception(f"Keypair generation failed: {result}")
    print("  [OK] Keypair generated")
    
    # Sign message
    message = b"Test message for Falcon-512"
    signed = ctypes.create_string_buffer(len(message) + 666)
    signed_len = ctypes.c_size_t()
    
    result = lib.PQCLEAN_FALCON512_CLEAN_crypto_sign(
        signed, ctypes.byref(signed_len),
        message, len(message),
        secret_key
    )
    if result != 0:
        raise Exception(f"Signing failed: {result}")
    print(f"  [OK] Message signed (signature size: {signed_len.value} bytes)")
    
    # Verify signature
    verified = ctypes.create_string_buffer(len(message))
    verified_len = ctypes.c_size_t()
    
    result = lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_open(
        verified, ctypes.byref(verified_len),
        signed, signed_len.value,
        public_key
    )
    if result != 0:
        raise Exception(f"Verification failed: {result}")
    
    if verified[:verified_len.value] != message:
        raise Exception("Verified message doesn't match original")
    
    print("  [OK] Signature verified")
    print("  [SUCCESS] Falcon-512 test passed")
    tests_passed += 1
    
except Exception as e:
    print(f"  [FAILED] Falcon-512 test failed: {e}")
    tests_failed += 1

# Test Falcon-1024 (Digital Signature)
print("\n[TEST] Falcon-1024 Digital Signature")
try:
    # Generate keypair
    public_key = ctypes.create_string_buffer(1793)
    secret_key = ctypes.create_string_buffer(2305)
    
    result = lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_keypair(public_key, secret_key)
    if result != 0:
        raise Exception(f"Keypair generation failed: {result}")
    print("  [OK] Keypair generated")
    
    # Sign message
    message = b"Test message for Falcon-1024"
    signed = ctypes.create_string_buffer(len(message) + 1280)
    signed_len = ctypes.c_size_t()
    
    result = lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign(
        signed, ctypes.byref(signed_len),
        message, len(message),
        secret_key
    )
    if result != 0:
        raise Exception(f"Signing failed: {result}")
    print(f"  [OK] Message signed (signature size: {signed_len.value} bytes)")
    
    # Verify signature
    verified = ctypes.create_string_buffer(len(message))
    verified_len = ctypes.c_size_t()
    
    result = lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_open(
        verified, ctypes.byref(verified_len),
        signed, signed_len.value,
        public_key
    )
    if result != 0:
        raise Exception(f"Verification failed: {result}")
    
    if verified[:verified_len.value] != message:
        raise Exception("Verified message doesn't match original")
    
    print("  [OK] Signature verified")
    print("  [SUCCESS] Falcon-1024 test passed")
    tests_passed += 1
    
except Exception as e:
    print(f"  [FAILED] Falcon-1024 test failed: {e}")
    tests_failed += 1

# Test signature twice to ensure consistency
print("\n[TEST] Double signature test (ensure randomness works)")
try:
    public_key = ctypes.create_string_buffer(897)
    secret_key = ctypes.create_string_buffer(1281)
    lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair(public_key, secret_key)
    
    message = b"Consistency test message"
    
    # First signature
    signed1 = ctypes.create_string_buffer(len(message) + 666)
    signed1_len = ctypes.c_size_t()
    lib.PQCLEAN_FALCON512_CLEAN_crypto_sign(
        signed1, ctypes.byref(signed1_len),
        message, len(message), secret_key
    )
    
    # Second signature
    signed2 = ctypes.create_string_buffer(len(message) + 666)
    signed2_len = ctypes.c_size_t()
    lib.PQCLEAN_FALCON512_CLEAN_crypto_sign(
        signed2, ctypes.byref(signed2_len),
        message, len(message), secret_key
    )
    
    # Signatures should be different (due to randomness)
    if signed1.raw[:signed1_len.value] == signed2.raw[:signed2_len.value]:
        print("  [WARN] Signatures are identical (no randomness)")
    else:
        print("  [OK] Signatures are different (randomness working)")
    
    # Both should verify correctly
    verified1 = ctypes.create_string_buffer(len(message))
    verified1_len = ctypes.c_size_t()
    result1 = lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_open(
        verified1, ctypes.byref(verified1_len),
        signed1, signed1_len.value, public_key
    )
    
    verified2 = ctypes.create_string_buffer(len(message))
    verified2_len = ctypes.c_size_t()
    result2 = lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_open(
        verified2, ctypes.byref(verified2_len),
        signed2, signed2_len.value, public_key
    )
    
    if result1 == 0 and result2 == 0:
        print("  [OK] Both signatures verify correctly")
        print("  [SUCCESS] Double signature test passed")
        tests_passed += 1
    else:
        raise Exception("One or both signatures failed to verify")
    
except Exception as e:
    print(f"  [FAILED] Double signature test failed: {e}")
    tests_failed += 1

# Print summary
print("\n" + "="*60)
print("Test Summary")
print("="*60)
print(f"Tests passed: {tests_passed}")
print(f"Tests failed: {tests_failed}")
print(f"Total tests: {tests_passed + tests_failed}")

if tests_failed == 0:
    print("\n[SUCCESS] All tests passed!")
    sys.exit(0)
else:
    print(f"\n[FAILED] {tests_failed} test(s) failed")
    sys.exit(1)
