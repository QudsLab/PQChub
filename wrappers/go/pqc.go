// Package pqc provides Go bindings for PQChub post-quantum cryptography algorithms.
//
// This package provides access to post-quantum cryptography algorithms from the
// PQClean project, including Key Encapsulation Mechanisms (KEM) and Digital
// Signature algorithms.
//
// Key Encapsulation Mechanisms (KEM):
//   - Kyber512, Kyber768, Kyber1024
//
// Digital Signatures:
//   - Dilithium2, Dilithium3, Dilithium5
//
// Example usage:
//
//	import "github.com/QudsLab/PQChub/wrappers/go/pqc"
//
//	// Key Encapsulation
//	kyber := pqc.NewKyber512()
//	publicKey, secretKey, err := kyber.Keypair()
//	if err != nil {
//	    log.Fatal(err)
//	}
//	ciphertext, sharedSecret, err := kyber.Encapsulate(publicKey)
//	if err != nil {
//	    log.Fatal(err)
//	}
//	decryptedSecret, err := kyber.Decapsulate(ciphertext, secretKey)
//	if err != nil {
//	    log.Fatal(err)
//	}
//	if !bytes.Equal(sharedSecret, decryptedSecret) {
//	    log.Fatal("Shared secrets do not match")
//	}
//
//	// Digital Signatures
//	dilithium := pqc.NewDilithium2()
//	pk, sk, err := dilithium.Keypair()
//	if err != nil {
//	    log.Fatal(err)
//	}
//	message := []byte("Hello, post-quantum world!")
//	signature, err := dilithium.Sign(message, sk)
//	if err != nil {
//	    log.Fatal(err)
//	}
//	valid, err := dilithium.Verify(message, signature, pk)
//	if err != nil {
//	    log.Fatal(err)
//	}
//	if !valid {
//	    log.Fatal("Signature verification failed")
//	}
package pqc

/*
#cgo CFLAGS: -I.
#cgo LDFLAGS: -L. -lpqc

// Forward declarations for PQC functions
extern int PQCLEAN_KYBER512_CLEAN_crypto_kem_keypair(unsigned char *pk, unsigned char *sk);
extern int PQCLEAN_KYBER512_CLEAN_crypto_kem_enc(unsigned char *ct, unsigned char *ss, const unsigned char *pk);
extern int PQCLEAN_KYBER512_CLEAN_crypto_kem_dec(unsigned char *ss, const unsigned char *ct, const unsigned char *sk);

extern int PQCLEAN_KYBER768_CLEAN_crypto_kem_keypair(unsigned char *pk, unsigned char *sk);
extern int PQCLEAN_KYBER768_CLEAN_crypto_kem_enc(unsigned char *ct, unsigned char *ss, const unsigned char *pk);
extern int PQCLEAN_KYBER768_CLEAN_crypto_kem_dec(unsigned char *ss, const unsigned char *ct, const unsigned char *sk);

extern int PQCLEAN_KYBER1024_CLEAN_crypto_kem_keypair(unsigned char *pk, unsigned char *sk);
extern int PQCLEAN_KYBER1024_CLEAN_crypto_kem_enc(unsigned char *ct, unsigned char *ss, const unsigned char *pk);
extern int PQCLEAN_KYBER1024_CLEAN_crypto_kem_dec(unsigned char *ss, const unsigned char *ct, const unsigned char *sk);

extern int PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_keypair(unsigned char *pk, unsigned char *sk);
extern int PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_signature(unsigned char *sig, size_t *siglen, const unsigned char *m, size_t mlen, const unsigned char *sk);
extern int PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_verify(const unsigned char *sig, size_t siglen, const unsigned char *m, size_t mlen, const unsigned char *pk);

extern int PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_keypair(unsigned char *pk, unsigned char *sk);
extern int PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_signature(unsigned char *sig, size_t *siglen, const unsigned char *m, size_t mlen, const unsigned char *sk);
extern int PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_verify(const unsigned char *sig, size_t siglen, const unsigned char *m, size_t mlen, const unsigned char *pk);

extern int PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_keypair(unsigned char *pk, unsigned char *sk);
extern int PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_signature(unsigned char *sig, size_t *siglen, const unsigned char *m, size_t mlen, const unsigned char *sk);
extern int PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_verify(const unsigned char *sig, size_t siglen, const unsigned char *m, size_t mlen, const unsigned char *pk);

extern const char* pqchub_get_version(void);
extern const char* pqchub_get_algorithms(void);
*/
import "C"

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"unsafe"
)

// Version information
const Version = "1.0.0"

// Common errors
var (
	ErrKeyGeneration   = errors.New("key generation failed")
	ErrEncapsulation   = errors.New("encapsulation failed")
	ErrDecapsulation   = errors.New("decapsulation failed")
	ErrSigning         = errors.New("signing failed")
	ErrVerification    = errors.New("verification failed")
	ErrInvalidKeySize  = errors.New("invalid key size")
	ErrLibraryNotFound = errors.New("PQC library not found")
)

