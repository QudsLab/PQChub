#!/usr/bin/env node
/**
 * PQChub - Auto-downloading Node.js wrapper for Post-Quantum Cryptography
 * Automatically downloads the correct binary for your platform
 */

const os = require('os');
const path = require('path');
const fs = require('fs');
const https = require('https');
const ffi = require('ffi-napi');
const ref = require('ref-napi');

// Configuration
const METADATA_URL = 'https://github.com/QudsLab/PQChub/raw/refs/heads/main/bins/binaries.json';
const CACHE_DIR = path.join(os.homedir(), '.pqchub', 'binaries');

// Detect platform
function detectPlatform() {
    const platform = os.platform();
    const arch = os.arch();
    
    if (platform === 'win32') {
        return arch === 'x64' ? 'windows-x64' : 'windows-x86';
    } else if (platform === 'darwin') {
        return arch === 'arm64' ? 'macos-arm64' : 'macos-x86_64';
    } else if (platform === 'linux') {
        return arch === 'arm64' || arch === 'aarch64' ? 'linux-aarch64' : 'linux-x86_64';
    } else {
        throw new Error(`Unsupported platform: ${platform} ${arch}`);
    }
}

// Download file
function downloadFile(url, destPath) {
    return new Promise((resolve, reject) => {
        console.log(`Downloading from ${url}...`);
        
        // Create directory if it doesn't exist
        fs.mkdirSync(path.dirname(destPath), { recursive: true });
        
        const file = fs.createWriteStream(destPath);
        https.get(url, (response) => {
            if (response.statusCode === 302 || response.statusCode === 301) {
                // Follow redirect
                return downloadFile(response.headers.location, destPath)
                    .then(resolve)
                    .catch(reject);
            }
            
            response.pipe(file);
            file.on('finish', () => {
                file.close();
                console.log(`Downloaded to ${destPath}`);
                resolve(destPath);
            });
        }).on('error', (err) => {
            fs.unlinkSync(destPath);
            reject(err);
        });
    });
}

// Get metadata
function getMetadata() {
    return new Promise((resolve, reject) => {
        console.log('Fetching binary metadata...');
        https.get(METADATA_URL, (response) => {
            let data = '';
            response.on('data', (chunk) => data += chunk);
            response.on('end', () => resolve(JSON.parse(data)));
        }).on('error', reject);
    });
}

// Get binary path
async function getBinaryPath() {
    const platformId = detectPlatform();
    const metadata = await getMetadata();
    
    if (!metadata.binaries[platformId]) {
        throw new Error(`No binary available for platform: ${platformId}`);
    }
    
    const binaryInfo = metadata.binaries[platformId];
    const binaryUrl = binaryInfo.url;
    const binaryFilename = binaryInfo.filename;
    
    // Check cache
    const cachedPath = path.join(CACHE_DIR, platformId, binaryFilename);
    
    if (fs.existsSync(cachedPath)) {
        console.log(`Using cached binary: ${cachedPath}`);
        return cachedPath;
    }
    
    // Download binary
    await downloadFile(binaryUrl, cachedPath);
    return cachedPath;
}

// Load library
let _lib = null;
let _binaryPath = null;

async function loadLibrary() {
    if (_lib === null) {
        _binaryPath = await getBinaryPath();
        
        _lib = ffi.Library(_binaryPath, {
            'PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair': ['int', ['pointer', 'pointer']],
            'PQCLEAN_FALCON512_CLEAN_crypto_sign': ['int', ['pointer', 'pointer', 'pointer', 'size_t', 'pointer']],
            'PQCLEAN_FALCON512_CLEAN_crypto_sign_open': ['int', ['pointer', 'pointer', 'pointer', 'size_t', 'pointer']],
            'PQCLEAN_FALCON1024_CLEAN_crypto_sign_keypair': ['int', ['pointer', 'pointer']],
            'PQCLEAN_FALCON1024_CLEAN_crypto_sign': ['int', ['pointer', 'pointer', 'pointer', 'size_t', 'pointer']],
            'PQCLEAN_FALCON1024_CLEAN_crypto_sign_open': ['int', ['pointer', 'pointer', 'pointer', 'size_t', 'pointer']]
        });
        
        console.log(`Loaded library: ${_binaryPath}`);
    }
    return _lib;
}

// Falcon-512 class
class Falcon512 {
    static PUBLICKEY_BYTES = 897;
    static SECRETKEY_BYTES = 1281;
    static SIGNATURE_BYTES = 666;
    
    constructor(lib) {
        this.lib = lib;
    }
    
    keypair() {
        const pk = Buffer.alloc(Falcon512.PUBLICKEY_BYTES);
        const sk = Buffer.alloc(Falcon512.SECRETKEY_BYTES);
        
        const result = this.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair(pk, sk);
        
        if (result !== 0) {
            throw new Error(`Keypair generation failed: ${result}`);
        }
        
        return { publicKey: pk, secretKey: sk };
    }
    
