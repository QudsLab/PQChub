# Supported Algorithms in PQChub

This document lists all post-quantum cryptography algorithms supported by PQChub, including their security levels, key sizes, and usage notes.

## Table of Contents
- [Key Encapsulation Mechanisms (KEMs)](#key-encapsulation-mechanisms-kems)
- [Digital Signature Algorithms](#digital-signature-algorithms)
- [Algorithm Comparison Table](#algorithm-comparison-table)
- [Algorithm Selection Guide](#algorithm-selection-guide)
- [References](#references)

---

## Key Encapsulation Mechanisms (KEMs)

### Kyber
- **Kyber512**
  - Security: 128-bit
  - Public key: 800 bytes
  - Secret key: 1632 bytes
  - Ciphertext: 768 bytes
  - Shared secret: 32 bytes
- **Kyber768**
  - Security: 192-bit
  - Public key: 1184 bytes
  - Secret key: 2400 bytes
  - Ciphertext: 1088 bytes
  - Shared secret: 32 bytes
- **Kyber1024**
  - Security: 256-bit
  - Public key: 1568 bytes
  - Secret key: 3168 bytes
  - Ciphertext: 1568 bytes
  - Shared secret: 32 bytes

## Digital Signature Algorithms

### Dilithium
- **Dilithium2**
  - Security: 128-bit
  - Public key: 1312 bytes
  - Secret key: 2528 bytes
  - Signature: 2420 bytes
- **Dilithium3**
  - Security: 192-bit
  - Public key: 1952 bytes
  - Secret key: 4000 bytes
  - Signature: 3293 bytes
- **Dilithium5**
  - Security: 256-bit
  - Public key: 2592 bytes
  - Secret key: 4864 bytes
  - Signature: 4595 bytes

### Falcon
- **Falcon512**
  - Security: 128-bit
  - Public key: 897 bytes
  - Secret key: 1281 bytes
  - Signature: ~666 bytes (variable)
- **Falcon1024**
  - Security: 256-bit
  - Public key: 1793 bytes
  - Secret key: 2305 bytes
  - Signature: ~1280 bytes (variable)

---

## Algorithm Comparison Table

| Algorithm      | Type      | Security | Public Key | Secret Key | Ciphertext/Signature | Shared Secret |
|---------------|-----------|----------|------------|------------|---------------------|--------------|
| Kyber512      | KEM       | 128-bit  | 800 B      | 1632 B     | 768 B               | 32 B         |
| Kyber768      | KEM       | 192-bit  | 1184 B     | 2400 B     | 1088 B              | 32 B         |
| Kyber1024     | KEM       | 256-bit  | 1568 B     | 3168 B     | 1568 B              | 32 B         |
| Dilithium2    | Signature | 128-bit  | 1312 B     | 2528 B     | 2420 B               | N/A          |
| Dilithium3    | Signature | 192-bit  | 1952 B     | 4000 B     | 3293 B               | N/A          |
| Dilithium5    | Signature | 256-bit  | 2592 B     | 4864 B     | 4595 B               | N/A          |
| Falcon512     | Signature | 128-bit  | 897 B      | 1281 B     | ~666 B               | N/A          |
| Falcon1024    | Signature | 256-bit  | 1793 B     | 2305 B     | ~1280 B              | N/A          |

---

## Algorithm Selection Guide

- **Kyber**: Recommended for key exchange and hybrid encryption. Fast, small keys, and NIST standard.
- **Dilithium**: Recommended for digital signatures. Robust, efficient, and NIST standard.
- **Falcon**: Recommended for applications needing very small signatures. More complex implementation, but efficient.

### Security Levels
- **128-bit**: Suitable for most applications, equivalent to AES-128.
- **192-bit**: For higher security requirements, equivalent to AES-192.
- **256-bit**: For maximum security, equivalent to AES-256.

### Usage Notes
- All algorithms are implemented using PQClean upstream source.
- Binaries are pre-compiled for all major platforms.
- Wrappers provide safe, idiomatic APIs for each language.
- See [API.md](./API.md) for usage examples and function signatures.

---

## References
- [NIST Post-Quantum Cryptography Project](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [PQClean Project](https://github.com/PQClean/PQClean)
- [Kyber Specification](https://pq-crystals.org/kyber/)
- [Dilithium Specification](https://pq-crystals.org/dilithium/)
- [Falcon Specification](https://falcon-sign.info/)

---

For questions or suggestions, please open an issue or discussion on GitHub.