//! PQChub - Rust wrapper for post-quantum cryptography algorithms
//!
//! This crate provides Rust bindings for post-quantum cryptography algorithms
//! from the PQClean project. It includes Key Encapsulation Mechanisms (KEM) and
//! Digital Signature algorithms.
//!
//! # Supported Algorithms
//!
//! ## Key Encapsulation Mechanisms (KEM)
//! - `Kyber512`, `Kyber768`, `Kyber1024`
//!
//! ## Digital Signatures
//! - `Dilithium2`, `Dilithium3`, `Dilithium5`
//!
//! # Example
//!
//! ```rust
//! use pqchub::{Kyber512, Dilithium2};
//!
//! // Key Encapsulation
//! let kyber = Kyber512::new()?;
//! let (public_key, secret_key) = kyber.keypair()?;
//! let (ciphertext, shared_secret) = kyber.encapsulate(&public_key)?;
//! let decrypted_secret = kyber.decapsulate(&ciphertext, &secret_key)?;
//! assert_eq!(shared_secret, decrypted_secret);
//!
//! // Digital Signatures
//! let dilithium = Dilithium2::new()?;
//! let (pk, sk) = dilithium.keypair()?;
//! let message = b"Hello, post-quantum world!";
//! let signature = dilithium.sign(message, &sk)?;
//! assert!(dilithium.verify(message, &signature, &pk)?);
//! # Ok::<(), Box<dyn std::error::Error>>(())
//! ```

use std::env;
use std::path::{Path, PathBuf};
use std::ffi::{CString, c_char, c_int, c_uchar};
use thiserror::Error;

pub mod kyber;
pub mod dilithium;

pub use kyber::{Kyber512, Kyber768, Kyber1024, Kyber};
pub use dilithium::{Dilithium2, Dilithium3, Dilithium5, Dilithium};

/// Library version
pub const VERSION: &str = "1.0.0";

/// PQC error types
#[derive(Error, Debug)]
pub enum PqcError {
    #[error("Library not found: {0}")]
    LibraryNotFound(String),
    
    #[error("Key generation failed with code {0}")]
    KeyGeneration(i32),
    
    #[error("Encapsulation failed with code {0}")]
    Encapsulation(i32),
    
    #[error("Decapsulation failed with code {0}")]
    Decapsulation(i32),
    
    #[error("Signature generation failed with code {0}")]
    Signing(i32),
    
    #[error("Signature verification failed with code {0}")]
    Verification(i32),
    
    #[error("Invalid key size: expected {expected}, got {actual}")]
    InvalidKeySize { expected: usize, actual: usize },
    
    #[error("Platform not supported: {0}")]
    UnsupportedPlatform(String),
    
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
}

/// Result type for PQC operations
pub type PqcResult<T> = Result<T, PqcError>;

/// Platform information
#[derive(Debug, Clone)]
pub struct PlatformInfo {
    pub system: String,
    pub architecture: String,
    pub binary_path: Option<PathBuf>,
}

/// Get current platform information
pub fn get_platform_info() -> PlatformInfo {
    let (system, architecture) = if cfg!(target_os = "windows") {
        if cfg!(target_arch = "x86_64") {
            ("windows".to_string(), "x64".to_string())
        } else if cfg!(target_arch = "x86") {
            ("windows".to_string(), "x86".to_string())
        } else {
            ("windows".to_string(), env::consts::ARCH.to_string())
        }
    } else if cfg!(target_os = "macos") {
        if cfg!(target_arch = "x86_64") {
            ("macos".to_string(), "x86_64".to_string())
        } else if cfg!(target_arch = "aarch64") {
            ("macos".to_string(), "arm64".to_string())
        } else {
            ("macos".to_string(), env::consts::ARCH.to_string())
        }
    } else if cfg!(target_os = "linux") {
        if cfg!(target_arch = "x86_64") {
            ("linux".to_string(), "x86_64".to_string())
        } else if cfg!(target_arch = "aarch64") {
            ("linux".to_string(), "aarch64".to_string())
        } else {
            ("linux".to_string(), env::consts::ARCH.to_string())
        }
    } else {
        (env::consts::OS.to_string(), env::consts::ARCH.to_string())
    };

    let binary_path = find_binary_path().ok();

    PlatformInfo {
        system,
        architecture,
        binary_path,
    }
}