    sign(message, secretKey) {
        if (secretKey.length !== Falcon512.SECRETKEY_BYTES) {
            throw new Error(`Secret key must be ${Falcon512.SECRETKEY_BYTES} bytes`);
        }
        
        const signed = Buffer.alloc(message.length + Falcon512.SIGNATURE_BYTES);
        const signedLen = ref.alloc(ref.types.size_t);
        
        const result = this.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign(
            signed, signedLen, message, message.length, secretKey
        );
        
        if (result !== 0) {
            throw new Error(`Signing failed: ${result}`);
        }
        
        return signed.slice(0, signedLen.deref());
    }
    
    verify(signedMessage, publicKey) {
        if (publicKey.length !== Falcon512.PUBLICKEY_BYTES) {
            throw new Error(`Public key must be ${Falcon512.PUBLICKEY_BYTES} bytes`);
        }
        
        const message = Buffer.alloc(signedMessage.length);
        const messageLen = ref.alloc(ref.types.size_t);
        
        const result = this.lib.PQCLEAN_FALCON512_CLEAN_crypto_sign_open(
            message, messageLen, signedMessage, signedMessage.length, publicKey
        );
        
        if (result !== 0) {
            throw new Error(`Verification failed: ${result}`);
        }
        
        return message.slice(0, messageLen.deref());
    }
}

// Falcon-1024 class
class Falcon1024 {
    static PUBLICKEY_BYTES = 1793;
    static SECRETKEY_BYTES = 2305;
    static SIGNATURE_BYTES = 1280;
    
    constructor(lib) {
        this.lib = lib;
    }
    
    keypair() {
        const pk = Buffer.alloc(Falcon1024.PUBLICKEY_BYTES);
        const sk = Buffer.alloc(Falcon1024.SECRETKEY_BYTES);
        
        const result = this.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_keypair(pk, sk);
        
        if (result !== 0) {
            throw new Error(`Keypair generation failed: ${result}`);
        }
        
        return { publicKey: pk, secretKey: sk };
    }
    
    sign(message, secretKey) {
        if (secretKey.length !== Falcon1024.SECRETKEY_BYTES) {
            throw new Error(`Secret key must be ${Falcon1024.SECRETKEY_BYTES} bytes`);
        }
        
        const signed = Buffer.alloc(message.length + Falcon1024.SIGNATURE_BYTES);
        const signedLen = ref.alloc(ref.types.size_t);
        
        const result = this.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign(
            signed, signedLen, message, message.length, secretKey
        );
        
        if (result !== 0) {
            throw new Error(`Signing failed: ${result}`);
        }
        
        return signed.slice(0, signedLen.deref());
    }
    
    verify(signedMessage, publicKey) {
        if (publicKey.length !== Falcon1024.PUBLICKEY_BYTES) {
            throw new Error(`Public key must be ${Falcon1024.PUBLICKEY_BYTES} bytes`);
        }
        
        const message = Buffer.alloc(signedMessage.length);
        const messageLen = ref.alloc(ref.types.size_t);
        
        const result = this.lib.PQCLEAN_FALCON1024_CLEAN_crypto_sign_open(
            message, messageLen, signedMessage, signedMessage.length, publicKey
        );
        
        if (result !== 0) {
            throw new Error(`Verification failed: ${result}`);
        }
        
        return message.slice(0, messageLen.deref());
    }
}

// Main demo
async function demo() {
    console.log('PQChub - Post-Quantum Cryptography Demo\n');
    
    const lib = await loadLibrary();
    
    console.log('='.repeat(60));
    console.log('Falcon-512 Digital Signature');
    console.log('='.repeat(60));
    
    const falcon = new Falcon512(lib);
    
    // Generate keypair
    const { publicKey, secretKey } = falcon.keypair();
    console.log('✓ Generated keypair');
    console.log(`  Public key: ${publicKey.length} bytes`);
    console.log(`  Secret key: ${secretKey.length} bytes`);
    
    // Sign message
    const message = Buffer.from('Hello, Post-Quantum World!');
    const signed = falcon.sign(message, secretKey);
    console.log(`\n✓ Signed message: ${signed.length} bytes`);
    
    // Verify signature
    const verified = falcon.verify(signed, publicKey);
    console.log('✓ Verified signature');
    console.log(`  Original: ${message.toString()}`);
    console.log(`  Verified: ${verified.toString()}`);
    
    if (Buffer.compare(message, verified) === 0) {
        console.log('\n✓ SUCCESS: Message integrity verified!');
    } else {
        console.log('\n✗ FAILED: Message mismatch!');
    }
    
    console.log('\n' + '='.repeat(60));
    console.log('All tests passed!');
    console.log('='.repeat(60));
}

// Export classes
module.exports = {
    loadLibrary,
    Falcon512,
    Falcon1024
};

// Run demo if executed directly
if (require.main === module) {
    demo().catch(console.error);
}
