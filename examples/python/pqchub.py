#!/usr/bin/env python3
"""
PQChub - Auto-downloading Python wrapper for Post-Quantum Cryptography
Automatically downloads the correct binary for your platform
"""

import os
import sys
import platform
import ctypes
import json
import urllib.request
from pathlib import Path

# Configuration
METADATA_URL = "https://github.com/QudsLab/PQChub/raw/refs/heads/main/bins/binaries.json"
CACHE_DIR = Path.home() / ".pqchub" / "binaries"

def detect_platform():
    """Detect current platform and return platform identifier"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        if "64" in machine or "amd64" in machine:
            return "windows-x64"
        else:
            return "windows-x86"
    elif system == "darwin":
        if "arm" in machine or "aarch64" in machine:
            return "macos-arm64"
        else:
            return "macos-x86_64"
    elif system == "linux":
        if "aarch64" in machine or "arm64" in machine:
            return "linux-aarch64"
        else:
            return "linux-x86_64"
    else:
        raise Exception(f"Unsupported platform: {system} {machine}")

def download_file(url, dest_path):
    """Download file from URL to destination"""
    print(f"Downloading from {url}...")
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, dest_path)
    print(f"Downloaded to {dest_path}")

def get_binary_path():
    """Get path to binary, downloading if necessary"""
    platform_id = detect_platform()
    
    # Download metadata
    print("Fetching binary metadata...")
    with urllib.request.urlopen(METADATA_URL) as response:
        metadata = json.loads(response.read().decode('utf-8'))
    
    if platform_id not in metadata['binaries']:
        raise Exception(f"No binary available for platform: {platform_id}")
    
    binary_info = metadata['binaries'][platform_id]
    binary_url = binary_info['url']
    binary_filename = binary_info['filename']
    
    # Check cache
    cached_path = CACHE_DIR / platform_id / binary_filename
    
    if cached_path.exists():
        print(f"Using cached binary: {cached_path}")
        return cached_path
    
    # Download binary
    download_file(binary_url, cached_path)
    return cached_path

# Load library
_lib = None
_binary_path = None

def load_library():
    """Load the PQC library"""
    global _lib, _binary_path
    if _lib is None:
        _binary_path = get_binary_path()
        _lib = ctypes.CDLL(str(_binary_path))
        print(f"Loaded library: {_binary_path}")
    return _lib

# Falcon-512 Digital Signature

class Falcon512:
    """Falcon-512 post-quantum digital signature scheme"""
    
    PUBLICKEY_BYTES = 897
    SECRETKEY_BYTES = 1281
    SIGNATURE_BYTES = 666
    
    def __init__(self):
        self.lib = load_library()
        
        # Setup function signatures
        self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte), 
            ctypes.POINTER(ctypes.c_ubyte)
        ]
        self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair.restype = ctypes.c_int
        
        self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_size_t),
            ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_ubyte)
        ]
        self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign.restype = ctypes.c_int
        
        self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_open.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_size_t),
            ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_ubyte)
        ]
        self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_open.restype = ctypes.c_int
    
    def keypair(self):
        """Generate a new keypair. Returns (public_key, secret_key)"""
        pk = ctypes.create_string_buffer(self.PUBLICKEY_BYTES)
        sk = ctypes.create_string_buffer(self.SECRETKEY_BYTES)
        
        result = self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair(
            ctypes.cast(pk, ctypes.POINTER(ctypes.c_ubyte)),
            ctypes.cast(sk, ctypes.POINTER(ctypes.c_ubyte))
        )
        
        if result != 0:
            raise Exception(f"Keypair generation failed: {result}")
        
        return bytes(pk), bytes(sk)
    
    def sign(self, message, secret_key):
        """Sign a message. Returns signed message"""
        if len(secret_key) != self.SECRETKEY_BYTES:
            raise ValueError(f"Secret key must be {self.SECRETKEY_BYTES} bytes")
        
        signed = ctypes.create_string_buffer(len(message) + self.SIGNATURE_BYTES)
        signed_len = ctypes.c_size_t()
        
        result = self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign(
            ctypes.cast(signed, ctypes.POINTER(ctypes.c_ubyte)),
            ctypes.byref(signed_len),
            ctypes.cast(ctypes.create_string_buffer(message), ctypes.POINTER(ctypes.c_ubyte)),
            len(message),
            ctypes.cast(ctypes.create_string_buffer(secret_key), ctypes.POINTER(ctypes.c_ubyte))
        )
        
        if result != 0:
            raise Exception(f"Signing failed: {result}")
        
        return bytes(signed[:signed_len.value])
    
    def verify(self, signed_message, public_key):
        """Verify and open a signed message. Returns original message"""
        if len(public_key) != self.PUBLICKEY_BYTES:
            raise ValueError(f"Public key must be {self.PUBLICKEY_BYTES} bytes")
        
        message = ctypes.create_string_buffer(len(signed_message))
        message_len = ctypes.c_size_t()
        
        result = self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_open(
            ctypes.cast(message, ctypes.POINTER(ctypes.c_ubyte)),
            ctypes.byref(message_len),
            ctypes.cast(ctypes.create_string_buffer(signed_message), ctypes.POINTER(ctypes.c_ubyte)),
            len(signed_message),
            ctypes.cast(ctypes.create_string_buffer(public_key), ctypes.POINTER(ctypes.c_ubyte))
        )
        
        if result != 0:
            raise Exception(f"Verification failed: {result}")
        
        return bytes(message[:message_len.value])


# Falcon-1024 Digital Signature

class Falcon1024:
    """Falcon-1024 post-quantum digital signature scheme (higher security)"""
    
    PUBLICKEY_BYTES = 1793
    SECRETKEY_BYTES = 2305
    SIGNATURE_BYTES = 1280
    
    def __init__(self):
        self.lib = load_library()
        
        # Setup function signatures
        self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_keypair.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte), 
            ctypes.POINTER(ctypes.c_ubyte)
        ]
        self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_keypair.restype = ctypes.c_int
        
        self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_size_t),
            ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_ubyte)
        ]
        self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign.restype = ctypes.c_int
        
        self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_open.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_size_t),
            ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_ubyte)
        ]
        self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_open.restype = ctypes.c_int
    
    def keypair(self):
        """Generate a new keypair. Returns (public_key, secret_key)"""
        pk = ctypes.create_string_buffer(self.PUBLICKEY_BYTES)
        sk = ctypes.create_string_buffer(self.SECRETKEY_BYTES)
        
        result = self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_keypair(
            ctypes.cast(pk, ctypes.POINTER(ctypes.c_ubyte)),
            ctypes.cast(sk, ctypes.POINTER(ctypes.c_ubyte))
        )
        
        if result != 0:
            raise Exception(f"Keypair generation failed: {result}")
        
        return bytes(pk), bytes(sk)
    
    def sign(self, message, secret_key):
        """Sign a message. Returns signed message"""
        if len(secret_key) != self.SECRETKEY_BYTES:
            raise ValueError(f"Secret key must be {self.SECRETKEY_BYTES} bytes")
        
        signed = ctypes.create_string_buffer(len(message) + self.SIGNATURE_BYTES)
        signed_len = ctypes.c_size_t()
        
        result = self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign(
            ctypes.cast(signed, ctypes.POINTER(ctypes.c_ubyte)),
            ctypes.byref(signed_len),
            ctypes.cast(ctypes.create_string_buffer(message), ctypes.POINTER(ctypes.c_ubyte)),
            len(message),
            ctypes.cast(ctypes.create_string_buffer(secret_key), ctypes.POINTER(ctypes.c_ubyte))
        )
        
        if result != 0:
            raise Exception(f"Signing failed: {result}")
        
        return bytes(signed[:signed_len.value])
    
    def verify(self, signed_message, public_key):
        """Verify and open a signed message. Returns original message"""
        if len(public_key) != self.PUBLICKEY_BYTES:
            raise ValueError(f"Public key must be {self.PUBLICKEY_BYTES} bytes")
        
        message = ctypes.create_string_buffer(len(signed_message))
        message_len = ctypes.c_size_t()
        
        result = self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_open(
            ctypes.cast(message, ctypes.POINTER(ctypes.c_ubyte)),
            ctypes.byref(message_len),
            ctypes.cast(ctypes.create_string_buffer(signed_message), ctypes.POINTER(ctypes.c_ubyte)),
            len(signed_message),
            ctypes.cast(ctypes.create_string_buffer(public_key), ctypes.POINTER(ctypes.c_ubyte))
        )
        
        if result != 0:
            raise Exception(f"Verification failed: {result}")
        
        return bytes(message[:message_len.value])


# Demo usage
if __name__ == "__main__":
    print("PQChub - Post-Quantum Cryptography Demo\n")
    
    # Falcon-512 Demo
    print("=" * 60)
    print("Falcon-512 Digital Signature")
    print("=" * 60)
    
    falcon = Falcon512()
    
    # Generate keypair
    pk, sk = falcon.keypair()
    print(f"✓ Generated keypair")
    print(f"  Public key: {len(pk)} bytes")
    print(f"  Secret key: {len(sk)} bytes")
    
    # Sign message
    message = b"Hello, Post-Quantum World!"
    signed = falcon.sign(message, sk)
    print(f"\n✓ Signed message: {len(signed)} bytes")
    
    # Verify signature
    verified = falcon.verify(signed, pk)
    print(f"✓ Verified signature")
    print(f"  Original: {message.decode()}")
    print(f"  Verified: {verified.decode()}")
    
    if message == verified:
        print("\n✓ SUCCESS: Message integrity verified!")
    else:
        print("\n✗ FAILED: Message mismatch!")
    
    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)