/// Find the PQC native library for the current platform
pub fn find_binary_path() -> PqcResult<PathBuf> {
    let info = get_platform_info();
    
    // Determine platform directory name
    let platform_dir = match info.system.as_str() {
        "macos" => format!("macos-{}", info.architecture),
        "windows" => {
            if info.architecture == "x86_64" || info.architecture == "x64" {
                "windows-x64".to_string()
            } else if info.architecture == "x86" {
                "windows-x86".to_string()
            } else {
                return Err(PqcError::UnsupportedPlatform(format!(
                    "Windows architecture: {}", info.architecture
                )));
            }
        }
        "linux" => format!("linux-{}", info.architecture),
        _ => return Err(PqcError::UnsupportedPlatform(info.system)),
    };

    // Determine library name
    let lib_name = match info.system.as_str() {
        "windows" => "pqc.dll",
        "macos" => "libpqc.dylib",
        _ => "libpqc.so",
    };

    // Find the binary path relative to this crate
    let manifest_dir = env::var("CARGO_MANIFEST_DIR")
        .map(PathBuf::from)
        .unwrap_or_else(|_| {
            // Fallback: try to find relative to current directory
            std::env::current_dir().unwrap_or_else(|_| PathBuf::from("."))
        });

    let repo_root = manifest_dir.parent().and_then(|p| p.parent())
        .unwrap_or(&manifest_dir);
    
    let binary_path = repo_root.join("bins").join(&platform_dir).join(lib_name);

    if !binary_path.exists() {
        return Err(PqcError::LibraryNotFound(format!(
            "Binary not found for platform {}: {}",
            platform_dir,
            binary_path.display()
        )));
    }

    Ok(binary_path)
}

/// Validate that a slice has the expected length
pub fn validate_length(data: &[u8], expected: usize, name: &str) -> PqcResult<()> {
    if data.len() != expected {
        Err(PqcError::InvalidKeySize {
            expected,
            actual: data.len(),
        })
    } else {
        Ok(())
    }
}

