const ffi = require('ffi-napi');
const ref = require('ref-napi');
const { 
    findBinaryPath, 
    validateBufferLength,
    validateMessage,
    PQCKeyGenerationError,
    PQCSignatureError,
} = require('./platform');

/**
 * Base class for Dilithium signature algorithms
 */
class BaseDilithium {
    constructor(binaryPath = null) {
        this.binaryPath = findBinaryPath(binaryPath);
        this._loadLibrary();
    }
    
    _loadLibrary() {
        try {
            // Define function signatures
            const funcDefs = {};
            
            // Dilithium function signatures
            funcDefs[`${this.constructor.FUNC_PREFIX}_crypto_sign_keypair`] = [
                'int', ['pointer', 'pointer']
            ];
            funcDefs[`${this.constructor.FUNC_PREFIX}_crypto_sign_signature`] = [
                'int', ['pointer', 'pointer', 'pointer', 'size_t', 'pointer']
            ];
            funcDefs[`${this.constructor.FUNC_PREFIX}_crypto_sign_verify`] = [
                'int', ['pointer', 'size_t', 'pointer', 'size_t', 'pointer']
            ];
            
            this.lib = ffi.Library(this.binaryPath, funcDefs);
        } catch (error) {
            throw new Error(`Failed to load PQC library from ${this.binaryPath}: ${error.message}`);
        }
    }
    
    /**
     * Generate a key pair for Dilithium signatures
     * @returns {Object} Object with publicKey and secretKey properties
     * @throws {PQCKeyGenerationError} If key generation fails
     */
    keypair() {
        const publicKey = Buffer.alloc(this.constructor.PUBLIC_KEY_BYTES);
        const secretKey = Buffer.alloc(this.constructor.SECRET_KEY_BYTES);
        
        const funcName = `${this.constructor.FUNC_PREFIX}_crypto_sign_keypair`;
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
     * Sign a message using Dilithium
     * @param {Buffer} message - The message to sign
     * @param {Buffer} secretKey - The signer's secret key
     * @returns {Buffer} The signature bytes
     * @throws {PQCSignatureError} If signing fails
     */
    sign(message, secretKey) {
        validateMessage(message);
        validateBufferLength(secretKey, this.constructor.SECRET_KEY_BYTES, 'secret key');
        
        const signature = Buffer.alloc(this.constructor.SIGNATURE_BYTES);
        const signatureLength = ref.alloc('size_t');
        
        const funcName = `${this.constructor.FUNC_PREFIX}_crypto_sign_signature`;
        const result = this.lib[funcName](
            signature,
            signatureLength,
            message,
            message.length,
            secretKey
        );
        
        if (result !== 0) {
            throw new PQCSignatureError(`Signature generation failed with code ${result}`);
        }
        
        // Return only the actual signature length
        const actualLength = signatureLength.deref();
        return Buffer.from(signature.subarray(0, actualLength));
    }
    
    /**
     * Verify a signature using Dilithium
     * @param {Buffer} message - The original message
     * @param {Buffer} signature - The signature to verify
     * @param {Buffer} publicKey - The signer's public key
     * @returns {boolean} True if signature is valid, false otherwise
     */
    verify(message, signature, publicKey) {
        validateMessage(message);
        validateBufferLength(publicKey, this.constructor.PUBLIC_KEY_BYTES, 'public key');
        
        if (!Buffer.isBuffer(signature)) {
            throw new TypeError('Signature must be a Buffer');
        }
        
        const funcName = `${this.constructor.FUNC_PREFIX}_crypto_sign_verify`;
        const result = this.lib[funcName](
            signature,
            signature.length,
            message,
            message.length,
            publicKey
        );
        
        // Return value: 0 = valid signature, non-zero = invalid signature
        return result === 0;
    }
}

/**
 * Dilithium2 Digital Signature Algorithm
 * 
 * Security Level: 1 (equivalent to AES-128)
 * Public Key: 1312 bytes
 * Secret Key: 2528 bytes
 * Signature: ~2420 bytes (variable)
 */
class Dilithium2 extends BaseDilithium {
    static PUBLIC_KEY_BYTES = 1312;
    static SECRET_KEY_BYTES = 2528;
    static SIGNATURE_BYTES = 2420;
    static FUNC_PREFIX = 'PQCLEAN_DILITHIUM2_CLEAN';
}

/**
 * Dilithium3 Digital Signature Algorithm
 * 
 * Security Level: 3 (equivalent to AES-192)
 * Public Key: 1952 bytes
 * Secret Key: 4000 bytes
 * Signature: ~3293 bytes (variable)
 */
class Dilithium3 extends BaseDilithium {
    static PUBLIC_KEY_BYTES = 1952;
    static SECRET_KEY_BYTES = 4000;
    static SIGNATURE_BYTES = 3293;
    static FUNC_PREFIX = 'PQCLEAN_DILITHIUM3_CLEAN';
}

/**
 * Dilithium5 Digital Signature Algorithm
 * 
 * Security Level: 5 (equivalent to AES-256)
 * Public Key: 2592 bytes
 * Secret Key: 4864 bytes
 * Signature: ~4595 bytes (variable)
 */
class Dilithium5 extends BaseDilithium {
    static PUBLIC_KEY_BYTES = 2592;
    static SECRET_KEY_BYTES = 4864;
    static SIGNATURE_BYTES = 4595;
    static FUNC_PREFIX = 'PQCLEAN_DILITHIUM5_CLEAN';
}

module.exports = {
    BaseDilithium,
    Dilithium2,
    Dilithium3,
    Dilithium5,
    Dilithium: Dilithium3, // Default alias
};