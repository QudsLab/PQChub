#!/bin/bash
set -euo pipefail

# PQClean Android NDK Build Script
# Builds native libraries for Android using NDK

ANDROID_ABI="$1"
PQCLEAN_SOURCE="${2:-pqclean}"

if [ ! -d "$PQCLEAN_SOURCE" ]; then
    echo "Error: PQClean source directory not found: $PQCLEAN_SOURCE"
    echo "Run download_pqclean.sh first"
    exit 1
fi

if [ -z "${ANDROID_NDK_ROOT:-}" ]; then
    echo "Error: ANDROID_NDK_ROOT environment variable not set"
    exit 1
fi

echo "Building Android library for ABI: $ANDROID_ABI"
echo "PQClean source: $PQCLEAN_SOURCE"
echo "Android NDK: $ANDROID_NDK_ROOT"

# Create build directory
BUILD_DIR="build_android_$ANDROID_ABI"
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

# Output directory
OUTPUT_DIR="bins/android-$ANDROID_ABI"
mkdir -p "$OUTPUT_DIR"
OUTPUT_LIB="$OUTPUT_DIR/libpqc.so"

# NDK toolchain settings
NDK_API_LEVEL=21  # Android 5.0+
TOOLCHAIN_PREFIX=""
ARCH_FLAGS=""

case "$ANDROID_ABI" in
    "arm64-v8a")
        TOOLCHAIN_PREFIX="aarch64-linux-android"
        ARCH_FLAGS="-march=armv8-a"
        ;;
    "armeabi-v7a")
        TOOLCHAIN_PREFIX="armv7a-linux-androideabi"
        ARCH_FLAGS="-march=armv7-a -mfloat-abi=softfp -mfpu=neon"
        ;;
    "x86_64")
        TOOLCHAIN_PREFIX="x86_64-linux-android"
        ARCH_FLAGS="-march=x86-64"
        ;;
    "x86")
        TOOLCHAIN_PREFIX="i686-linux-android"
        ARCH_FLAGS="-march=i686"
        ;;
    *)
        echo "Error: Unsupported Android ABI: $ANDROID_ABI"
        exit 1
        ;;
esac

# Set up NDK toolchain
NDK_TOOLCHAIN_DIR="$ANDROID_NDK_ROOT/toolchains/llvm/prebuilt"

# Detect host OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    HOST_TAG="linux-x86_64"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    HOST_TAG="darwin-x86_64"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    HOST_TAG="windows-x86_64"
else
    echo "Error: Unsupported host OS: $OSTYPE"
    exit 1
fi

TOOLCHAIN_PATH="$NDK_TOOLCHAIN_DIR/$HOST_TAG"

if [ ! -d "$TOOLCHAIN_PATH" ]; then
    echo "Error: NDK toolchain not found: $TOOLCHAIN_PATH"
    exit 1
fi

# Set compiler and flags
CC="$TOOLCHAIN_PATH/bin/${TOOLCHAIN_PREFIX}${NDK_API_LEVEL}-clang"
CXX="$TOOLCHAIN_PATH/bin/${TOOLCHAIN_PREFIX}${NDK_API_LEVEL}-clang++"

if [ ! -f "$CC" ]; then
    echo "Error: Compiler not found: $CC"
    exit 1
fi

CFLAGS="-O3 -fPIC $ARCH_FLAGS -DANDROID -D__ANDROID_API__=$NDK_API_LEVEL"
LDFLAGS="-shared"

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
    
    # Falcon signature variants (may have issues on some Android ABIs)
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

# Create Android-specific wrapper
WRAPPER_FILE="$BUILD_DIR/pqc_android_wrapper.c"
cat > "$WRAPPER_FILE" << EOF
/*
 * PQChub Android Library Wrapper
 * This file exports functions for Android JNI usage
 */

#include <jni.h>
#include <android/log.h>

#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, "PQChub", __VA_ARGS__)

// Library info functions
const char* pqchub_get_version(void) {
    return "PQChub 1.0.0";
}

const char* pqchub_get_algorithms(void) {
    return "ML-KEM-512,ML-KEM-768,ML-KEM-1024,ML-DSA-44,ML-DSA-65,ML-DSA-87,Falcon-512,Falcon-1024";
}

const char* pqchub_get_android_abi(void) {
    return "$ANDROID_ABI";
}

// JNI wrapper for version info
JNIEXPORT jstring JNICALL
Java_com_qudslab_pqchub_PQC_getVersion(JNIEnv *env, jclass clazz) {
    return (*env)->NewStringUTF(env, pqchub_get_version());
}

JNIEXPORT jstring JNICALL
Java_com_qudslab_pqchub_PQC_getAlgorithms(JNIEnv *env, jclass clazz) {
    return (*env)->NewStringUTF(env, pqchub_get_algorithms());
}

JNIEXPORT jstring JNICALL
Java_com_qudslab_pqchub_PQC_getAndroidAbi(JNIEnv *env, jclass clazz) {
    return (*env)->NewStringUTF(env, pqchub_get_android_abi());
}

// Library initialization
JNIEXPORT jint JNICALL
JNI_OnLoad(JavaVM *vm, void *reserved) {
    LOGI("PQChub native library loaded for ABI: $ANDROID_ABI");
    return JNI_VERSION_1_6;
}
EOF

# Add wrapper to source files
SOURCE_FILES+=("$WRAPPER_FILE")

# Compile the shared library
echo "Compiling Android shared library..."
"$CC" $CFLAGS "${INCLUDE_DIRS[@]}" "${SOURCE_FILES[@]}" $LDFLAGS -llog -o "$OUTPUT_LIB"

if [ -f "$OUTPUT_LIB" ]; then
    echo "✅ Successfully built: $OUTPUT_LIB"
    
    # Show library info
    ls -lh "$OUTPUT_LIB"
    file "$OUTPUT_LIB"
    
    # Check dependencies
    "$TOOLCHAIN_PATH/bin/llvm-readobj" --needed-libs "$OUTPUT_LIB" || true
    
    echo "✅ Build completed successfully"
else
    echo "❌ Build failed: Output library not found"
    exit 1
fi

# Clean up build directory
rm -rf "$BUILD_DIR"

echo "Android library for $ANDROID_ABI is ready at $OUTPUT_LIB"