/// External function declarations for the PQC library
extern "C" {
    // Library info functions
    fn pqchub_get_version() -> *const c_char;
    fn pqchub_get_algorithms() -> *const c_char;
    
    // Kyber512 functions
    fn PQCLEAN_KYBER512_CLEAN_crypto_kem_keypair(pk: *mut c_uchar, sk: *mut c_uchar) -> c_int;
    fn PQCLEAN_KYBER512_CLEAN_crypto_kem_enc(
        ct: *mut c_uchar, 
        ss: *mut c_uchar, 
        pk: *const c_uchar
    ) -> c_int;
    fn PQCLEAN_KYBER512_CLEAN_crypto_kem_dec(
        ss: *mut c_uchar, 
        ct: *const c_uchar, 
        sk: *const c_uchar
    ) -> c_int;
    
    // Kyber768 functions
    fn PQCLEAN_KYBER768_CLEAN_crypto_kem_keypair(pk: *mut c_uchar, sk: *mut c_uchar) -> c_int;
    fn PQCLEAN_KYBER768_CLEAN_crypto_kem_enc(
        ct: *mut c_uchar, 
        ss: *mut c_uchar, 
        pk: *const c_uchar
    ) -> c_int;
    fn PQCLEAN_KYBER768_CLEAN_crypto_kem_dec(
        ss: *mut c_uchar, 
        ct: *const c_uchar, 
        sk: *const c_uchar
    ) -> c_int;
    
    // Kyber1024 functions
    fn PQCLEAN_KYBER1024_CLEAN_crypto_kem_keypair(pk: *mut c_uchar, sk: *mut c_uchar) -> c_int;
    fn PQCLEAN_KYBER1024_CLEAN_crypto_kem_enc(
        ct: *mut c_uchar, 
        ss: *mut c_uchar, 
        pk: *const c_uchar
    ) -> c_int;
    fn PQCLEAN_KYBER1024_CLEAN_crypto_kem_dec(
        ss: *mut c_uchar, 
        ct: *const c_uchar, 
        sk: *const c_uchar
    ) -> c_int;
    
    // Dilithium2 functions
    fn PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_keypair(pk: *mut c_uchar, sk: *mut c_uchar) -> c_int;
    fn PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_signature(
        sig: *mut c_uchar,
        siglen: *mut usize,
        m: *const c_uchar,
        mlen: usize,
        sk: *const c_uchar,
    ) -> c_int;
    fn PQCLEAN_DILITHIUM2_CLEAN_crypto_sign_verify(
        sig: *const c_uchar,
        siglen: usize,
        m: *const c_uchar,
        mlen: usize,
        pk: *const c_uchar,
    ) -> c_int;
    
    // Dilithium3 functions
    fn PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_keypair(pk: *mut c_uchar, sk: *mut c_uchar) -> c_int;
    fn PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_signature(
        sig: *mut c_uchar,
        siglen: *mut usize,
        m: *const c_uchar,
        mlen: usize,
        sk: *const c_uchar,
    ) -> c_int;
    fn PQCLEAN_DILITHIUM3_CLEAN_crypto_sign_verify(
        sig: *const c_uchar,
        siglen: usize,
        m: *const c_uchar,
        mlen: usize,
        pk: *const c_uchar,
    ) -> c_int;
    
    // Dilithium5 functions
    fn PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_keypair(pk: *mut c_uchar, sk: *mut c_uchar) -> c_int;
    fn PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_signature(
        sig: *mut c_uchar,
        siglen: *mut usize,
        m: *const c_uchar,
        mlen: usize,
        sk: *const c_uchar,
    ) -> c_int;
    fn PQCLEAN_DILITHIUM5_CLEAN_crypto_sign_verify(
        sig: *const c_uchar,
        siglen: usize,
        m: *const c_uchar,
        mlen: usize,
        pk: *const c_uchar,
    ) -> c_int;
}

/// Get library version information
pub fn get_library_version() -> Option<String> {
    unsafe {
        let version_ptr = pqchub_get_version();
        if version_ptr.is_null() {
            None
        } else {
            let c_str = std::ffi::CStr::from_ptr(version_ptr);
            c_str.to_str().ok().map(|s| s.to_string())
        }
    }
}

/// Get supported algorithms
pub fn get_algorithms() -> Option<String> {
    unsafe {
        let algorithms_ptr = pqchub_get_algorithms();
        if algorithms_ptr.is_null() {
            None
        } else {
            let c_str = std::ffi::CStr::from_ptr(algorithms_ptr);
            c_str.to_str().ok().map(|s| s.to_string())
        }
    }
}

/// Get comprehensive library information
pub fn get_info() -> serde_json::Value {
    use serde_json::json;
    
    let platform = get_platform_info();
    
    json!({
        "version": VERSION,
        "platform": {
            "system": platform.system,
            "architecture": platform.architecture,
            "binary_path": platform.binary_path.as_ref().map(|p| p.to_string_lossy()),
            "library_version": get_library_version(),
            "algorithms": get_algorithms()
        },
        "algorithms": {
            "kem": ["Kyber512", "Kyber768", "Kyber1024"],
            "signatures": ["Dilithium2", "Dilithium3", "Dilithium5"]
        }
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_platform_info() {
        let info = get_platform_info();
        assert!(!info.system.is_empty());
        assert!(!info.architecture.is_empty());
        println!("Platform: {} {}", info.system, info.architecture);
    }

    #[test] 
    fn test_find_binary_path() {
        match find_binary_path() {
            Ok(path) => {
                println!("Binary found at: {}", path.display());
                assert!(path.exists());
            }
            Err(e) => {
                println!("Binary not found: {}", e);
                // This is expected in test environments without binaries
            }
        }
    }
}