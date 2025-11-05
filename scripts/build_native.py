#!/usr/bin/env python3
"""
PQClean Native Library Build Script (Windows)
Builds a unified native library containing all supported PQC algorithms
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import glob

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def build_native_windows(target_platform, pqclean_source):
    """Build native library for Windows"""
    
    if not Path(pqclean_source).exists():
        print(f"Error: PQClean source directory not found: {pqclean_source}")
        print("Run download_pqclean.py first")
        return False
    
    print(f"Building native library for {target_platform}")
    print(f"PQClean source: {pqclean_source}")
    
    # Create build directory
    build_dir = Path(f"build_{target_platform}")
    build_dir.mkdir(exist_ok=True)
    
    # Output directory
    output_dir = Path("bins") / target_platform
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Compiler settings based on platform
    if target_platform == "windows-x64":
        arch = "x64"
        output_lib = output_dir / "pqc.dll"
    elif target_platform == "windows-x86":
        arch = "x86"
        output_lib = output_dir / "pqc.dll"
    else:
        print(f"Error: Unsupported target platform: {target_platform}")
        return False
    
    print(f"Architecture: {arch}")
    print(f"Output: {output_lib}")
    
    # Supported algorithms
    algorithms = [
        # Kyber KEM variants
        "crypto_kem/kyber512/clean",
        "crypto_kem/kyber768/clean", 
        "crypto_kem/kyber1024/clean",
        
        # Dilithium signature variants
        "crypto_sign/dilithium2/clean",
        "crypto_sign/dilithium3/clean",
        "crypto_sign/dilithium5/clean",
        
        # Falcon signature variants
        "crypto_sign/falcon-512/clean",
        "crypto_sign/falcon-1024/clean",
    ]
    
    # Check which algorithms are available
    available_algorithms = []
    pqclean_path = Path(pqclean_source)
    
    for algo in algorithms:
        algo_path = pqclean_path / algo
        if algo_path.exists():
            available_algorithms.append(algo)
            print(f"[OK] Found: {algo}")
        else:
            print(f"[WARN] Missing: {algo}")
    
    if not available_algorithms:
        print(f"Error: No supported algorithms found in {pqclean_source}")
        return False
    
    print(f"Building {len(available_algorithms)} algorithms...")
    
    # Collect all source files
    source_files = []
    include_dirs = []
    
    # Add common files
    common_dir = pqclean_path / "common"
    if common_dir.exists():
        include_dirs.append(str(common_dir.absolute()))
        # Add specific common files that are needed
        for common_file in ["fips202.c", "sha2.c", "randombytes.c", "aes.c"]:
            common_path = common_dir / common_file
            if common_path.exists():
                source_files.append(str(common_path.absolute()))
    
    # Process each algorithm
    for algo in available_algorithms:
        algo_dir = pqclean_path / algo
        include_dirs.append(str(algo_dir.absolute()))
        
        # Find all .c files in the algorithm directory
        c_files = list(algo_dir.glob("*.c"))
        source_files.extend([str(f.absolute()) for f in c_files])
    
    print(f"Found {len(source_files)} source files")
    print(f"Include directories: {len(include_dirs)}")
    
    # Create wrapper C file
    wrapper_file = build_dir / "pqc_wrapper.c"
    wrapper_content = '''/*
 * PQChub Unified Library Wrapper (Windows)
 * This file exports all supported PQC algorithm functions
 */

#include <stddef.h>

// Export macro for Windows DLL
#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

// Library info functions
EXPORT const char* pqchub_get_version(void) {
    return "PQChub 1.0.0";
}

EXPORT const char* pqchub_get_algorithms(void) {
    return "ML-KEM-512,ML-KEM-768,ML-KEM-1024,ML-DSA-44,ML-DSA-65,ML-DSA-87,Falcon-512,Falcon-1024";
}

EXPORT const char* pqchub_get_platform(void) {
    return "''' + target_platform + '''";
}
'''
    
    # Create DEF file to export ALL algorithm functions
    def_file = build_dir / "pqc.def"
    def_content = '''LIBRARY pqc
EXPORTS
    pqchub_get_version
    pqchub_get_algorithms
    pqchub_get_platform
    
    ; Kyber512 KEM
    PQCLEAN_KYBER512_CLEAN_crypto_kem_keypair
    PQCLEAN_KYBER512_CLEAN_crypto_kem_enc
    PQCLEAN_KYBER512_CLEAN_crypto_kem_dec
    
    ; Kyber768 KEM
    PQCLEAN_KYBER768_CLEAN_crypto_kem_keypair
    PQCLEAN_KYBER768_CLEAN_crypto_kem_enc
    PQCLEAN_KYBER768_CLEAN_crypto_kem_dec
    
    ; Kyber1024 KEM
    PQCLEAN_KYBER1024_CLEAN_crypto_kem_keypair
    PQCLEAN_KYBER1024_CLEAN_crypto_kem_enc
    PQCLEAN_KYBER1024_CLEAN_crypto_kem_dec
    
    ; Dilithium2 Signature
    PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_keypair
    PQCLEAN_DILITHIUM2_CLEAN_crypto_sign
    PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_open
    PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_signature
    PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_verify
    
    ; Dilithium3 Signature
    PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_keypair
    PQCLEAN_DILITHIUM3_CLEAN_crypto_sign
    PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_open
    PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_signature
    PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_verify
    
    ; Dilithium5 Signature
    PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_keypair
    PQCLEAN_DILITHIUM5_CLEAN_crypto_sign
    PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_open
    PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_signature
    PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_verify
    
    ; Falcon-512 Signature
    PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair
    PQCLEAN_FALCON512_CLEAN_crypto_sign
    PQCLEAN_FALCON512_CLEAN_crypto_sign_open
    PQCLEAN_FALCON512_CLEAN_crypto_sign_signature
    PQCLEAN_FALCON512_CLEAN_crypto_sign_verify
    
    ; Falcon-1024 Signature
    PQCLEAN_FALCON1024_CLEAN_crypto_sign_keypair
    PQCLEAN_FALCON1024_CLEAN_crypto_sign
    PQCLEAN_FALCON1024_CLEAN_crypto_sign_open
    PQCLEAN_FALCON1024_CLEAN_crypto_sign_signature
    PQCLEAN_FALCON1024_CLEAN_crypto_sign_verify
'''
    
    with open(wrapper_file, 'w') as f:
        f.write(wrapper_content)
    
    with open(def_file, 'w') as f:
        f.write(def_content)
    
    source_files.append(str(wrapper_file.absolute()))
    
    # Step 1: Compile each source file to object file with unique names
    print("Compiling source files to object files...")
    obj_files = []
    obj_counter = 0
    
    for src_file in source_files:
        # Create unique object file name
        obj_file = build_dir / f"obj_{obj_counter}.obj"
        obj_files.append(str(obj_file.absolute()))
        obj_counter += 1
        
        # Compile this source file
        compile_cmd = [
            "cl.exe",
            "/c",            # Compile only (don't link)
            "/O2",           # Optimize for speed
            "/GL",           # Whole program optimization
            "/MD",           # Use MSVCRT.lib
            "/nologo",       # Suppress startup banner
            "/W1",           # Warning level 1
        ]
        
        # Add include directories
        for include_dir in include_dirs:
            compile_cmd.append(f"/I{include_dir}")
        
        # Add source file and output object file
        compile_cmd.append(src_file)
        compile_cmd.append(f"/Fo{obj_file.absolute()}")
        
        # Compile without changing directory
        success = run_command(compile_cmd)
        if not success:
            print(f"[ERROR] Failed to compile: {src_file}")
            return False
    
    print(f"Successfully compiled {len(obj_files)} object files")
    
    # Step 2: Link all object files into DLL
    print("Linking DLL...")
    link_cmd = [
        "link.exe",
        "/DLL",                      # Create DLL
        "/LTCG",                     # Link-time code generation
        "/nologo",                   # Suppress startup banner
        f"/OUT:{output_lib.absolute()}",  # Output file
    ]
    
    # Add all object files
    link_cmd.extend(obj_files)
    
    # Add DEF file to export Falcon functions
    link_cmd.append(f"/DEF:{def_file.absolute()}")
    
    # Add necessary libraries
    link_cmd.append("advapi32.lib")
    
    # Link without changing directory
    success = run_command(link_cmd)
    
    if success and output_lib.exists():
        print(f"[SUCCESS] Successfully built: {output_lib}")
        
        # Show library info
        print(f"File size: {output_lib.stat().st_size} bytes")
        
        print("[SUCCESS] Build completed successfully")
        
        # Clean up build directory artifacts (only temporary object files)
        # Keep .lib and .exp in output directory as they're needed for linking
        for pattern in ["*.obj", "*.pdb"]:
            for file in build_dir.glob(pattern):
                try:
                    file.unlink()
                except:
                    pass
        
        return True
    else:
        print("[ERROR] Build failed: Output library not found")
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python build_native.py <target_platform> <pqclean_source>")
        print("Example: python build_native.py windows-x64 pqclean")
        sys.exit(1)
    
    target_platform = sys.argv[1]
    pqclean_source = sys.argv[2]
    
    success = build_native_windows(target_platform, pqclean_source)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()