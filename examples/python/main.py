from pathlib import Path
from termcolor import colored
from utils import MLKEM512, MLKEM768, MLKEM1024, MLDSA44, MLDSA65, MLDSA87, Falcon512, Falcon1024

METADATA_URL = "https://github.com/QudsLab/PQChub/raw/refs/heads/main/bins/binaries.json"
CACHE_DIR = Path("download_cache")
EXP_DIR = Path("test_output")

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