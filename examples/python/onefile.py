import json
import ctypes
import platform
import urllib.request
from pathlib import Path
from termcolor import colored
from .bin import get_binary_path

METADATA_URL = "https://github.com/QudsLab/PQChub/raw/refs/heads/main/bins/binaries.json"
CACHE_DIR = Path("download_cache")
EXP_DIR = Path("test_output")

## ---------------------------------------------------------------------------------------------------------------------------------------------------------

def detect_platform() -> (bool, str):
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        if "64" in machine or "amd64" in machine:
            return (True, "windows-x64")
        else:
            return (True, "windows-x86")
    elif system == "darwin":
        if "arm" in machine or "aarch64" in machine:
            return (True, "macos-arm64")
        else:
            return (True, "macos-x86_64")
    elif system == "linux":
        if "aarch64" in machine or "arm64" in machine:
            return (True, "linux-aarch64")
        else:
            return (True, "linux-x86_64")
    else:
        raise (False, f"Unsupported platform: {system} {machine}")
def download_file(url, dest_path) -> (bool, str):
    try:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, dest_path)
        return (True, "Download successful")
    except Exception as e:
        return (False, str(e))
def get_binary_path(metadata_url, cache_dir) -> (bool, bool, str):
    try:
        platform_status, platform_id = detect_platform()
        if platform_status:
            with urllib.request.urlopen(metadata_url) as response:
                metadata = json.loads(response.read().decode('utf-8'))
            if platform_id in metadata['binaries']:
                binary_info = metadata['binaries'][platform_id]
                binary_url = binary_info['url']
                binary_filename = binary_info['filename']
                cached_path = cache_dir / platform_id / binary_filename
                if cached_path.exists():
                    return (True, False, str(cached_path))
                else:
                    download_file(binary_url, cached_path)
                    return (True, True, str(cached_path))
    except Exception as e:
        return (False, False, str(e))
    return (False, False, "Unsupported platform")

## ---------------------------------------------------------------------------------------------------------------------------------------------------------

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

## ---------------------------------------------------------------------------------------------------------------------------------------------------------
##                           MAIN TESTING LOGIC
## ---------------------------------------------------------------------------------------------------------------------------------------------------------

print(colored("="*60, "cyan"))
print(colored(f"PQC Algorithm Binary path is {CACHE_DIR}", "cyan"))
print(colored("="*60, "cyan"))

def write_file(name, contentType, content):
    exp_path = EXP_DIR / name
    exp_bin_path = EXP_DIR / name / 'bin'
    exp_path.mkdir(parents=True, exist_ok=True)
    exp_bin_path.mkdir(parents=True, exist_ok=True)
    
    # Save binary version if content is bytes
    if isinstance(content, bytes):
        bin_file = exp_bin_path / f"{contentType}.bin"
        with open(bin_file, "wb") as f:
            f.write(content)
        # Save hex version in text file
        txt_file = exp_path / f"{contentType}.txt"
        hex_content = content.hex()
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(hex_content)
    # Save only text version if content is string
    elif isinstance(content, str):
        txt_file = exp_path / f"{contentType}.txt"
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(content)

def test_kem(name, kem_class, secret_message):
    msg_file       = "message"
    pk_file        = "public_key"
    sk_file        = "secret_key"
    ct_file        = "ciphertext"
    ss1_file       = "shared_secret_1"
    ss2_file       = "shared_secret_2"
    encrypted_file = "encrypted_message"
    decrypted_file = "decrypted_message"
    
    write_file(name, "message", secret_message.decode())
    print(colored(f"Starting test of {name} algorithm, creating pk,sk", "blue"))
    kem = kem_class(METADATA_URL, CACHE_DIR)
    pk, sk = kem.keypair()
    write_file(name, "public_key", pk)
    write_file(name, "secret_key", sk)
    ct, ss1 = kem.encapsulate(pk)
    write_file(name, "ciphertext", ct)
    write_file(name, "shared_secret_1", ss1)
    print(colored(f"pk length: {len(pk)}, sk length: {len(sk)}, encrypted msg length: {len(ct)}", "yellow"))
    ss2 = kem.decapsulate(ct, sk)
    write_file(name, "shared_secret_2", ss2)
    result = "SUCCESS" if ss1 == ss2 else "FAILED"
    print(colored(f"Decryption result: {result} (shared secret matched: {ss1 == ss2})", "green"))
    print(colored(f"Test of {name} algorithm ended\n", "white"))

def test_signature(name, sig_class, secret_message):
    # create output directory for this algorithm
    exp_path = EXP_DIR / name
    exp_path.mkdir(parents=True, exist_ok=True)
    msg_file       = "message"
    pk_file        = "public_key"
    sk_file        = "secret_key"
    encrypted_file = "encrypted_message"
    decrypted_file = "decrypted_message"
    
    write_file(name, "message", secret_message.decode())
    
    try:
        print(colored(f"Starting test of {name} algorithm, creating pk,sk", "blue"))
        sig = sig_class(METADATA_URL, CACHE_DIR)
        pk, sk = sig.keypair()
        write_file(name, "public_key", pk)
        write_file(name, "secret_key", sk)
        signed = sig.sign(secret_message, sk)
        write_file(name, "encrypted_message", signed)
        print(colored(f"pk length: {len(pk)}, sk length: {len(sk)}, signed msg length: {len(signed)}", "yellow"))
        verified = sig.verify(signed, pk)
        write_file(name, "decrypted_message", verified)
        result = "SUCCESS" if verified == secret_message else "FAILED"
        print(colored(f"Verification result: {result} (message matched: {verified == secret_message})", "green"))
        print(colored(f"Test of {name} algorithm ended\n", "white"))
    except Exception as e:
        print(colored(f"pk length: N/A, sk length: N/A, signed msg length: N/A", "yellow"))
        print(colored(f"Verification result: FAILED - {str(e)}", "red"))
        print(colored(f"Test of {name} algorithm ended\n", "white"))

secret_message = b"This is a secret message for PQC testing!"
print(colored(f"Secret message: {secret_message.decode()}", "red"))
print()

test_kem("ML-KEM-512",          MLKEM512, secret_message)
test_kem("ML-KEM-768",          MLKEM768, secret_message)
test_kem("ML-KEM-1024",        MLKEM1024, secret_message)
test_signature("ML-DSA-44",      MLDSA44, secret_message)
test_signature("ML-DSA-65",      MLDSA65, secret_message)
test_signature("ML-DSA-87",      MLDSA87, secret_message)
test_signature("Falcon-512",   Falcon512, secret_message)
test_signature("Falcon-1024", Falcon1024, secret_message)

print(colored("\n" + "="*60, "cyan"))
print(colored("All 8 PQC algorithms tested!", "green"))
print(colored("="*60, "cyan"))