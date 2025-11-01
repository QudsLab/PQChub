package pqc

/*
#cgo CFLAGS: -I.
#cgo LDFLAGS: -L. -lpqc

extern int PQCLEAN_KYBER512_CLEAN_crypto_kem_keypair(unsigned char *pk, unsigned char *sk);
extern int PQCLEAN_KYBER512_CLEAN_crypto_kem_enc(unsigned char *ct, unsigned char *ss, const unsigned char *pk);
extern int PQCLEAN_KYBER512_CLEAN_crypto_kem_dec(unsigned char *ss, const unsigned char *ct, const unsigned char *sk);

extern int PQCLEAN_KYBER768_CLEAN_crypto_kem_keypair(unsigned char *pk, unsigned char *sk);
extern int PQCLEAN_KYBER768_CLEAN_crypto_kem_enc(unsigned char *ct, unsigned char *ss, const unsigned char *pk);
extern int PQCLEAN_KYBER768_CLEAN_crypto_kem_dec(unsigned char *ss, const unsigned char *ct, const unsigned char *sk);

extern int PQCLEAN_KYBER1024_CLEAN_crypto_kem_keypair(unsigned char *pk, unsigned char *sk);
extern int PQCLEAN_KYBER1024_CLEAN_crypto_kem_enc(unsigned char *ct, unsigned char *ss, const unsigned char *pk);
extern int PQCLEAN_KYBER1024_CLEAN_crypto_kem_dec(unsigned char *ss, const unsigned char *ct, const unsigned char *sk);
*/
import "C"

import (
	"fmt"
	"unsafe"
)

// Kyber512 provides Kyber-512 key encapsulation mechanism
type Kyber512 struct{}

// NewKyber512 creates a new Kyber512 instance
func NewKyber512() *Kyber512 {
	return &Kyber512{}
}

// Keypair generates a Kyber512 key pair
func (k *Kyber512) Keypair() (publicKey, secretKey []byte, err error) {
	if libraryPath == "" {
		return nil, nil, ErrLibraryNotFound
	}

	publicKey = make([]byte, Kyber512PublicKeyBytes)
	secretKey = make([]byte, Kyber512SecretKeyBytes)

	result := C.PQCLEAN_KYBER512_CLEAN_crypto_kem_keypair(
		(*C.uchar)(unsafe.Pointer(&publicKey[0])),
		(*C.uchar)(unsafe.Pointer(&secretKey[0])),
	)

	if result != 0 {
		return nil, nil, fmt.Errorf("%w: code %d", ErrKeyGeneration, result)
	}

	return publicKey, secretKey, nil
}

// Encapsulate encapsulates a shared secret using the public key
func (k *Kyber512) Encapsulate(publicKey []byte) (ciphertext, sharedSecret []byte, err error) {
	if libraryPath == "" {
		return nil, nil, ErrLibraryNotFound
	}

	if err := validateKeyLength(publicKey, Kyber512PublicKeyBytes, "public key"); err != nil {
		return nil, nil, err
	}

	ciphertext = make([]byte, Kyber512CiphertextBytes)
	sharedSecret = make([]byte, Kyber512SharedSecretBytes)

	result := C.PQCLEAN_KYBER512_CLEAN_crypto_kem_enc(
		(*C.uchar)(unsafe.Pointer(&ciphertext[0])),
		(*C.uchar)(unsafe.Pointer(&sharedSecret[0])),
		(*C.uchar)(unsafe.Pointer(&publicKey[0])),
	)

	if result != 0 {
		return nil, nil, fmt.Errorf("%w: code %d", ErrEncapsulation, result)
	}

	return ciphertext, sharedSecret, nil
}

// Decapsulate decapsulates the shared secret using the secret key
func (k *Kyber512) Decapsulate(ciphertext, secretKey []byte) (sharedSecret []byte, err error) {
	if libraryPath == "" {
		return nil, ErrLibraryNotFound
	}

	if err := validateKeyLength(ciphertext, Kyber512CiphertextBytes, "ciphertext"); err != nil {
		return nil, err
	}
	if err := validateKeyLength(secretKey, Kyber512SecretKeyBytes, "secret key"); err != nil {
		return nil, err
	}

	sharedSecret = make([]byte, Kyber512SharedSecretBytes)

	result := C.PQCLEAN_KYBER512_CLEAN_crypto_kem_dec(
		(*C.uchar)(unsafe.Pointer(&sharedSecret[0])),
		(*C.uchar)(unsafe.Pointer(&ciphertext[0])),
		(*C.uchar)(unsafe.Pointer(&secretKey[0])),
	)

	if result != 0 {
		return nil, fmt.Errorf("%w: code %d", ErrDecapsulation, result)
	}

	return sharedSecret, nil
}

// Kyber768 provides Kyber-768 key encapsulation mechanism
type Kyber768 struct{}

// NewKyber768 creates a new Kyber768 instance
func NewKyber768() *Kyber768 {
	return &Kyber768{}
}

// Keypair generates a Kyber768 key pair
func (k *Kyber768) Keypair() (publicKey, secretKey []byte, err error) {
	if libraryPath == "" {
		return nil, nil, ErrLibraryNotFound
	}

	publicKey = make([]byte, Kyber768PublicKeyBytes)
	secretKey = make([]byte, Kyber768SecretKeyBytes)

	result := C.PQCLEAN_KYBER768_CLEAN_crypto_kem_keypair(
		(*C.uchar)(unsafe.Pointer(&publicKey[0])),
		(*C.uchar)(unsafe.Pointer(&secretKey[0])),
	)

	if result != 0 {
		return nil, nil, fmt.Errorf("%w: code %d", ErrKeyGeneration, result)
	}

	return publicKey, secretKey, nil
}

