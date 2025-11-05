#!/bin/bash
set -euo pipefail

# PQClean Native Library Build Script
# Builds a unified native library containing all supported PQC algorithms

TARGET_PLATFORM="$1"
PQCLEAN_SOURCE="${2:-pqclean}"

if [ ! -d "$PQCLEAN_SOURCE" ]; then
    echo "Error: PQClean source directory not found: $PQCLEAN_SOURCE"
    echo "Run download_pqclean.sh first"
    exit 1
fi

echo "Building native library for $TARGET_PLATFORM"
echo "PQClean source: $PQCLEAN_SOURCE"

# Create build directory
BUILD_DIR="build_$TARGET_PLATFORM"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# Output directory
OUTPUT_DIR="bins/$TARGET_PLATFORM"
mkdir -p "$OUTPUT_DIR"

# Compiler settings based on platform
case "$TARGET_PLATFORM" in
    "linux-x86_64")
        CC="${CC:-gcc}"
        CFLAGS="-O3 -fPIC -march=x86-64 -mtune=generic"
        LDFLAGS="-shared"
        OUTPUT_LIB="$OUTPUT_DIR/libpqc.so"
        ;;
    "linux-aarch64")
        CC="${CC:-aarch64-linux-gnu-gcc}"
        CFLAGS="-O3 -fPIC -march=armv8-a"
        LDFLAGS="-shared"
        OUTPUT_LIB="$OUTPUT_DIR/libpqc.so"
        ;;
    "macos-x86_64")
        CC="${CC:-clang}"
        CFLAGS="-O3 -fPIC -arch x86_64 -mmacosx-version-min=10.12"
        LDFLAGS="-shared -arch x86_64"
        OUTPUT_LIB="$OUTPUT_DIR/libpqc.dylib"
        ;;
    "macos-arm64")
        CC="${CC:-clang}"
        CFLAGS="-O3 -fPIC -arch arm64 -mmacosx-version-min=11.0"
        LDFLAGS="-shared -arch arm64"
        OUTPUT_LIB="$OUTPUT_DIR/libpqc.dylib"
        ;;
    *)
        echo "Error: Unsupported target platform: $TARGET_PLATFORM"
        exit 1
        ;;
esac

echo "Compiler: $CC"
echo "CFLAGS: $CFLAGS"
echo "LDFLAGS: $LDFLAGS"
echo "Output: $OUTPUT_LIB"

# Supported algorithms
ALGORITHMS=(
    # Kyber KEM variants
    "crypto_kem/kyber512/clean"
    "crypto_kem/kyber768/clean"
    "crypto_kem/kyber1024/clean"
    
    # Dilithium signature variants
    "crypto_sign/dilithium2/clean"
    "crypto_sign/dilithium3/clean"
    "crypto_sign/dilithium5/clean"
    
    # Falcon signature variants
    "crypto_sign/falcon-512/clean"
    "crypto_sign/falcon-1024/clean"
)

# Check which algorithms are available
AVAILABLE_ALGORITHMS=()
for algo in "${ALGORITHMS[@]}"; do
    if [ -d "$PQCLEAN_SOURCE/$algo" ]; then
        AVAILABLE_ALGORITHMS+=("$algo")
        echo "✓ Found: $algo"
    else
        echo "⚠ Missing: $algo"
    fi
done

