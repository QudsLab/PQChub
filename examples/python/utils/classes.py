import ctypes
from .bin import get_binary_path

def load_library(metadata_url, cache_dir):
    success, is_new, binary_path = get_binary_path(metadata_url, cache_dir)
    if success and binary_path:
        return ctypes.CDLL(str(binary_path))
    raise Exception(f"Failed to load library: {binary_path}")

class MLKEM512:
    PUBLICKEY_BYTES = 800
    SECRETKEY_BYTES = 1632
    CIPHERTEXT_BYTES = 768
    SHAREDSECRET_BYTES = 32
    def __init__(self, metadata_url, cache_dir):
        self.lib = load_library(metadata_url, cache_dir)
        self.lib.PQCLEAN_MLKEM512_CLEAN_crypto_kem_keypair.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLKEM512_CLEAN_crypto_kem_keypair.restype = ctypes.c_int
        self.lib.PQCLEAN_MLKEM512_CLEAN_crypto_kem_enc.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLKEM512_CLEAN_crypto_kem_enc.restype = ctypes.c_int
        self.lib.PQCLEAN_MLKEM512_CLEAN_crypto_kem_dec.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLKEM512_CLEAN_crypto_kem_dec.restype = ctypes.c_int
    def keypair(self):
        pk = ctypes.create_string_buffer(self.PUBLICKEY_BYTES)
        sk = ctypes.create_string_buffer(self.SECRETKEY_BYTES)
        if self.lib.PQCLEAN_MLKEM512_CLEAN_crypto_kem_keypair(ctypes.cast(pk, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(sk, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Keypair failed")
        return bytes(pk), bytes(sk)
    def encapsulate(self, pk):
        ct = ctypes.create_string_buffer(self.CIPHERTEXT_BYTES)
        ss = ctypes.create_string_buffer(self.SHAREDSECRET_BYTES)
        pk_buf = ctypes.create_string_buffer(pk)
        if self.lib.PQCLEAN_MLKEM512_CLEAN_crypto_kem_enc(ctypes.cast(ct, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(ss, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(pk_buf, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Encapsulation failed")
        return bytes(ct), bytes(ss)
    def decapsulate(self, ct, sk):
        ss = ctypes.create_string_buffer(self.SHAREDSECRET_BYTES)
        ct_buf = ctypes.create_string_buffer(ct)
        sk_buf = ctypes.create_string_buffer(sk)
        if self.lib.PQCLEAN_MLKEM512_CLEAN_crypto_kem_dec(ctypes.cast(ss, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(ct_buf, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(sk_buf, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Decapsulation failed")
        return bytes(ss)

class MLKEM768:
    PUBLICKEY_BYTES = 1184
    SECRETKEY_BYTES = 2400
    CIPHERTEXT_BYTES = 1088
    SHAREDSECRET_BYTES = 32
    def __init__(self, metadata_url, cache_dir):
        self.lib = load_library(metadata_url, cache_dir)
        self.lib.PQCLEAN_MLKEM768_CLEAN_crypto_kem_keypair.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLKEM768_CLEAN_crypto_kem_keypair.restype = ctypes.c_int
        self.lib.PQCLEAN_MLKEM768_CLEAN_crypto_kem_enc.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLKEM768_CLEAN_crypto_kem_enc.restype = ctypes.c_int
        self.lib.PQCLEAN_MLKEM768_CLEAN_crypto_kem_dec.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLKEM768_CLEAN_crypto_kem_dec.restype = ctypes.c_int
    def keypair(self):
        pk = ctypes.create_string_buffer(self.PUBLICKEY_BYTES)
        sk = ctypes.create_string_buffer(self.SECRETKEY_BYTES)
        if self.lib.PQCLEAN_MLKEM768_CLEAN_crypto_kem_keypair(ctypes.cast(pk, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(sk, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Keypair failed")
        return bytes(pk), bytes(sk)
    def encapsulate(self, pk):
        ct = ctypes.create_string_buffer(self.CIPHERTEXT_BYTES)
        ss = ctypes.create_string_buffer(self.SHAREDSECRET_BYTES)
        pk_buf = ctypes.create_string_buffer(pk)
        if self.lib.PQCLEAN_MLKEM768_CLEAN_crypto_kem_enc(ctypes.cast(ct, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(ss, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(pk_buf, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Encapsulation failed")
        return bytes(ct), bytes(ss)
    def decapsulate(self, ct, sk):
        ss = ctypes.create_string_buffer(self.SHAREDSECRET_BYTES)
        ct_buf = ctypes.create_string_buffer(ct)
        sk_buf = ctypes.create_string_buffer(sk)
        if self.lib.PQCLEAN_MLKEM768_CLEAN_crypto_kem_dec(ctypes.cast(ss, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(ct_buf, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(sk_buf, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Decapsulation failed")
        return bytes(ss)

class MLKEM1024:
    PUBLICKEY_BYTES = 1568
    SECRETKEY_BYTES = 3168
    CIPHERTEXT_BYTES = 1568
    SHAREDSECRET_BYTES = 32
    def __init__(self, metadata_url, cache_dir):
        self.lib = load_library(metadata_url, cache_dir)
        self.lib.PQCLEAN_MLKEM1024_CLEAN_crypto_kem_keypair.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLKEM1024_CLEAN_crypto_kem_keypair.restype = ctypes.c_int
        self.lib.PQCLEAN_MLKEM1024_CLEAN_crypto_kem_enc.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLKEM1024_CLEAN_crypto_kem_enc.restype = ctypes.c_int
        self.lib.PQCLEAN_MLKEM1024_CLEAN_crypto_kem_dec.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLKEM1024_CLEAN_crypto_kem_dec.restype = ctypes.c_int
    def keypair(self):
        pk = ctypes.create_string_buffer(self.PUBLICKEY_BYTES)
        sk = ctypes.create_string_buffer(self.SECRETKEY_BYTES)
        if self.lib.PQCLEAN_MLKEM1024_CLEAN_crypto_kem_keypair(ctypes.cast(pk, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(sk, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Keypair failed")
        return bytes(pk), bytes(sk)
    def encapsulate(self, pk):
        ct = ctypes.create_string_buffer(self.CIPHERTEXT_BYTES)
        ss = ctypes.create_string_buffer(self.SHAREDSECRET_BYTES)
        pk_buf = ctypes.create_string_buffer(pk)
        if self.lib.PQCLEAN_MLKEM1024_CLEAN_crypto_kem_enc(ctypes.cast(ct, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(ss, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(pk_buf, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Encapsulation failed")
        return bytes(ct), bytes(ss)
    def decapsulate(self, ct, sk):
        ss = ctypes.create_string_buffer(self.SHAREDSECRET_BYTES)
        ct_buf = ctypes.create_string_buffer(ct)
        sk_buf = ctypes.create_string_buffer(sk)
        if self.lib.PQCLEAN_MLKEM1024_CLEAN_crypto_kem_dec(ctypes.cast(ss, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(ct_buf, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(sk_buf, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Decapsulation failed")
        return bytes(ss)

class MLDSA44:
    PUBLICKEY_BYTES = 1312
    SECRETKEY_BYTES = 2560
    SIGNATURE_BYTES = 2420
    def __init__(self, metadata_url, cache_dir):
        self.lib = load_library(metadata_url, cache_dir)
        self.lib.PQCLEAN_MLDSA44_CLEAN_crypto_sign_keypair.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLDSA44_CLEAN_crypto_sign_keypair.restype = ctypes.c_int
        self.lib.PQCLEAN_MLDSA44_CLEAN_crypto_sign.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ulonglong), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_ulonglong, ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLDSA44_CLEAN_crypto_sign.restype = ctypes.c_int
        self.lib.PQCLEAN_MLDSA44_CLEAN_crypto_sign_open.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ulonglong), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_ulonglong, ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLDSA44_CLEAN_crypto_sign_open.restype = ctypes.c_int
    def keypair(self):
        pk = ctypes.create_string_buffer(self.PUBLICKEY_BYTES)
        sk = ctypes.create_string_buffer(self.SECRETKEY_BYTES)
        if self.lib.PQCLEAN_MLDSA44_CLEAN_crypto_sign_keypair(ctypes.cast(pk, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(sk, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Keypair failed")
        return bytes(pk), bytes(sk)
    def sign(self, message, sk):
        sm = ctypes.create_string_buffer(len(message) + self.SIGNATURE_BYTES)
        smlen = ctypes.c_ulonglong()
        msg_buf = ctypes.create_string_buffer(message)
        sk_buf = ctypes.create_string_buffer(sk)
        if self.lib.PQCLEAN_MLDSA44_CLEAN_crypto_sign(ctypes.cast(sm, ctypes.POINTER(ctypes.c_ubyte)), ctypes.byref(smlen), ctypes.cast(msg_buf, ctypes.POINTER(ctypes.c_ubyte)), len(message), ctypes.cast(sk_buf, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Signing failed")
        return bytes(sm[:smlen.value])
    def verify(self, signed_message, pk):
        m = ctypes.create_string_buffer(len(signed_message))
        mlen = ctypes.c_ulonglong()
        sm_buf = ctypes.create_string_buffer(signed_message)
        pk_buf = ctypes.create_string_buffer(pk)
        if self.lib.PQCLEAN_MLDSA44_CLEAN_crypto_sign_open(ctypes.cast(m, ctypes.POINTER(ctypes.c_ubyte)), ctypes.byref(mlen), ctypes.cast(sm_buf, ctypes.POINTER(ctypes.c_ubyte)), len(signed_message), ctypes.cast(pk_buf, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Verification failed")
        return bytes(m[:mlen.value])

class MLDSA65:
    PUBLICKEY_BYTES = 1952
    SECRETKEY_BYTES = 4032
    SIGNATURE_BYTES = 3309
    def __init__(self, metadata_url, cache_dir):
        self.lib = load_library(metadata_url, cache_dir)
        self.lib.PQCLEAN_MLDSA65_CLEAN_crypto_sign_keypair.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLDSA65_CLEAN_crypto_sign_keypair.restype = ctypes.c_int
        self.lib.PQCLEAN_MLDSA65_CLEAN_crypto_sign.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ulonglong), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_ulonglong, ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLDSA65_CLEAN_crypto_sign.restype = ctypes.c_int
        self.lib.PQCLEAN_MLDSA65_CLEAN_crypto_sign_open.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ulonglong), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_ulonglong, ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLDSA65_CLEAN_crypto_sign_open.restype = ctypes.c_int
    def keypair(self):
        pk = ctypes.create_string_buffer(self.PUBLICKEY_BYTES)
        sk = ctypes.create_string_buffer(self.SECRETKEY_BYTES)
        if self.lib.PQCLEAN_MLDSA65_CLEAN_crypto_sign_keypair(ctypes.cast(pk, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(sk, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Keypair failed")
        return bytes(pk), bytes(sk)
    def sign(self, message, sk):
        sm = ctypes.create_string_buffer(len(message) + self.SIGNATURE_BYTES)
        smlen = ctypes.c_ulonglong()
        msg_buf = ctypes.create_string_buffer(message)
        sk_buf = ctypes.create_string_buffer(sk)
        if self.lib.PQCLEAN_MLDSA65_CLEAN_crypto_sign(ctypes.cast(sm, ctypes.POINTER(ctypes.c_ubyte)), ctypes.byref(smlen), ctypes.cast(msg_buf, ctypes.POINTER(ctypes.c_ubyte)), len(message), ctypes.cast(sk_buf, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Signing failed")
        return bytes(sm[:smlen.value])
    def verify(self, signed_message, pk):
        m = ctypes.create_string_buffer(len(signed_message))
        mlen = ctypes.c_ulonglong()
        sm_buf = ctypes.create_string_buffer(signed_message)
        pk_buf = ctypes.create_string_buffer(pk)
        if self.lib.PQCLEAN_MLDSA65_CLEAN_crypto_sign_open(ctypes.cast(m, ctypes.POINTER(ctypes.c_ubyte)), ctypes.byref(mlen), ctypes.cast(sm_buf, ctypes.POINTER(ctypes.c_ubyte)), len(signed_message), ctypes.cast(pk_buf, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Verification failed")
        return bytes(m[:mlen.value])

class MLDSA87:
    PUBLICKEY_BYTES = 2592
    SECRETKEY_BYTES = 4896
    SIGNATURE_BYTES = 4627
    def __init__(self, metadata_url, cache_dir):
        self.lib = load_library(metadata_url, cache_dir)
        self.lib.PQCLEAN_MLDSA87_CLEAN_crypto_sign_keypair.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLDSA87_CLEAN_crypto_sign_keypair.restype = ctypes.c_int
        self.lib.PQCLEAN_MLDSA87_CLEAN_crypto_sign.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ulonglong), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_ulonglong, ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLDSA87_CLEAN_crypto_sign.restype = ctypes.c_int
        self.lib.PQCLEAN_MLDSA87_CLEAN_crypto_sign_open.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ulonglong), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_ulonglong, ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_MLDSA87_CLEAN_crypto_sign_open.restype = ctypes.c_int
    def keypair(self):
        pk = ctypes.create_string_buffer(self.PUBLICKEY_BYTES)
        sk = ctypes.create_string_buffer(self.SECRETKEY_BYTES)
        if self.lib.PQCLEAN_MLDSA87_CLEAN_crypto_sign_keypair(ctypes.cast(pk, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(sk, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Keypair failed")
        return bytes(pk), bytes(sk)
    def sign(self, message, sk):
        sm = ctypes.create_string_buffer(len(message) + self.SIGNATURE_BYTES)
        smlen = ctypes.c_ulonglong()
        msg_buf = ctypes.create_string_buffer(message)
        sk_buf = ctypes.create_string_buffer(sk)
        if self.lib.PQCLEAN_MLDSA87_CLEAN_crypto_sign(ctypes.cast(sm, ctypes.POINTER(ctypes.c_ubyte)), ctypes.byref(smlen), ctypes.cast(msg_buf, ctypes.POINTER(ctypes.c_ubyte)), len(message), ctypes.cast(sk_buf, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Signing failed")
        return bytes(sm[:smlen.value])
    def verify(self, signed_message, pk):
        m = ctypes.create_string_buffer(len(signed_message))
        mlen = ctypes.c_ulonglong()
        sm_buf = ctypes.create_string_buffer(signed_message)
        pk_buf = ctypes.create_string_buffer(pk)
        if self.lib.PQCLEAN_MLDSA87_CLEAN_crypto_sign_open(ctypes.cast(m, ctypes.POINTER(ctypes.c_ubyte)), ctypes.byref(mlen), ctypes.cast(sm_buf, ctypes.POINTER(ctypes.c_ubyte)), len(signed_message), ctypes.cast(pk_buf, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Verification failed")
        return bytes(m[:mlen.value])

class Falcon512:
    PUBLICKEY_BYTES = 897
    SECRETKEY_BYTES = 1281
    SIGNATURE_BYTES = 752
    def __init__(self, metadata_url, cache_dir):
        self.lib = load_library(metadata_url, cache_dir)
        self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair.restype = ctypes.c_int
        self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ulonglong), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_ulonglong, ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign.restype = ctypes.c_int
        self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_open.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ulonglong), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_ulonglong, ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_open.restype = ctypes.c_int
    def keypair(self):
        pk = ctypes.create_string_buffer(self.PUBLICKEY_BYTES)
        sk = ctypes.create_string_buffer(self.SECRETKEY_BYTES)
        if self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair(ctypes.cast(pk, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(sk, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Keypair failed")
        return bytes(pk), bytes(sk)
    def sign(self, message, sk):
        sm = ctypes.create_string_buffer(len(message) + self.SIGNATURE_BYTES)
        smlen = ctypes.c_ulonglong()
        msg_buf = ctypes.create_string_buffer(message)
        sk_buf = ctypes.create_string_buffer(sk)
        if self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign(ctypes.cast(sm, ctypes.POINTER(ctypes.c_ubyte)), ctypes.byref(smlen), ctypes.cast(msg_buf, ctypes.POINTER(ctypes.c_ubyte)), len(message), ctypes.cast(sk_buf, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Signing failed")
        return bytes(sm[:smlen.value])
    def verify(self, signed_message, pk):
        m = ctypes.create_string_buffer(len(signed_message))
        mlen = ctypes.c_ulonglong()
        sm_buf = ctypes.create_string_buffer(signed_message)
        pk_buf = ctypes.create_string_buffer(pk)
        if self.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_open(ctypes.cast(m, ctypes.POINTER(ctypes.c_ubyte)), ctypes.byref(mlen), ctypes.cast(sm_buf, ctypes.POINTER(ctypes.c_ubyte)), len(signed_message), ctypes.cast(pk_buf, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Verification failed")
        return bytes(m[:mlen.value])

class Falcon1024:
    PUBLICKEY_BYTES = 1793
    SECRETKEY_BYTES = 2305
    SIGNATURE_BYTES = 1462
    def __init__(self, metadata_url, cache_dir):
        self.lib = load_library(metadata_url, cache_dir)
        self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_keypair.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_keypair.restype = ctypes.c_int
        self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ulonglong), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_ulonglong, ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign.restype = ctypes.c_int
        self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_open.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ulonglong), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_ulonglong, ctypes.POINTER(ctypes.c_ubyte)]
        self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_open.restype = ctypes.c_int
    def keypair(self):
        pk = ctypes.create_string_buffer(self.PUBLICKEY_BYTES)
        sk = ctypes.create_string_buffer(self.SECRETKEY_BYTES)
        if self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_keypair(ctypes.cast(pk, ctypes.POINTER(ctypes.c_ubyte)), ctypes.cast(sk, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Keypair failed")
        return bytes(pk), bytes(sk)
    def sign(self, message, sk):
        sm = ctypes.create_string_buffer(len(message) + self.SIGNATURE_BYTES)
        smlen = ctypes.c_ulonglong()
        msg_buf = ctypes.create_string_buffer(message)
        sk_buf = ctypes.create_string_buffer(sk)
        if self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign(ctypes.cast(sm, ctypes.POINTER(ctypes.c_ubyte)), ctypes.byref(smlen), ctypes.cast(msg_buf, ctypes.POINTER(ctypes.c_ubyte)), len(message), ctypes.cast(sk_buf, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Signing failed")
        return bytes(sm[:smlen.value])
    def verify(self, signed_message, pk):
        m = ctypes.create_string_buffer(len(signed_message))
        mlen = ctypes.c_ulonglong()
        sm_buf = ctypes.create_string_buffer(signed_message)
        pk_buf = ctypes.create_string_buffer(pk)
        if self.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_open(ctypes.cast(m, ctypes.POINTER(ctypes.c_ubyte)), ctypes.byref(mlen), ctypes.cast(sm_buf, ctypes.POINTER(ctypes.c_ubyte)), len(signed_message), ctypes.cast(pk_buf, ctypes.POINTER(ctypes.c_ubyte))) != 0:
            raise Exception("Verification failed")
        return bytes(m[:mlen.value])
