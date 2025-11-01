//! Kyber Key Encapsulation Mechanisms

use crate::{PqcError, PqcResult, validate_length};
use std::ffi::c_uchar;

/// Kyber512 Key Encapsulation Mechanism
/// 
/// Security Level: 1 (equivalent to AES-128)
/// - Public Key: 800 bytes
/// - Secret Key: 1632 bytes  
/// - Ciphertext: 768 bytes
/// - Shared Secret: 32 bytes
pub struct Kyber512 {
    _private: (),
}

impl Kyber512 {
    /// Algorithm constants
    pub const PUBLIC_KEY_BYTES: usize = 800;
    pub const SECRET_KEY_BYTES: usize = 1632;
    pub const CIPHERTEXT_BYTES: usize = 768;
    pub const SHARED_SECRET_BYTES: usize = 32;

    /// Create a new Kyber512 instance
    pub fn new() -> PqcResult<Self> {
        // Verify library is available
        crate::find_binary_path()?;
        Ok(Self { _private: () })
    }

    /// Generate a key pair
    pub fn keypair(&self) -> PqcResult<(Vec<u8>, Vec<u8>)> {
        let mut public_key = vec![0u8; Self::PUBLIC_KEY_BYTES];
        let mut secret_key = vec![0u8; Self::SECRET_KEY_BYTES];

        let result = unsafe {
            crate::PQCLEAN_KYBER512_CLEAN_crypto_kem_keypair(
                public_key.as_mut_ptr() as *mut c_uchar,
                secret_key.as_mut_ptr() as *mut c_uchar,
            )
        };

        if result != 0 {
            return Err(PqcError::KeyGeneration(result));
        }

        Ok((public_key, secret_key))
    }

    /// Encapsulate a shared secret
    pub fn encapsulate(&self, public_key: &[u8]) -> PqcResult<(Vec<u8>, Vec<u8>)> {
        validate_length(public_key, Self::PUBLIC_KEY_BYTES, "public key")?;

        let mut ciphertext = vec![0u8; Self::CIPHERTEXT_BYTES];
        let mut shared_secret = vec![0u8; Self::SHARED_SECRET_BYTES];

        let result = unsafe {
            crate::PQCLEAN_KYBER512_CLEAN_crypto_kem_enc(
                ciphertext.as_mut_ptr() as *mut c_uchar,
                shared_secret.as_mut_ptr() as *mut c_uchar,
                public_key.as_ptr() as *const c_uchar,
            )
        };

        if result != 0 {
            return Err(PqcError::Encapsulation(result));
        }

        Ok((ciphertext, shared_secret))
    }

    /// Decapsulate the shared secret
    pub fn decapsulate(&self, ciphertext: &[u8], secret_key: &[u8]) -> PqcResult<Vec<u8>> {
        validate_length(ciphertext, Self::CIPHERTEXT_BYTES, "ciphertext")?;
        validate_length(secret_key, Self::SECRET_KEY_BYTES, "secret key")?;

        let mut shared_secret = vec![0u8; Self::SHARED_SECRET_BYTES];

        let result = unsafe {
            crate::PQCLEAN_KYBER512_CLEAN_crypto_kem_dec(
                shared_secret.as_mut_ptr() as *mut c_uchar,
                ciphertext.as_ptr() as *const c_uchar,
                secret_key.as_ptr() as *const c_uchar,
            )
        };

        if result != 0 {
            return Err(PqcError::Decapsulation(result));
        }

        Ok(shared_secret)
    }
}

/// Kyber768 Key Encapsulation Mechanism
/// 
/// Security Level: 3 (equivalent to AES-192)
/// - Public Key: 1184 bytes
/// - Secret Key: 2400 bytes
/// - Ciphertext: 1088 bytes
/// - Shared Secret: 32 bytes
pub struct Kyber768 {
    _private: (),
}

impl Kyber768 {
    /// Algorithm constants
    pub const PUBLIC_KEY_BYTES: usize = 1184;
    pub const SECRET_KEY_BYTES: usize = 2400;
    pub const CIPHERTEXT_BYTES: usize = 1088;
    pub const SHARED_SECRET_BYTES: usize = 32;