// Encapsulate encapsulates a shared secret using the public key
func (k *Kyber768) Encapsulate(publicKey []byte) (ciphertext, sharedSecret []byte, err error) {
	if libraryPath == "" {
		return nil, nil, ErrLibraryNotFound
	}

	if err := validateKeyLength(publicKey, Kyber768PublicKeyBytes, "public key"); err != nil {
		return nil, nil, err
	}

	ciphertext = make([]byte, Kyber768CiphertextBytes)
	sharedSecret = make([]byte, Kyber768SharedSecretBytes)

	result := C.PQCLEAN_KYBER768_CLEAN_crypto_kem_enc(
		(*C.uchar)(unsafe.Pointer(&ciphertext[0])),
		(*C.uchar)(unsafe.Pointer(&sharedSecret[0])),
		(*C.uchar)(unsafe.Pointer(&publicKey[0])),
	)

	if result != 0 {
		return nil, nil, fmt.Errorf("%w: code %d", ErrEncapsulation, result)
	}

	return ciphertext, sharedSecret, nil
}

// Decapsulate decapsulates the shared secret using the secret key
func (k *Kyber768) Decapsulate(ciphertext, secretKey []byte) (sharedSecret []byte, err error) {
	if libraryPath == "" {
		return nil, ErrLibraryNotFound
	}

	if err := validateKeyLength(ciphertext, Kyber768CiphertextBytes, "ciphertext"); err != nil {
		return nil, err
	}
	if err := validateKeyLength(secretKey, Kyber768SecretKeyBytes, "secret key"); err != nil {
		return nil, err
	}

	sharedSecret = make([]byte, Kyber768SharedSecretBytes)

	result := C.PQCLEAN_KYBER768_CLEAN_crypto_kem_dec(
		(*C.uchar)(unsafe.Pointer(&sharedSecret[0])),
		(*C.uchar)(unsafe.Pointer(&ciphertext[0])),
		(*C.uchar)(unsafe.Pointer(&secretKey[0])),
	)

	if result != 0 {
		return nil, fmt.Errorf("%w: code %d", ErrDecapsulation, result)
	}

	return sharedSecret, nil
}

// Kyber1024 provides Kyber-1024 key encapsulation mechanism
type Kyber1024 struct{}

// NewKyber1024 creates a new Kyber1024 instance
func NewKyber1024() *Kyber1024 {
	return &Kyber1024{}
}

// Keypair generates a Kyber1024 key pair
func (k *Kyber1024) Keypair() (publicKey, secretKey []byte, err error) {
	if libraryPath == "" {
		return nil, nil, ErrLibraryNotFound
	}

	publicKey = make([]byte, Kyber1024PublicKeyBytes)
	secretKey = make([]byte, Kyber1024SecretKeyBytes)

	result := C.PQCLEAN_KYBER1024_CLEAN_crypto_kem_keypair(
		(*C.uchar)(unsafe.Pointer(&publicKey[0])),
		(*C.uchar)(unsafe.Pointer(&secretKey[0])),
	)

	if result != 0 {
		return nil, nil, fmt.Errorf("%w: code %d", ErrKeyGeneration, result)
	}

	return publicKey, secretKey, nil
}

// Encapsulate encapsulates a shared secret using the public key
func (k *Kyber1024) Encapsulate(publicKey []byte) (ciphertext, sharedSecret []byte, err error) {
	if libraryPath == "" {
		return nil, nil, ErrLibraryNotFound
	}

	if err := validateKeyLength(publicKey, Kyber1024PublicKeyBytes, "public key"); err != nil {
		return nil, nil, err
	}

	ciphertext = make([]byte, Kyber1024CiphertextBytes)
	sharedSecret = make([]byte, Kyber1024SharedSecretBytes)

	result := C.PQCLEAN_KYBER1024_CLEAN_crypto_kem_enc(
		(*C.uchar)(unsafe.Pointer(&ciphertext[0])),
		(*C.uchar)(unsafe.Pointer(&sharedSecret[0])),
		(*C.uchar)(unsafe.Pointer(&publicKey[0])),
	)

	if result != 0 {
		return nil, nil, fmt.Errorf("%w: code %d", ErrEncapsulation, result)
	}

	return ciphertext, sharedSecret, nil
}

// Decapsulate decapsulates the shared secret using the secret key
func (k *Kyber1024) Decapsulate(ciphertext, secretKey []byte) (sharedSecret []byte, err error) {
	if libraryPath == "" {
		return nil, ErrLibraryNotFound
	}

	if err := validateKeyLength(ciphertext, Kyber1024CiphertextBytes, "ciphertext"); err != nil {
		return nil, err
	}
	if err := validateKeyLength(secretKey, Kyber1024SecretKeyBytes, "secret key"); err != nil {
		return nil, err
	}

	sharedSecret = make([]byte, Kyber1024SharedSecretBytes)

	result := C.PQCLEAN_KYBER1024_CLEAN_crypto_kem_dec(
		(*C.uchar)(unsafe.Pointer(&sharedSecret[0])),
		(*C.uchar)(unsafe.Pointer(&ciphertext[0])),
		(*C.uchar)(unsafe.Pointer(&secretKey[0])),
	)

	if result != 0 {
		return nil, fmt.Errorf("%w: code %d", ErrDecapsulation, result)
	}

	return sharedSecret, nil
}

// NewKyber creates a new Kyber768 instance (default)
func NewKyber() *Kyber768 {
	return NewKyber768()
}