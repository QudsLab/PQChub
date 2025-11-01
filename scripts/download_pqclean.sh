#!/bin/bash
set -euo pipefail

# PQClean Download Script (Bash version)
# Download and extract PQClean source code from GitHub

PQCLEAN_REF="${1:-master}"
OUTPUT_DIR="${2:-pqclean}"

echo "Downloading PQClean (ref: $PQCLEAN_REF) to $OUTPUT_DIR"

# Create output directory
if [ -d "$OUTPUT_DIR" ]; then
    echo "Output directory $OUTPUT_DIR already exists"
    read -p "Do you want to remove it and continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted"
        exit 1
    fi
    rm -rf "$OUTPUT_DIR"
fi

mkdir -p "$OUTPUT_DIR"

# Download URL
ARCHIVE_URL="https://github.com/PQClean/PQClean/archive/${PQCLEAN_REF}.tar.gz"
ARCHIVE_FILE="$OUTPUT_DIR/PQClean-${PQCLEAN_REF}.tar.gz"

echo "Downloading $ARCHIVE_URL"

# Download with curl or wget
if command -v curl >/dev/null 2>&1; then
    curl -L -o "$ARCHIVE_FILE" "$ARCHIVE_URL"
elif command -v wget >/dev/null 2>&1; then
    wget -O "$ARCHIVE_FILE" "$ARCHIVE_URL"
else
    echo "Error: Neither curl nor wget found"
    exit 1
fi

echo "Downloaded to $ARCHIVE_FILE"

# Extract archive
echo "Extracting $ARCHIVE_FILE"
tar -xzf "$ARCHIVE_FILE" -C "$OUTPUT_DIR" --strip-components=1

# Clean up archive
rm "$ARCHIVE_FILE"

echo "✅ PQClean $PQCLEAN_REF downloaded successfully to $OUTPUT_DIR"

# Verify essential directories exist
ESSENTIAL_DIRS=("crypto_kem" "crypto_sign" "common")
MISSING_DIRS=()

for dir in "${ESSENTIAL_DIRS[@]}"; do
    if [ ! -d "$OUTPUT_DIR/$dir" ]; then
        MISSING_DIRS+=("$dir")
    fi
done

if [ ${#MISSING_DIRS[@]} -ne 0 ]; then
    echo "⚠️  Warning: Missing expected directories: ${MISSING_DIRS[*]}"
    exit 1
fi

echo "✅ Directory structure verification passed"
echo "PQClean source is ready for compilation"