    /// Create a new Kyber768 instance
    pub fn new() -> PqcResult<Self> {
        crate::find_binary_path()?;
        Ok(Self { _private: () })
    }

    /// Generate a key pair
    pub fn keypair(&self) -> PqcResult<(Vec<u8>, Vec<u8>)> {
        let mut public_key = vec![0u8; Self::PUBLIC_KEY_BYTES];
        let mut secret_key = vec![0u8; Self::SECRET_KEY_BYTES];

        let result = unsafe {
            crate::PQCLEAN_KYBER768_CLEAN_crypto_kem_keypair(
                public_key.as_mut_ptr() as *mut c_uchar,
                secret_key.as_mut_ptr() as *mut c_uchar,
            )
        };

        if result != 0 {
            return Err(PqcError::KeyGeneration(result));
        }

        Ok((public_key, secret_key))
    }

    /// Encapsulate a shared secret
    pub fn encapsulate(&self, public_key: &[u8]) -> PqcResult<(Vec<u8>, Vec<u8>)> {
        validate_length(public_key, Self::PUBLIC_KEY_BYTES, "public key")?;

        let mut ciphertext = vec![0u8; Self::CIPHERTEXT_BYTES];
        let mut shared_secret = vec![0u8; Self::SHARED_SECRET_BYTES];

        let result = unsafe {
            crate::PQCLEAN_KYBER768_CLEAN_crypto_kem_enc(
                ciphertext.as_mut_ptr() as *mut c_uchar,
                shared_secret.as_mut_ptr() as *mut c_uchar,
                public_key.as_ptr() as *const c_uchar,
            )
        };

        if result != 0 {
            return Err(PqcError::Encapsulation(result));
        }

        Ok((ciphertext, shared_secret))
    }

    /// Decapsulate the shared secret
    pub fn decapsulate(&self, ciphertext: &[u8], secret_key: &[u8]) -> PqcResult<Vec<u8>> {
        validate_length(ciphertext, Self::CIPHERTEXT_BYTES, "ciphertext")?;
        validate_length(secret_key, Self::SECRET_KEY_BYTES, "secret key")?;

        let mut shared_secret = vec![0u8; Self::SHARED_SECRET_BYTES];

        let result = unsafe {
            crate::PQCLEAN_KYBER768_CLEAN_crypto_kem_dec(
                shared_secret.as_mut_ptr() as *mut c_uchar,
                ciphertext.as_ptr() as *const c_uchar,
                secret_key.as_ptr() as *const c_uchar,
            )
        };

        if result != 0 {
            return Err(PqcError::Decapsulation(result));
        }

        Ok(shared_secret)
    }
}

/// Kyber1024 Key Encapsulation Mechanism
/// 
/// Security Level: 5 (equivalent to AES-256)
/// - Public Key: 1568 bytes
/// - Secret Key: 3168 bytes
/// - Ciphertext: 1568 bytes
/// - Shared Secret: 32 bytes
pub struct Kyber1024 {
    _private: (),
}

impl Kyber1024 {
    /// Algorithm constants
    pub const PUBLIC_KEY_BYTES: usize = 1568;
    pub const SECRET_KEY_BYTES: usize = 3168;
    pub const CIPHERTEXT_BYTES: usize = 1568;
    pub const SHARED_SECRET_BYTES: usize = 32;

    /// Create a new Kyber1024 instance
    pub fn new() -> PqcResult<Self> {
        crate::find_binary_path()?;
        Ok(Self { _private: () })
    }

    /// Generate a key pair
    pub fn keypair(&self) -> PqcResult<(Vec<u8>, Vec<u8>)> {
        let mut public_key = vec![0u8; Self::PUBLIC_KEY_BYTES];
        let mut secret_key = vec![0u8; Self::SECRET_KEY_BYTES];

        let result = unsafe {
            crate::PQCLEAN_KYBER1024_CLEAN_crypto_kem_keypair(
                public_key.as_mut_ptr() as *mut c_uchar,
                secret_key.as_mut_ptr() as *mut c_uchar,
            )
        };

        if result != 0 {
            return Err(PqcError::KeyGeneration(result));
        }

        Ok((public_key, secret_key))
    }

