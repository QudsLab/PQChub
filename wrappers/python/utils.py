"""
PQChub Python Wrapper - Platform Detection and Utilities
"""

import os
import platform
import sys
from pathlib import Path


def get_platform_info():
    """Get current platform information for binary selection"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # Normalize architecture names
    if machine in ['x86_64', 'amd64']:
        arch = 'x86_64'
    elif machine in ['aarch64', 'arm64']:
        arch = 'aarch64' if system == 'linux' else 'arm64'
    elif machine in ['i386', 'i686', 'x86']:
        arch = 'x86'
    elif machine.startswith('arm'):
        arch = 'arm'
    else:
        arch = machine
    
    return system, arch


def get_library_name(system):
    """Get the library file name for the given system"""
    if system == 'windows':
        return 'pqc.dll'
    elif system == 'darwin':
        return 'libpqc.dylib'
    else:  # linux and others
        return 'libpqc.so'


def find_binary_path(custom_path=None):
    """Find the PQC native library for the current platform"""
    if custom_path:
        custom_path = Path(custom_path)
        if custom_path.exists() and custom_path.is_file():
            return str(custom_path)
        else:
            raise FileNotFoundError(f"Custom binary path not found: {custom_path}")
    
    # Get platform info
    system, arch = get_platform_info()
    
    # Determine platform directory name
    if system == 'darwin':
        platform_dir = f"macos-{arch}"
    elif system == 'windows':
        if arch == 'x86_64':
            platform_dir = "windows-x64"
        elif arch == 'x86':
            platform_dir = "windows-x86"
        else:
            raise RuntimeError(f"Unsupported Windows architecture: {arch}")
    elif system == 'linux':
        platform_dir = f"linux-{arch}"
    else:
        raise RuntimeError(f"Unsupported operating system: {system}")
    
    # Get library name
    lib_name = get_library_name(system)
    
    # Find the binary path relative to this module
    module_dir = Path(__file__).parent
    repo_root = module_dir.parent.parent
    binary_path = repo_root / "bins" / platform_dir / lib_name
    
    if not binary_path.exists():
        # Try alternative paths
        alternative_paths = [
            # If running from within the wrapper directory
            module_dir / ".." / ".." / "bins" / platform_dir / lib_name,
            # If installed as a package
            Path(sys.prefix) / "share" / "pqchub" / "bins" / platform_dir / lib_name,
        ]
        
        for alt_path in alternative_paths:
            if alt_path.exists():
                binary_path = alt_path
                break
        else:
            raise FileNotFoundError(
                f"PQC native library not found for platform {platform_dir}.\n"
                f"Expected: {binary_path}\n"
                f"Make sure you have cloned the repository with Git LFS enabled.\n"
                f"Current platform: {system} {arch}"
            )
    
    return str(binary_path.resolve())


def validate_key_length(key, expected_length, key_type="key"):
    """Validate that a key has the expected length"""
    if not isinstance(key, (bytes, bytearray)):
        raise TypeError(f"{key_type} must be bytes or bytearray")
    
    if len(key) != expected_length:
        raise ValueError(
            f"{key_type} must be exactly {expected_length} bytes, "
            f"got {len(key)} bytes"
        )


def validate_message(message):
    """Validate message input"""
    if not isinstance(message, (bytes, bytearray)):
        raise TypeError("Message must be bytes or bytearray")


def secure_zero(data):
    """Securely zero out memory (best effort in Python)"""
    if isinstance(data, bytearray):
        for i in range(len(data)):
            data[i] = 0
    # Note: For bytes objects, we can't zero them as they're immutable
    # This is a limitation of Python's memory management


class PQCError(Exception):
    """Base exception for PQC operations"""
    pass


class PQCLibraryError(PQCError):
    """Error loading or calling PQC library"""
    pass


class PQCKeyGenerationError(PQCError):
    """Error during key generation"""
    pass


class PQCEncryptionError(PQCError):
    """Error during encryption/encapsulation"""
    pass


class PQCDecryptionError(PQCError):
    """Error during decryption/decapsulation"""
    pass


class PQCSignatureError(PQCError):
    """Error during signature operations"""
    pass


class PQCVerificationError(PQCError):
    """Error during signature verification"""
    pass