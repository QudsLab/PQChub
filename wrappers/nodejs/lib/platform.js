const os = require('os');
const path = require('path');
const fs = require('fs');

/**
 * Get current platform information for binary selection
 * @returns {Object} Platform information
 */
function getPlatformInfo() {
    const platform = os.platform();
    const arch = os.arch();
    
    let system, architecture;
    
    // Normalize system name
    switch (platform) {
        case 'win32':
            system = 'windows';
            break;
        case 'darwin':
            system = 'macos';
            break;
        case 'linux':
            system = 'linux';
            break;
        default:
            system = platform;
    }
    
    // Normalize architecture
    switch (arch) {
        case 'x64':
            architecture = system === 'windows' ? 'x64' : 'x86_64';
            break;
        case 'arm64':
            architecture = system === 'macos' ? 'arm64' : 'aarch64';
            break;
        case 'ia32':
            architecture = 'x86';
            break;
        default:
            architecture = arch;
    }
    
    return { system, architecture };
}

/**
 * Get the library file name for the given system
 * @param {string} system - Operating system name
 * @returns {string} Library file name
 */
function getLibraryName(system) {
    switch (system) {
        case 'windows':
            return 'pqc.dll';
        case 'macos':
            return 'libpqc.dylib';
        default:
            return 'libpqc.so';
    }
}

/**
 * Find the PQC native library for the current platform
 * @param {string|null} customPath - Optional custom path to binary
 * @returns {string} Path to the native library
 * @throws {Error} If library not found
 */
function findBinaryPath(customPath = null) {
    if (customPath) {
        if (fs.existsSync(customPath)) {
            return path.resolve(customPath);
        } else {
            throw new Error(`Custom binary path not found: ${customPath}`);
        }
    }
    
    const { system, architecture } = getPlatformInfo();
    
    // Determine platform directory name
    let platformDir;
    if (system === 'macos') {
        platformDir = `macos-${architecture}`;
    } else if (system === 'windows') {
        if (architecture === 'x86_64' || architecture === 'x64') {
            platformDir = 'windows-x64';
        } else if (architecture === 'x86') {
            platformDir = 'windows-x86';
        } else {
            throw new Error(`Unsupported Windows architecture: ${architecture}`);
        }
    } else if (system === 'linux') {
        platformDir = `linux-${architecture}`;
    } else {
        throw new Error(`Unsupported operating system: ${system}`);
    }
    
    const libName = getLibraryName(system);
    
    // Find the binary path relative to this module
    const moduleDir = __dirname;
    const repoRoot = path.resolve(moduleDir, '..', '..');
    const binaryPath = path.join(repoRoot, 'bins', platformDir, libName);
    
    if (!fs.existsSync(binaryPath)) {
        // Try alternative paths
        const alternativePaths = [
            // If running from within the wrapper directory
            path.resolve(moduleDir, '..', '..', 'bins', platformDir, libName),
            // If installed globally
            path.join(process.env.PREFIX || '/usr/local', 'share', 'pqchub', 'bins', platformDir, libName),
        ];
        
        let found = false;
        for (const altPath of alternativePaths) {
            if (fs.existsSync(altPath)) {
                return path.resolve(altPath);
            }
        }
        
        throw new Error(
            `PQC native library not found for platform ${platformDir}.\n` +
            `Expected: ${binaryPath}\n` +
            `Make sure you have cloned the repository with Git LFS enabled.\n` +
            `Current platform: ${system} ${architecture}`
        );
    }
    
    return path.resolve(binaryPath);
}

/**
 * Validate buffer length
 * @param {Buffer} buffer - Buffer to validate
 * @param {number} expectedLength - Expected length
 * @param {string} type - Type description for error messages
 * @throws {Error} If validation fails
 */
function validateBufferLength(buffer, expectedLength, type = 'buffer') {
    if (!Buffer.isBuffer(buffer)) {
        throw new TypeError(`${type} must be a Buffer`);
    }
    
    if (buffer.length !== expectedLength) {
        throw new Error(
            `${type} must be exactly ${expectedLength} bytes, ` +
            `got ${buffer.length} bytes`
        );
    }
}

/**
 * Validate message input
 * @param {Buffer} message - Message to validate
 * @throws {Error} If validation fails
 */
function validateMessage(message) {
    if (!Buffer.isBuffer(message)) {
        throw new TypeError('Message must be a Buffer');
    }
}

/**
 * Custom error classes
 */
class PQCError extends Error {
    constructor(message) {
        super(message);
        this.name = 'PQCError';
    }
}

class PQCLibraryError extends PQCError {
    constructor(message) {
        super(message);
        this.name = 'PQCLibraryError';
    }
}

class PQCKeyGenerationError extends PQCError {
    constructor(message) {
        super(message);
        this.name = 'PQCKeyGenerationError';
    }
}

class PQCEncryptionError extends PQCError {
    constructor(message) {
        super(message);
        this.name = 'PQCEncryptionError';
    }
}

class PQCDecryptionError extends PQCError {
    constructor(message) {
        super(message);
        this.name = 'PQCDecryptionError';
    }
}

class PQCSignatureError extends PQCError {
    constructor(message) {
        super(message);
        this.name = 'PQCSignatureError';
    }
}

class PQCVerificationError extends PQCError {
    constructor(message) {
        super(message);
        this.name = 'PQCVerificationError';
    }
}

module.exports = {
    getPlatformInfo,
    getLibraryName,
    findBinaryPath,
    validateBufferLength,
    validateMessage,
    PQCError,
    PQCLibraryError,
    PQCKeyGenerationError,
    PQCEncryptionError,
    PQCDecryptionError,
    PQCSignatureError,
    PQCVerificationError,
};