    /// Encapsulate a shared secret
    pub fn encapsulate(&self, public_key: &[u8]) -> PqcResult<(Vec<u8>, Vec<u8>)> {
        validate_length(public_key, Self::PUBLIC_KEY_BYTES, "public key")?;

        let mut ciphertext = vec![0u8; Self::CIPHERTEXT_BYTES];
        let mut shared_secret = vec![0u8; Self::SHARED_SECRET_BYTES];

        let result = unsafe {
            crate::PQCLEAN_KYBER1024_CLEAN_crypto_kem_enc(
                ciphertext.as_mut_ptr() as *mut c_uchar,
                shared_secret.as_mut_ptr() as *mut c_uchar,
                public_key.as_ptr() as *const c_uchar,
            )
        };

        if result != 0 {
            return Err(PqcError::Encapsulation(result));
        }

        Ok((ciphertext, shared_secret))
    }

    /// Decapsulate the shared secret
    pub fn decapsulate(&self, ciphertext: &[u8], secret_key: &[u8]) -> PqcResult<Vec<u8>> {
        validate_length(ciphertext, Self::CIPHERTEXT_BYTES, "ciphertext")?;
        validate_length(secret_key, Self::SECRET_KEY_BYTES, "secret key")?;

        let mut shared_secret = vec![0u8; Self::SHARED_SECRET_BYTES];

        let result = unsafe {
            crate::PQCLEAN_KYBER1024_CLEAN_crypto_kem_dec(
                shared_secret.as_mut_ptr() as *mut c_uchar,
                ciphertext.as_ptr() as *const c_uchar,
                secret_key.as_ptr() as *const c_uchar,
            )
        };

        if result != 0 {
            return Err(PqcError::Decapsulation(result));
        }

        Ok(shared_secret)
    }
}

/// Type alias for the default Kyber variant (Kyber768)
pub type Kyber = Kyber768;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kyber512() -> PqcResult<()> {
        let kyber = Kyber512::new()?;
        let (pk, sk) = kyber.keypair()?;
        
        assert_eq!(pk.len(), Kyber512::PUBLIC_KEY_BYTES);
        assert_eq!(sk.len(), Kyber512::SECRET_KEY_BYTES);
        
        let (ct, ss1) = kyber.encapsulate(&pk)?;
        assert_eq!(ct.len(), Kyber512::CIPHERTEXT_BYTES);
        assert_eq!(ss1.len(), Kyber512::SHARED_SECRET_BYTES);
        
        let ss2 = kyber.decapsulate(&ct, &sk)?;
        assert_eq!(ss1, ss2);
        
        Ok(())
    }

    #[test]
    fn test_kyber768() -> PqcResult<()> {
        let kyber = Kyber768::new()?;
        let (pk, sk) = kyber.keypair()?;
        
        assert_eq!(pk.len(), Kyber768::PUBLIC_KEY_BYTES);
        assert_eq!(sk.len(), Kyber768::SECRET_KEY_BYTES);
        
        let (ct, ss1) = kyber.encapsulate(&pk)?;
        assert_eq!(ct.len(), Kyber768::CIPHERTEXT_BYTES);
        assert_eq!(ss1.len(), Kyber768::SHARED_SECRET_BYTES);
        
        let ss2 = kyber.decapsulate(&ct, &sk)?;
        assert_eq!(ss1, ss2);
        
        Ok(())
    }

    #[test]
    fn test_kyber1024() -> PqcResult<()> {
        let kyber = Kyber1024::new()?;
        let (pk, sk) = kyber.keypair()?;
        
        assert_eq!(pk.len(), Kyber1024::PUBLIC_KEY_BYTES);
        assert_eq!(sk.len(), Kyber1024::SECRET_KEY_BYTES);
        
        let (ct, ss1) = kyber.encapsulate(&pk)?;
        assert_eq!(ct.len(), Kyber1024::CIPHERTEXT_BYTES);
        assert_eq!(ss1.len(), Kyber1024::SHARED_SECRET_BYTES);
        
        let ss2 = kyber.decapsulate(&ct, &sk)?;
        assert_eq!(ss1, ss2);
        
        Ok(())
    }
}