"""
PQChub Python Wrapper - Falcon Digital Signatures
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


class BaseFalcon(BasePQC):
    """Base class for Falcon signature algorithms"""
    
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
        Generate a key pair for Falcon signatures
        
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
        Sign a message using Falcon
        
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
        Verify a signature using Falcon
        
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


class Falcon512(BaseFalcon):
    """
    Falcon-512 Digital Signature Algorithm
    
    Security Level: 1 (equivalent to AES-128)
    Public Key: 897 bytes
    Secret Key: 1281 bytes
    Signature: ~690 bytes (variable)
    """
    
    PUBLIC_KEY_BYTES = 897
    SECRET_KEY_BYTES = 1281
    SIGNATURE_BYTES = 690
    FUNC_PREFIX = "PQCLEAN_FALCON512_CLEAN"


class Falcon1024(BaseFalcon):
    """
    Falcon-1024 Digital Signature Algorithm
    
    Security Level: 5 (equivalent to AES-256)
    Public Key: 1793 bytes
    Secret Key: 2305 bytes
    Signature: ~1330 bytes (variable)
    """
    
    PUBLIC_KEY_BYTES = 1793
    SECRET_KEY_BYTES = 2305
    SIGNATURE_BYTES = 1330
    FUNC_PREFIX = "PQCLEAN_FALCON1024_CLEAN"


# Convenience aliases
Falcon = Falcon512  # Default to smaller variant