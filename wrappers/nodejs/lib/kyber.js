const ffi = require('ffi-napi');
const ref = require('ref-napi');
const { 
    findBinaryPath, 
    validateBufferLength,
    PQCKeyGenerationError,
    PQCEncryptionError,
    PQCDecryptionError,
} = require('./platform');

/**
 * Base class for Kyber algorithms
 */
class BaseKyber {
    constructor(binaryPath = null) {
        this.binaryPath = findBinaryPath(binaryPath);
        this._loadLibrary();
    }
    
    _loadLibrary() {
        try {
            // Define function signatures
            const funcDefs = {};
            
            // Kyber function signatures
            funcDefs[`${this.constructor.FUNC_PREFIX}_crypto_kem_keypair`] = [
                'int', ['pointer', 'pointer']
            ];
            funcDefs[`${this.constructor.FUNC_PREFIX}_crypto_kem_enc`] = [
                'int', ['pointer', 'pointer', 'pointer']
            ];
            funcDefs[`${this.constructor.FUNC_PREFIX}_crypto_kem_dec`] = [
                'int', ['pointer', 'pointer', 'pointer']
            ];
            
            // Library info functions
            funcDefs['pqchub_get_version'] = ['string', []];
            funcDefs['pqchub_get_algorithms'] = ['string', []];
            
            this.lib = ffi.Library(this.binaryPath, funcDefs);
        } catch (error) {
            throw new Error(`Failed to load PQC library from ${this.binaryPath}: ${error.message}`);
        }
    }
    
    /**
     * Generate a key pair for Kyber KEM
     * @returns {Object} Object with publicKey and secretKey properties
     * @throws {PQCKeyGenerationError} If key generation fails
     */
    keypair() {
        const publicKey = Buffer.alloc(this.constructor.PUBLIC_KEY_BYTES);
        const secretKey = Buffer.alloc(this.constructor.SECRET_KEY_BYTES);
        
        const funcName = `${this.constructor.FUNC_PREFIX}_crypto_kem_keypair`;
        const result = this.lib[funcName](publicKey, secretKey);
        
        if (result !== 0) {
            throw new PQCKeyGenerationError(`Key generation failed with code ${result}`);
        }
        
        return {
            publicKey: Buffer.from(publicKey),
            secretKey: Buffer.from(secretKey)
        };
    }
    
    /**
     * Encapsulate a shared secret using the public key
     * @param {Buffer} publicKey - The recipient's public key
     * @returns {Object} Object with ciphertext and sharedSecret properties
     * @throws {PQCEncryptionError} If encapsulation fails
     */
    encapsulate(publicKey) {
        validateBufferLength(publicKey, this.constructor.PUBLIC_KEY_BYTES, 'public key');
        
        const ciphertext = Buffer.alloc(this.constructor.CIPHERTEXT_BYTES);
        const sharedSecret = Buffer.alloc(this.constructor.SHARED_SECRET_BYTES);
        
        const funcName = `${this.constructor.FUNC_PREFIX}_crypto_kem_enc`;
        const result = this.lib[funcName](ciphertext, sharedSecret, publicKey);
        
        if (result !== 0) {
            throw new PQCEncryptionError(`Encapsulation failed with code ${result}`);
        }
        
        return {
            ciphertext: Buffer.from(ciphertext),
            sharedSecret: Buffer.from(sharedSecret)
        };
    }
    
    /**
     * Decapsulate the shared secret using the secret key
     * @param {Buffer} ciphertext - The ciphertext to decapsulate
     * @param {Buffer} secretKey - The recipient's secret key
     * @returns {Buffer} The shared secret
     * @throws {PQCDecryptionError} If decapsulation fails
     */
    decapsulate(ciphertext, secretKey) {
        validateBufferLength(ciphertext, this.constructor.CIPHERTEXT_BYTES, 'ciphertext');
        validateBufferLength(secretKey, this.constructor.SECRET_KEY_BYTES, 'secret key');
        
        const sharedSecret = Buffer.alloc(this.constructor.SHARED_SECRET_BYTES);
        
        const funcName = `${this.constructor.FUNC_PREFIX}_crypto_kem_dec`;
        const result = this.lib[funcName](sharedSecret, ciphertext, secretKey);
        
        if (result !== 0) {
            throw new PQCDecryptionError(`Decapsulation failed with code ${result}`);
        }
        
        return Buffer.from(sharedSecret);
    }
}

/**
 * Kyber512 Key Encapsulation Mechanism
 * 
 * Security Level: 1 (equivalent to AES-128)
 * Public Key: 800 bytes
 * Secret Key: 1632 bytes
 * Ciphertext: 768 bytes
 * Shared Secret: 32 bytes
 */
class Kyber512 extends BaseKyber {
    static PUBLIC_KEY_BYTES = 800;
    static SECRET_KEY_BYTES = 1632;
    static CIPHERTEXT_BYTES = 768;
    static SHARED_SECRET_BYTES = 32;
    static FUNC_PREFIX = 'PQCLEAN_KYBER512_CLEAN';
}

/**
 * Kyber768 Key Encapsulation Mechanism
 * 
 * Security Level: 3 (equivalent to AES-192)
 * Public Key: 1184 bytes
 * Secret Key: 2400 bytes
 * Ciphertext: 1088 bytes
 * Shared Secret: 32 bytes
 */
class Kyber768 extends BaseKyber {
    static PUBLIC_KEY_BYTES = 1184;
    static SECRET_KEY_BYTES = 2400;
    static CIPHERTEXT_BYTES = 1088;
    static SHARED_SECRET_BYTES = 32;
    static FUNC_PREFIX = 'PQCLEAN_KYBER768_CLEAN';
}

/**
 * Kyber1024 Key Encapsulation Mechanism
 * 
 * Security Level: 5 (equivalent to AES-256)
 * Public Key: 1568 bytes
 * Secret Key: 3168 bytes
 * Ciphertext: 1568 bytes
 * Shared Secret: 32 bytes
 */
class Kyber1024 extends BaseKyber {
    static PUBLIC_KEY_BYTES = 1568;
    static SECRET_KEY_BYTES = 3168;
    static CIPHERTEXT_BYTES = 1568;
    static SHARED_SECRET_BYTES = 32;
    static FUNC_PREFIX = 'PQCLEAN_KYBER1024_CLEAN';
}

module.exports = {
    BaseKyber,
    Kyber512,
    Kyber768,
    Kyber1024,
    Kyber: Kyber768, // Default alias
};