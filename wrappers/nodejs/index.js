/**
 * PQChub - Node.js Wrapper for Post-Quantum Cryptography
 * 
 * This package provides Node.js bindings for post-quantum cryptography algorithms
 * from the PQClean project. It includes Key Encapsulation Mechanisms (KEM) and
 * Digital Signature algorithms.
 * 
 * Key Encapsulation Mechanisms (KEM):
 *     - Kyber512, Kyber768, Kyber1024
 * 
 * Digital Signatures:
 *     - Dilithium2, Dilithium3, Dilithium5
 * 
 * Example usage:
 * 
 *     const { Kyber512, Dilithium2 } = require('pqchub');
 *     
 *     // Key Encapsulation
 *     const kyber = new Kyber512();
 *     const { publicKey, secretKey } = kyber.keypair();
 *     const { ciphertext, sharedSecret } = kyber.encapsulate(publicKey);
 *     const decryptedSecret = kyber.decapsulate(ciphertext, secretKey);
 *     console.assert(Buffer.compare(sharedSecret, decryptedSecret) === 0);
 *     
 *     // Digital Signatures
 *     const dilithium = new Dilithium2();
 *     const keys = dilithium.keypair();
 *     const message = Buffer.from("Hello, post-quantum world!");
 *     const signature = dilithium.sign(message, keys.secretKey);
 *     console.assert(dilithium.verify(message, signature, keys.publicKey));
 */

const { Kyber512, Kyber768, Kyber1024, Kyber } = require('./lib/kyber');
const { Dilithium2, Dilithium3, Dilithium5, Dilithium } = require('./lib/dilithium');
const { 
    getPlatformInfo,
    findBinaryPath,
    PQCError,
    PQCLibraryError,
    PQCKeyGenerationError,
    PQCEncryptionError,
    PQCDecryptionError,
    PQCSignatureError,
    PQCVerificationError,
} = require('./lib/platform');

/**
 * Get information about the PQChub library and available algorithms
 * @returns {Object} Library information
 */
function getInfo() {
    try {
        const platformInfo = getPlatformInfo();
        const binaryPath = findBinaryPath();
        
        // Try to load a library to get version info
        let version = 'Unknown';
        let algorithms = 'Unknown';
        
        try {
            const kyber = new Kyber512();
            if (kyber.lib && kyber.lib.pqchub_get_version) {
                version = kyber.lib.pqchub_get_version();
            }
            if (kyber.lib && kyber.lib.pqchub_get_algorithms) {
                algorithms = kyber.lib.pqchub_get_algorithms().split(',');
            }
        } catch (e) {
            // Ignore errors, use defaults
        }
        
        return {
            version: '1.0.0',
            platform: {
                system: platformInfo.system,
                architecture: platformInfo.architecture,
                binaryPath: binaryPath,
                libraryVersion: version,
                algorithms: algorithms,
            },
            algorithms: {
                kem: ['Kyber512', 'Kyber768', 'Kyber1024'],
                signatures: ['Dilithium2', 'Dilithium3', 'Dilithium5'],
            },
        };
    } catch (error) {
        return {
            version: '1.0.0',
            error: error.message,
            platform: getPlatformInfo(),
        };
    }
}

/**
 * Quick test of all available algorithms
 * @returns {Object} Test results for each algorithm
 */
function testAlgorithms() {
    const results = {};
    
    // Test Kyber algorithms
    for (const KyberClass of [Kyber512, Kyber768, Kyber1024]) {
        try {
            const kyber = new KyberClass();
            const { publicKey, secretKey } = kyber.keypair();
            const { ciphertext, sharedSecret } = kyber.encapsulate(publicKey);
            const decryptedSecret = kyber.decapsulate(ciphertext, secretKey);
            results[KyberClass.name] = Buffer.compare(sharedSecret, decryptedSecret) === 0;
        } catch (error) {
            results[KyberClass.name] = `Error: ${error.message}`;
        }
    }
    
    // Test Dilithium algorithms
    for (const DilithiumClass of [Dilithium2, Dilithium3, Dilithium5]) {
        try {
            const dilithium = new DilithiumClass();
            const { publicKey, secretKey } = dilithium.keypair();
            const message = Buffer.from('Test message');
            const signature = dilithium.sign(message, secretKey);
            results[DilithiumClass.name] = dilithium.verify(message, signature, publicKey);
        } catch (error) {
            results[DilithiumClass.name] = `Error: ${error.message}`;
        }
    }
    
    return results;
}

module.exports = {
    // Version info
    version: '1.0.0',
    
    // Kyber KEM algorithms
    Kyber512,
    Kyber768,
    Kyber1024,
    Kyber, // Default alias for Kyber768
    
    // Dilithium signature algorithms
    Dilithium2,
    Dilithium3,
    Dilithium5,
    Dilithium, // Default alias for Dilithium3
    
    // Utilities
    getPlatformInfo,
    findBinaryPath,
    getInfo,
    testAlgorithms,
    
    // Exceptions
    PQCError,
    PQCLibraryError,
    PQCKeyGenerationError,
    PQCEncryptionError,
    PQCDecryptionError,
    PQCSignatureError,
    PQCVerificationError,
};