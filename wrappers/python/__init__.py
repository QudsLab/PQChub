"""
PQChub - Python Wrapper for Post-Quantum Cryptography

This package provides Python bindings for post-quantum cryptography algorithms
from the PQClean project. It includes Key Encapsulation Mechanisms (KEM) and
Digital Signature algorithms.

Key Encapsulation Mechanisms (KEM):
    - Kyber512, Kyber768, Kyber1024

Digital Signatures:
    - Dilithium2, Dilithium3, Dilithium5
    - Falcon512, Falcon1024

Example usage:

    from pqchub import Kyber512, Dilithium2
    
    # Key Encapsulation
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
"""

__version__ = "1.0.0"
__author__ = "QudsLab"
__email__ = "contact@qudslab.org"
__url__ = "https://github.com/QudsLab/PQChub"

# Import main classes
from .kyber import Kyber512, Kyber768, Kyber1024, Kyber
from .dilithium import Dilithium2, Dilithium3, Dilithium5, Dilithium
from .falcon import Falcon512, Falcon1024, Falcon
from .pqc import PQCLibrary, get_library
from .utils import (
    get_platform_info,
    find_binary_path,
    PQCError,
    PQCLibraryError,
    PQCKeyGenerationError,
    PQCEncryptionError,
    PQCDecryptionError,
    PQCSignatureError,
    PQCVerificationError,
)

# All exportable symbols
__all__ = [
    # Version info
    '__version__',
    '__author__',
    '__email__',
    '__url__',
    
    # Kyber KEM algorithms
    'Kyber512',
    'Kyber768', 
    'Kyber1024',
    'Kyber',  # Default alias for Kyber768
    
    # Dilithium signature algorithms
    'Dilithium2',
    'Dilithium3',
    'Dilithium5',
    'Dilithium',  # Default alias for Dilithium3
    
    # Falcon signature algorithms
    'Falcon512',
    'Falcon1024',
    'Falcon',  # Default alias for Falcon512
    
    # Library interface
    'PQCLibrary',
    'get_library',
    
    # Utilities
    'get_platform_info',
    'find_binary_path',
    
    # Exceptions
    'PQCError',
    'PQCLibraryError',
    'PQCKeyGenerationError',
    'PQCEncryptionError',
    'PQCDecryptionError',
    'PQCSignatureError',
    'PQCVerificationError',
]


def get_info():
    """Get information about the PQChub library and available algorithms"""
    try:
        lib = get_library()
        platform_info = lib.get_platform_info()
        
        return {
            'version': __version__,
            'platform': platform_info,
            'algorithms': {
                'kem': ['Kyber512', 'Kyber768', 'Kyber1024'],
                'signatures': ['Dilithium2', 'Dilithium3', 'Dilithium5', 
                              'Falcon512', 'Falcon1024'],
            },
            'binary_path': platform_info['binary_path'],
        }
    except Exception as e:
        return {
            'version': __version__,
            'error': str(e),
            'platform': dict(zip(['system', 'architecture'], get_platform_info())),
        }


def test_algorithms():
    """Quick test of all available algorithms"""
    results = {}
    
    # Test Kyber algorithms
    for kyber_class in [Kyber512, Kyber768, Kyber1024]:
        try:
            kyber = kyber_class()
            pk, sk = kyber.keypair()
            ct, ss1 = kyber.encapsulate(pk)
            ss2 = kyber.decapsulate(ct, sk)
            results[kyber_class.__name__] = ss1 == ss2
        except Exception as e:
            results[kyber_class.__name__] = f"Error: {e}"
    
    # Test Dilithium algorithms
    for dilithium_class in [Dilithium2, Dilithium3, Dilithium5]:
        try:
            dilithium = dilithium_class()
            pk, sk = dilithium.keypair()
            message = b"Test message"
            signature = dilithium.sign(message, sk)
            results[dilithium_class.__name__] = dilithium.verify(message, signature, pk)
        except Exception as e:
            results[dilithium_class.__name__] = f"Error: {e}"
    
    # Test Falcon algorithms
    for falcon_class in [Falcon512, Falcon1024]:
        try:
            falcon = falcon_class()
            pk, sk = falcon.keypair()
            message = b"Test message"
            signature = falcon.sign(message, sk)
            results[falcon_class.__name__] = falcon.verify(message, signature, pk)
        except Exception as e:
            results[falcon_class.__name__] = f"Error: {e}"
    
    return results