if [ ${#AVAILABLE_ALGORITHMS[@]} -eq 0 ]; then
    echo "Error: No supported algorithms found in $PQCLEAN_SOURCE"
    exit 1
fi

echo "Building ${#AVAILABLE_ALGORITHMS[@]} algorithms..."

# Collect all source files
SOURCE_FILES=()
INCLUDE_DIRS=()

# Add common files
COMMON_DIR="$PQCLEAN_SOURCE/common"
if [ -d "$COMMON_DIR" ]; then
    INCLUDE_DIRS+=("-I$COMMON_DIR")
    # Add specific common files that are needed
    for common_file in fips202.c sha2.c randombytes.c aes.c; do
        if [ -f "$COMMON_DIR/$common_file" ]; then
            SOURCE_FILES+=("$COMMON_DIR/$common_file")
        fi
    done
fi

# Process each algorithm
for algo in "${AVAILABLE_ALGORITHMS[@]}"; do
    algo_dir="$PQCLEAN_SOURCE/$algo"
    INCLUDE_DIRS+=("-I$algo_dir")
    
    # Find all .c files in the algorithm directory
    while IFS= read -r -d '' file; do
        SOURCE_FILES+=("$file")
    done < <(find "$algo_dir" -name "*.c" -print0)
done

echo "Found ${#SOURCE_FILES[@]} source files"
echo "Include directories: ${INCLUDE_DIRS[*]}"

# Create wrapper C file that exports all functions
WRAPPER_FILE="$BUILD_DIR/pqc_wrapper.c"
cat > "$WRAPPER_FILE" << 'EOF'
/*
 * PQChub Unified Library Wrapper
 * This file exports all supported PQC algorithm functions
 */

// Include all algorithm headers
#include "api.h"

// Kyber KEM
#ifdef PQCLEAN_KYBER512_CLEAN_CRYPTO_PUBLICKEYBYTES
extern int PQCLEAN_KYBER512_CLEAN_crypto_kem_keypair(unsigned char *pk, unsigned char *sk);
extern int PQCLEAN_KYBER512_CLEAN_crypto_kem_enc(unsigned char *ct, unsigned char *ss, const unsigned char *pk);
extern int PQCLEAN_KYBER512_CLEAN_crypto_kem_dec(unsigned char *ss, const unsigned char *ct, const unsigned char *sk);
#endif

#ifdef PQCLEAN_KYBER768_CLEAN_CRYPTO_PUBLICKEYBYTES
extern int PQCLEAN_KYBER768_CLEAN_crypto_kem_keypair(unsigned char *pk, unsigned char *sk);
extern int PQCLEAN_KYBER768_CLEAN_crypto_kem_enc(unsigned char *ct, unsigned char *ss, const unsigned char *pk);
extern int PQCLEAN_KYBER768_CLEAN_crypto_kem_dec(unsigned char *ss, const unsigned char *ct, const unsigned char *sk);
#endif

#ifdef PQCLEAN_KYBER1024_CLEAN_CRYPTO_PUBLICKEYBYTES
extern int PQCLEAN_KYBER1024_CLEAN_crypto_kem_keypair(unsigned char *pk, unsigned char *sk);
extern int PQCLEAN_KYBER1024_CLEAN_crypto_kem_enc(unsigned char *ct, unsigned char *ss, const unsigned char *pk);
extern int PQCLEAN_KYBER1024_CLEAN_crypto_kem_dec(unsigned char *ss, const unsigned char *ct, const unsigned char *sk);
#endif

// Dilithium signatures
#ifdef PQCLEAN_DILITHIUM2_CLEAN_CRYPTO_PUBLICKEYBYTES
extern int PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_keypair(unsigned char *pk, unsigned char *sk);
extern int PQCLEAN_DILITHIUM2_CLEAN_crypto_sign(unsigned char *sm, size_t *smlen, const unsigned char *m, size_t mlen, const unsigned char *sk);
extern int PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_open(unsigned char *m, size_t *mlen, const unsigned char *sm, size_t smlen, const unsigned char *pk);
extern int PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_signature(unsigned char *sig, size_t *siglen, const unsigned char *m, size_t mlen, const unsigned char *sk);
extern int PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_verify(const unsigned char *sig, size_t siglen, const unsigned char *m, size_t mlen, const unsigned char *pk);
#endif

#ifdef PQCLEAN_DILITHIUM3_CLEAN_CRYPTO_PUBLICKEYBYTES
extern int PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_keypair(unsigned char *pk, unsigned char *sk);
extern int PQCLEAN_DILITHIUM3_CLEAN_crypto_sign(unsigned char *sm, size_t *smlen, const unsigned char *m, size_t mlen, const unsigned char *sk);
extern int PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_open(unsigned char *m, size_t *mlen, const unsigned char *sm, size_t smlen, const unsigned char *pk);
extern int PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_signature(unsigned char *sig, size_t *siglen, const unsigned char *m, size_t mlen, const unsigned char *sk);
extern int PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_verify(const unsigned char *sig, size_t siglen, const unsigned char *m, size_t mlen, const unsigned char *pk);
#endif

#ifdef PQCLEAN_DILITHIUM5_CLEAN_CRYPTO_PUBLICKEYBYTES
extern int PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_keypair(unsigned char *pk, unsigned char *sk);
extern int PQCLEAN_DILITHIUM5_CLEAN_crypto_sign(unsigned char *sm, size_t *smlen, const unsigned char *m, size_t mlen, const unsigned char *sk);
extern int PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_open(unsigned char *m, size_t *mlen, const unsigned char *sm, size_t smlen, const unsigned char *pk);
extern int PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_signature(unsigned char *sig, size_t *siglen, const unsigned char *m, size_t mlen, const unsigned char *sk);
extern int PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_verify(const unsigned char *sig, size_t siglen, const unsigned char *m, size_t mlen, const unsigned char *pk);
#endif

// Falcon signatures
#ifdef PQCLEAN_FALCON512_CLEAN_CRYPTO_PUBLICKEYBYTES
extern int PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair(unsigned char *pk, unsigned char *sk);
extern int PQCLEAN_FALCON512_CLEAN_crypto_sign(unsigned char *sm, size_t *smlen, const unsigned char *m, size_t mlen, const unsigned char *sk);
extern int PQCLEAN_FALCON512_CLEAN_crypto_sign_open(unsigned char *m, size_t *mlen, const unsigned char *sm, size_t smlen, const unsigned char *pk);
extern int PQCLEAN_FALCON512_CLEAN_crypto_sign_signature(unsigned char *sig, size_t *siglen, const unsigned char *m, size_t mlen, const unsigned char *sk);
extern int PQCLEAN_FALCON512_CLEAN_crypto_sign_verify(const unsigned char *sig, size_t siglen, const unsigned char *m, size_t mlen, const unsigned char *pk);
#endif

#ifdef PQCLEAN_FALCON1024_CLEAN_CRYPTO_PUBLICKEYBYTES
extern int PQCLEAN_FALCON1024_CLEAN_crypto_sign_keypair(unsigned char *pk, unsigned char *sk);
extern int PQCLEAN_FALCON1024_CLEAN_crypto_sign(unsigned char *sm, size_t *smlen, const unsigned char *m, size_t mlen, const unsigned char *sk);
extern int PQCLEAN_FALCON1024_CLEAN_crypto_sign_open(unsigned char *m, size_t *mlen, const unsigned char *sm, size_t smlen, const unsigned char *pk);
extern int PQCLEAN_FALCON1024_CLEAN_crypto_sign_signature(unsigned char *sig, size_t *siglen, const unsigned char *m, size_t mlen, const unsigned char *sk);
extern int PQCLEAN_FALCON1024_CLEAN_crypto_sign_verify(const unsigned char *sig, size_t siglen, const unsigned char *m, size_t mlen, const unsigned char *pk);
#endif

// Library info function
const char* pqchub_get_version(void) {
    return "PQChub 1.0.0";
}

const char* pqchub_get_algorithms(void) {
    return "ML-KEM-512,ML-KEM-768,ML-KEM-1024,ML-DSA-44,ML-DSA-65,ML-DSA-87,Falcon-512,Falcon-1024";
}
EOF

# Add wrapper to source files
SOURCE_FILES+=("$WRAPPER_FILE")

# Compile the shared library
echo "Compiling shared library..."
$CC $CFLAGS "${INCLUDE_DIRS[@]}" "${SOURCE_FILES[@]}" $LDFLAGS -o "$OUTPUT_LIB"

if [ -f "$OUTPUT_LIB" ]; then
    echo "✅ Successfully built: $OUTPUT_LIB"
    
    # Show library info
    ls -lh "$OUTPUT_LIB"
    
    # Platform-specific library info
    case "$TARGET_PLATFORM" in
        linux-*)
            file "$OUTPUT_LIB"
            objdump -T "$OUTPUT_LIB" | grep -E "(kyber|dilithium|falcon)" | head -10 || true
            ;;
        macos-*)
            file "$OUTPUT_LIB"
            otool -L "$OUTPUT_LIB" || true
            ;;
    esac
    
    echo "✅ Build completed successfully"
else
    echo "❌ Build failed: Output library not found"
    exit 1
fi

# Clean up build directory
rm -rf "$BUILD_DIR"

echo "Native library for $TARGET_PLATFORM is ready at $OUTPUT_LIB"