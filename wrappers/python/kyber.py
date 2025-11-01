"""
PQChub Python Wrapper - Kyber Key Encapsulation Mechanisms
"""

import ctypes
from typing import Optional, Tuple

from .pqc import BasePQC
from .utils import (
    validate_key_length,
    PQCKeyGenerationError,
    PQCEncryptionError,
    PQCDecryptionError,
)


class BaseKyber(BasePQC):
    """Base class for Kyber algorithms"""
    
    # Algorithm parameters (to be set by subclasses)
    PUBLIC_KEY_BYTES = 0
    SECRET_KEY_BYTES = 0
    CIPHERTEXT_BYTES = 0
    SHARED_SECRET_BYTES = 32  # All Kyber variants use 32-byte shared secrets
    
    # Function name prefix (to be set by subclasses)
    FUNC_PREFIX = ""
    
    def get_required_functions(self) -> list:
        """Get required function names for this algorithm"""
        prefix = self.FUNC_PREFIX
        return [
            f"{prefix}_crypto_kem_keypair",
            f"{prefix}_crypto_kem_enc", 
            f"{prefix}_crypto_kem_dec",
        ]
    
    def keypair(self) -> Tuple[bytes, bytes]:
        """
        Generate a key pair for Kyber KEM
        
        Returns:
            Tuple of (public_key, secret_key)
        
        Raises:
            PQCKeyGenerationError: If key generation fails
        """
        public_key = ctypes.create_string_buffer(self.PUBLIC_KEY_BYTES)
        secret_key = ctypes.create_string_buffer(self.SECRET_KEY_BYTES)
        
        func_name = f"{self.FUNC_PREFIX}_crypto_kem_keypair"
        func = getattr(self.lib.lib, func_name)
        func.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
        func.restype = ctypes.c_int
        
        result = func(
            ctypes.cast(public_key, ctypes.POINTER(ctypes.c_ubyte)),
            ctypes.cast(secret_key, ctypes.POINTER(ctypes.c_ubyte))
        )
        
        if result != 0:
            raise PQCKeyGenerationError(f"Key generation failed with code {result}")
        
        return bytes(public_key), bytes(secret_key)
    
    def encapsulate(self, public_key: bytes) -> Tuple[bytes, bytes]:
        """
        Encapsulate a shared secret using the public key
        
        Args:
            public_key: The recipient's public key
            
        Returns:
            Tuple of (ciphertext, shared_secret)
            
        Raises:
            PQCEncryptionError: If encapsulation fails
        """
        validate_key_length(public_key, self.PUBLIC_KEY_BYTES, "public key")
        
        ciphertext = ctypes.create_string_buffer(self.CIPHERTEXT_BYTES)
        shared_secret = ctypes.create_string_buffer(self.SHARED_SECRET_BYTES)
        
        func_name = f"{self.FUNC_PREFIX}_crypto_kem_enc"
        func = getattr(self.lib.lib, func_name)
        func.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte),  # ciphertext
            ctypes.POINTER(ctypes.c_ubyte),  # shared secret
            ctypes.POINTER(ctypes.c_ubyte),  # public key
        ]
        func.restype = ctypes.c_int
        
        result = func(
            ctypes.cast(ciphertext, ctypes.POINTER(ctypes.c_ubyte)),
            ctypes.cast(shared_secret, ctypes.POINTER(ctypes.c_ubyte)),
            ctypes.cast(ctypes.c_char_p(public_key), ctypes.POINTER(ctypes.c_ubyte))
        )
        
        if result != 0:
            raise PQCEncryptionError(f"Encapsulation failed with code {result}")
        
        return bytes(ciphertext), bytes(shared_secret)
    
    def decapsulate(self, ciphertext: bytes, secret_key: bytes) -> bytes:
        """
        Decapsulate the shared secret using the secret key
        
        Args:
            ciphertext: The ciphertext to decapsulate
            secret_key: The recipient's secret key
            
        Returns:
            The shared secret
            
        Raises:
            PQCDecryptionError: If decapsulation fails
        """
        validate_key_length(ciphertext, self.CIPHERTEXT_BYTES, "ciphertext")
        validate_key_length(secret_key, self.SECRET_KEY_BYTES, "secret key")
        
        shared_secret = ctypes.create_string_buffer(self.SHARED_SECRET_BYTES)
        
        func_name = f"{self.FUNC_PREFIX}_crypto_kem_dec"
        func = getattr(self.lib.lib, func_name)
        func.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte),  # shared secret
            ctypes.POINTER(ctypes.c_ubyte),  # ciphertext
            ctypes.POINTER(ctypes.c_ubyte),  # secret key
        ]
        func.restype = ctypes.c_int
        
        result = func(
            ctypes.cast(shared_secret, ctypes.POINTER(ctypes.c_ubyte)),
            ctypes.cast(ctypes.c_char_p(ciphertext), ctypes.POINTER(ctypes.c_ubyte)),
            ctypes.cast(ctypes.c_char_p(secret_key), ctypes.POINTER(ctypes.c_ubyte))
        )
        
        if result != 0:
            raise PQCDecryptionError(f"Decapsulation failed with code {result}")
        
        return bytes(shared_secret)


class Kyber512(BaseKyber):
    """
    Kyber512 Key Encapsulation Mechanism
    
    Security Level: 1 (equivalent to AES-128)
    Public Key: 800 bytes
    Secret Key: 1632 bytes
    Ciphertext: 768 bytes
    Shared Secret: 32 bytes
    """
    
    PUBLIC_KEY_BYTES = 800
    SECRET_KEY_BYTES = 1632
    CIPHERTEXT_BYTES = 768
    FUNC_PREFIX = "PQCLEAN_KYBER512_CLEAN"


class Kyber768(BaseKyber):
    """
    Kyber768 Key Encapsulation Mechanism
    
    Security Level: 3 (equivalent to AES-192)
    Public Key: 1184 bytes
    Secret Key: 2400 bytes
    Ciphertext: 1088 bytes
    Shared Secret: 32 bytes
    """
    
    PUBLIC_KEY_BYTES = 1184
    SECRET_KEY_BYTES = 2400
    CIPHERTEXT_BYTES = 1088
    FUNC_PREFIX = "PQCLEAN_KYBER768_CLEAN"


class Kyber1024(BaseKyber):
    """
    Kyber1024 Key Encapsulation Mechanism
    
    Security Level: 5 (equivalent to AES-256)
    Public Key: 1568 bytes
    Secret Key: 3168 bytes
    Ciphertext: 1568 bytes
    Shared Secret: 32 bytes
    """
    
    PUBLIC_KEY_BYTES = 1568
    SECRET_KEY_BYTES = 3168
    CIPHERTEXT_BYTES = 1568
    FUNC_PREFIX = "PQCLEAN_KYBER1024_CLEAN"


# Convenience aliases
Kyber = Kyber768  # Default to security level 3