// Platform information
type PlatformInfo struct {
	System       string
	Architecture string
	BinaryPath   string
}

// GetPlatformInfo returns information about the current platform
func GetPlatformInfo() PlatformInfo {
	system := runtime.GOOS
	arch := runtime.GOARCH

	// Normalize system name
	switch system {
	case "windows":
		system = "windows"
	case "darwin":
		system = "macos"
	case "linux":
		system = "linux"
	}

	// Normalize architecture
	switch arch {
	case "amd64":
		if system == "windows" {
			arch = "x64"
		} else {
			arch = "x86_64"
		}
	case "arm64":
		if system == "macos" {
			arch = "arm64"
		} else {
			arch = "aarch64"
		}
	case "386":
		arch = "x86"
	}

	return PlatformInfo{
		System:       system,
		Architecture: arch,
	}
}

// findBinaryPath locates the PQC native library for the current platform
func findBinaryPath() (string, error) {
	info := GetPlatformInfo()

	// Determine platform directory name
	var platformDir string
	switch info.System {
	case "macos":
		platformDir = fmt.Sprintf("macos-%s", info.Architecture)
	case "windows":
		if info.Architecture == "x86_64" || info.Architecture == "x64" {
			platformDir = "windows-x64"
		} else if info.Architecture == "x86" {
			platformDir = "windows-x86"
		} else {
			return "", fmt.Errorf("unsupported Windows architecture: %s", info.Architecture)
		}
	case "linux":
		platformDir = fmt.Sprintf("linux-%s", info.Architecture)
	default:
		return "", fmt.Errorf("unsupported operating system: %s", info.System)
	}

	// Determine library name
	var libName string
	switch info.System {
	case "windows":
		libName = "pqc.dll"
	case "macos":
		libName = "libpqc.dylib"
	default:
		libName = "libpqc.so"
	}

	// Find the binary path relative to this module
	_, filename, _, ok := runtime.Caller(0)
	if !ok {
		return "", errors.New("could not determine module path")
	}

	moduleDir := filepath.Dir(filename)
	repoRoot := filepath.Join(moduleDir, "..", "..")
	binaryPath := filepath.Join(repoRoot, "bins", platformDir, libName)

	if _, err := os.Stat(binaryPath); os.IsNotExist(err) {
		return "", fmt.Errorf("%w for platform %s: %s", ErrLibraryNotFound, platformDir, binaryPath)
	}

	abs, err := filepath.Abs(binaryPath)
	if err != nil {
		return "", fmt.Errorf("failed to get absolute path: %w", err)
	}

	return abs, nil
}

// Initialize the library path
var libraryPath string

func init() {
	var err error
	libraryPath, err = findBinaryPath()
	if err != nil {
		// Don't panic in init, let individual functions handle the error
		libraryPath = ""
	}
}

// GetLibraryInfo returns information about the loaded library
func GetLibraryInfo() map[string]interface{} {
	info := make(map[string]interface{})
	info["version"] = Version
	info["platform"] = GetPlatformInfo()

	if libraryPath != "" {
		info["binary_path"] = libraryPath

		// Try to get library version
		if version := C.pqchub_get_version(); version != nil {
			info["library_version"] = C.GoString(version)
		}

		// Try to get algorithms
		if algorithms := C.pqchub_get_algorithms(); algorithms != nil {
			info["algorithms"] = C.GoString(algorithms)
		}
	} else {
		info["error"] = "Library not found"
	}

	return info
}

// validateKeyLength validates that a key has the expected length
func validateKeyLength(key []byte, expectedLength int, keyType string) error {
	if len(key) != expectedLength {
		return fmt.Errorf("%s must be exactly %d bytes, got %d bytes", keyType, expectedLength, len(key))
	}
	return nil
}

// Common key size constants
const (
	// Kyber512 constants
	Kyber512PublicKeyBytes  = 800
	Kyber512SecretKeyBytes  = 1632
	Kyber512CiphertextBytes = 768
	Kyber512SharedSecretBytes = 32

	// Kyber768 constants
	Kyber768PublicKeyBytes  = 1184
	Kyber768SecretKeyBytes  = 2400
	Kyber768CiphertextBytes = 1088
	Kyber768SharedSecretBytes = 32

	// Kyber1024 constants
	Kyber1024PublicKeyBytes  = 1568
	Kyber1024SecretKeyBytes  = 3168
	Kyber1024CiphertextBytes = 1568
	Kyber1024SharedSecretBytes = 32

	// Dilithium2 constants
	Dilithium2PublicKeyBytes = 1312
	Dilithium2SecretKeyBytes = 2528
	Dilithium2SignatureBytes = 2420

	// Dilithium3 constants
	Dilithium3PublicKeyBytes = 1952
	Dilithium3SecretKeyBytes = 4000
	Dilithium3SignatureBytes = 3293

	// Dilithium5 constants
	Dilithium5PublicKeyBytes = 2592
	Dilithium5SecretKeyBytes = 4864
	Dilithium5SignatureBytes = 4595
)