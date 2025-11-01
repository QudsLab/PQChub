#!/usr/bin/env python3
"""
PQClean Download Script
Download and extract PQClean source code from GitHub
"""

import argparse
import os
import sys
import urllib.request
import tarfile
import zipfile
import shutil
from pathlib import Path

def download_file(url, dest_path):
    """Download a file from URL to destination path"""
    print(f"Downloading {url}")
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"Downloaded to {dest_path}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def extract_archive(archive_path, extract_to):
    """Extract tar.gz or zip archive"""
    print(f"Extracting {archive_path}")
    try:
        if archive_path.endswith('.tar.gz'):
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(extract_to)
        elif archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
        else:
            print(f"Unsupported archive format: {archive_path}")
            return False
        print(f"Extracted to {extract_to}")
        return True
    except Exception as e:
        print(f"Error extracting {archive_path}: {e}")
        return False

def download_pqclean(ref="master", output_dir="pqclean", force=False):
    """Download PQClean source code"""
    
    # Create output directory
    output_path = Path(output_dir)
    if output_path.exists():
        if not force:
            print(f"Output directory {output_path} already exists")
            response = input("Do you want to remove it and continue? (y/N): ")
            if response.lower() != 'y':
                print("Aborted")
                return False
        else:
            print(f"Removing existing directory {output_path}")
        shutil.rmtree(output_path)
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Download URL for the specified reference
    archive_url = f"https://github.com/PQClean/PQClean/archive/{ref}.tar.gz"
    archive_file = output_path / f"PQClean-{ref}.tar.gz"
    
    # Download the archive
    if not download_file(archive_url, archive_file):
        return False
    
    # Extract the archive
    temp_extract = output_path / "temp"
    temp_extract.mkdir(exist_ok=True)
    
    if not extract_archive(str(archive_file), str(temp_extract)):
        return False
    
    # Find the extracted directory (should be PQClean-{ref})
    extracted_dirs = list(temp_extract.glob("PQClean-*"))
    if not extracted_dirs:
        print("Error: Could not find extracted PQClean directory")
        return False
    
    source_dir = extracted_dirs[0]
    
    # Move contents to output directory
    for item in source_dir.iterdir():
        dest = output_path / item.name
        if dest.exists():
            if dest.is_dir():
                shutil.rmtree(dest)
            else:
                dest.unlink()
        shutil.move(str(item), str(dest))
    
    # Clean up
    shutil.rmtree(temp_extract)
    archive_file.unlink()
    
    print(f"[SUCCESS] PQClean {ref} downloaded successfully to {output_path}")
    
    # Verify essential directories exist
    essential_dirs = ["crypto_kem", "crypto_sign", "common"]
    missing_dirs = []
    for dir_name in essential_dirs:
        if not (output_path / dir_name).exists():
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"[WARNING] Missing expected directories: {missing_dirs}")
        return False
    
    print("[SUCCESS] Directory structure verification passed")
    return True

def main():
    parser = argparse.ArgumentParser(description="Download PQClean source code")
    parser.add_argument("--ref", default="master", 
                       help="Git reference to download (branch, tag, or commit)")
    parser.add_argument("--output", default="pqclean",
                       help="Output directory for PQClean source")
    parser.add_argument("--force", action="store_true",
                       help="Force overwrite existing directory without prompting")
    
    args = parser.parse_args()
    
    success = download_pqclean(args.ref, args.output, force=args.force)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()