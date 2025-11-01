"""
PQChub Python Wrapper - Dilithium Digital Signatures
"""

import ctypes
from typing import Optional, Tuple

from .pqc import BasePQC
from .utils import (
    validate_key_length,
    validate_message,
    PQCKeyGenerationError,
    PQCSignatureError,
    PQCVerificationError,
)


class BaseDilithium(BasePQC):
    """Base class for Dilithium signature algorithms"""
    
    # Algorithm parameters (to be set by subclasses)
    PUBLIC_KEY_BYTES = 0
    SECRET_KEY_BYTES = 0
    SIGNATURE_BYTES = 0
    
    # Function name prefix (to be set by subclasses)
    FUNC_PREFIX = ""
    
    def get_required_functions(self) -> list:
        """Get required function names for this algorithm"""
        prefix = self.FUNC_PREFIX
        return [
            f"{prefix}_crypto_sign_keypair",
            f"{prefix}_crypto_sign_signature",
            f"{prefix}_crypto_sign_verify",
        ]
    
    def keypair(self) -> Tuple[bytes, bytes]:
        """
        Generate a key pair for Dilithium signatures
        
        Returns:
            Tuple of (public_key, secret_key)
        
        Raises:
            PQCKeyGenerationError: If key generation fails
        """
        public_key = ctypes.create_string_buffer(self.PUBLIC_KEY_BYTES)
        secret_key = ctypes.create_string_buffer(self.SECRET_KEY_BYTES)
        
        func_name = f"{self.FUNC_PREFIX}_crypto_sign_keypair"
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
    
    def sign(self, message: bytes, secret_key: bytes) -> bytes:
        """
        Sign a message using Dilithium
        
        Args:
            message: The message to sign
            secret_key: The signer's secret key
            
        Returns:
            The signature bytes
            
        Raises:
            PQCSignatureError: If signing fails
        """
        validate_message(message)
        validate_key_length(secret_key, self.SECRET_KEY_BYTES, "secret key")
        
        signature = ctypes.create_string_buffer(self.SIGNATURE_BYTES)
        signature_length = ctypes.c_size_t()
        
        func_name = f"{self.FUNC_PREFIX}_crypto_sign_signature"
        func = getattr(self.lib.lib, func_name)
        func.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte),   # signature
            ctypes.POINTER(ctypes.c_size_t),  # signature length
            ctypes.POINTER(ctypes.c_ubyte),   # message
            ctypes.c_size_t,                  # message length
            ctypes.POINTER(ctypes.c_ubyte),   # secret key
        ]
        func.restype = ctypes.c_int
        
        result = func(
            ctypes.cast(signature, ctypes.POINTER(ctypes.c_ubyte)),
            ctypes.byref(signature_length),
            ctypes.cast(ctypes.c_char_p(message), ctypes.POINTER(ctypes.c_ubyte)),
            len(message),
            ctypes.cast(ctypes.c_char_p(secret_key), ctypes.POINTER(ctypes.c_ubyte))
        )
        
        if result != 0:
            raise PQCSignatureError(f"Signature generation failed with code {result}")
        
        # Return only the actual signature length
        actual_length = signature_length.value
        return bytes(signature[:actual_length])
    
    def verify(self, message: bytes, signature: bytes, public_key: bytes) -> bool:
        """
        Verify a signature using Dilithium
        
        Args:
            message: The original message
            signature: The signature to verify
            public_key: The signer's public key
            
        Returns:
            True if signature is valid, False otherwise
            
        Raises:
            PQCVerificationError: If verification operation fails
        """
        validate_message(message)
        validate_key_length(public_key, self.PUBLIC_KEY_BYTES, "public key")
        
        if not isinstance(signature, (bytes, bytearray)):
            raise TypeError("Signature must be bytes or bytearray")
        
        func_name = f"{self.FUNC_PREFIX}_crypto_sign_verify"
        func = getattr(self.lib.lib, func_name)
        func.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte),   # signature
            ctypes.c_size_t,                  # signature length
            ctypes.POINTER(ctypes.c_ubyte),   # message
            ctypes.c_size_t,                  # message length
            ctypes.POINTER(ctypes.c_ubyte),   # public key
        ]
        func.restype = ctypes.c_int
        
        result = func(
            ctypes.cast(ctypes.c_char_p(signature), ctypes.POINTER(ctypes.c_ubyte)),
            len(signature),
            ctypes.cast(ctypes.c_char_p(message), ctypes.POINTER(ctypes.c_ubyte)),
            len(message),
            ctypes.cast(ctypes.c_char_p(public_key), ctypes.POINTER(ctypes.c_ubyte))
        )
        
        # Return value: 0 = valid signature, non-zero = invalid signature
        return result == 0


class Dilithium2(BaseDilithium):
    """
    Dilithium2 Digital Signature Algorithm
    
    Security Level: 1 (equivalent to AES-128)
    Public Key: 1312 bytes
    Secret Key: 2528 bytes
    Signature: ~2420 bytes (variable)
    """
    
    PUBLIC_KEY_BYTES = 1312
    SECRET_KEY_BYTES = 2528
    SIGNATURE_BYTES = 2420
    FUNC_PREFIX = "PQCLEAN_DILITHIUM2_CLEAN"


class Dilithium3(BaseDilithium):
    """
    Dilithium3 Digital Signature Algorithm
    
    Security Level: 3 (equivalent to AES-192)
    Public Key: 1952 bytes
    Secret Key: 4000 bytes
    Signature: ~3293 bytes (variable)
    """
    
    PUBLIC_KEY_BYTES = 1952
    SECRET_KEY_BYTES = 4000
    SIGNATURE_BYTES = 3293
    FUNC_PREFIX = "PQCLEAN_DILITHIUM3_CLEAN"


class Dilithium5(BaseDilithium):
    """
    Dilithium5 Digital Signature Algorithm
    
    Security Level: 5 (equivalent to AES-256)
    Public Key: 2592 bytes
    Secret Key: 4864 bytes
    Signature: ~4595 bytes (variable)
    """
    
    PUBLIC_KEY_BYTES = 2592
    SECRET_KEY_BYTES = 4864
    SIGNATURE_BYTES = 4595
    FUNC_PREFIX = "PQCLEAN_DILITHIUM5_CLEAN"


# Convenience aliases
Dilithium = Dilithium3  # Default to security level 3