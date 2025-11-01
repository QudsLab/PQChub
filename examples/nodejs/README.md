# Node.js Example - PQChub

Auto-downloading Node.js wrapper for Post-Quantum Cryptography.

## Installation

```bash
# Install dependencies
npm install

# Or manually
npm install ffi-napi ref-napi
```

## Requirements

- Node.js 12+
- `ffi-napi` - Foreign Function Interface
- `ref-napi` - Native types for FFI

## Quick Start

```javascript
const { loadLibrary, Falcon512, Falcon1024 } = require('./pqchub');

async function main() {
    // Load library (auto-downloads on first run)
    const lib = await loadLibrary();
    
    // Falcon-512 (NIST Level 1)
    const falcon512 = new Falcon512(lib);
    const { publicKey, secretKey } = falcon512.keypair();
    const signed = falcon512.sign(Buffer.from('Hello World'), secretKey);
    const message = falcon512.verify(signed, publicKey);
    console.log('Message:', message.toString());
    
    // Falcon-1024 (NIST Level 5)
    const falcon1024 = new Falcon1024(lib);
    const keys = falcon1024.keypair();
    const signedMsg = falcon1024.sign(Buffer.from('Top Secret'), keys.secretKey);
    const verified = falcon1024.verify(signedMsg, keys.publicKey);
    console.log('Verified:', verified.toString());
}

main();
```

## Features

### Auto-Download
- Automatically detects your platform (OS + architecture)
- Downloads the correct binary from GitHub
- Caches binary locally at `~/.pqchub/binaries/`
- Only downloads once - subsequent runs use cached version

### Supported Platforms
- Linux (x86_64, aarch64)
- macOS (x86_64, ARM64)
- Windows (x64, x86)
- Android (arm64-v8a, armeabi-v7a, x86_64, x86)

## API Reference

### `loadLibrary()`

Asynchronous function that downloads and loads the PQC library.

```javascript
const lib = await loadLibrary();
// Returns: Native library handle
// Throws: Error if download fails or platform unsupported
```

### `Falcon512`

Fast, compact digital signatures (NIST Level 1).

**Constructor:**
```javascript
const falcon = new Falcon512(lib);
```

**Methods:**

```javascript
// Generate keypair
const { publicKey, secretKey } = falcon.keypair();
// Returns: { publicKey: Buffer, secretKey: Buffer }
//   - publicKey: 897 bytes
//   - secretKey: 1281 bytes

// Sign message
const signedMessage = falcon.sign(message: Buffer, secretKey: Buffer);
// Returns: Buffer - signed message (original + signature)

// Verify signature
const originalMessage = falcon.verify(signedMessage: Buffer, publicKey: Buffer);
// Returns: Buffer - original message if valid
// Throws: Error if signature invalid
```

**Key Sizes:**
- Public Key: 897 bytes
- Secret Key: 1281 bytes
- Signature: ~666 bytes (variable)

### `Falcon1024`

High-security digital signatures (NIST Level 5).

**Constructor:**
```javascript
const falcon = new Falcon1024(lib);
```

**Methods:**

```javascript
// Generate keypair
const { publicKey, secretKey } = falcon.keypair();
// Returns: { publicKey: Buffer, secretKey: Buffer }
//   - publicKey: 1793 bytes
//   - secretKey: 2305 bytes

// Sign message
const signedMessage = falcon.sign(message: Buffer, secretKey: Buffer);
// Returns: Buffer - signed message (original + signature)

// Verify signature
const originalMessage = falcon.verify(signedMessage: Buffer, publicKey: Buffer);
// Returns: Buffer - original message if valid
// Throws: Error if signature invalid
```

**Key Sizes:**
- Public Key: 1793 bytes
- Secret Key: 2305 bytes
- Signature: ~1280 bytes (variable)

## Complete Example

```javascript
const { loadLibrary, Falcon512, Falcon1024 } = require('./pqchub');
const fs = require('fs');

async function main() {
    // Load library
    console.log('Loading PQC library...');
    const lib = await loadLibrary();
    console.log('✅ Library loaded\n');
    
    // Example 1: Falcon-512
    console.log('=== Falcon-512 Example ===');
    const falcon512 = new Falcon512(lib);
    
    const keys512 = falcon512.keypair();
    console.log(`Public key: ${keys512.publicKey.length} bytes`);
    console.log(`Secret key: ${keys512.secretKey.length} bytes`);
    
    const message = Buffer.from('Confidential document');
    console.log(`\nMessage: ${message.toString()}`);
    
    const signed512 = falcon512.sign(message, keys512.secretKey);
    console.log(`Signed: ${signed512.length} bytes`);
    
    const verified512 = falcon512.verify(signed512, keys512.publicKey);
    console.log(`Verified: ${verified512.toString()}`);
    console.log('✅ Falcon-512 signature valid\n');
    
    // Example 2: Falcon-1024
    console.log('=== Falcon-1024 Example ===');
    const falcon1024 = new Falcon1024(lib);
    
    const keys1024 = falcon1024.keypair();
    console.log(`Public key: ${keys1024.publicKey.length} bytes`);
    console.log(`Secret key: ${keys1024.secretKey.length} bytes`);
    
    const topSecret = Buffer.from('Top Secret Data');
    const signed1024 = falcon1024.sign(topSecret, keys1024.secretKey);
    const verified1024 = falcon1024.verify(signed1024, keys1024.publicKey);
    console.log(`Verified: ${verified1024.toString()}`);
    console.log('✅ Falcon-1024 signature valid\n');
    
    // Example 3: Save keys to files
    console.log('=== Saving Keys ===');
    fs.writeFileSync('public.key', keys512.publicKey);
    fs.writeFileSync('secret.key', keys512.secretKey);
    console.log('✅ Keys saved to files');
}

main().catch(console.error);
```

## How It Works

1. **Platform Detection**: `detectPlatform()` identifies your OS and architecture
2. **Metadata Fetch**: Downloads `binaries.json` with binary URLs
3. **Binary Download**: Downloads correct binary to `~/.pqchub/binaries/<platform>/`
4. **Library Loading**: Uses `ffi-napi` to load the native library
5. **FFI Setup**: Configures function signatures for all PQC operations
6. **Ready to Use**: Create `Falcon512` or `Falcon1024` instances

## Caching

Binaries are cached at:
- **Linux/macOS**: `~/.pqchub/binaries/<platform>/`
- **Windows**: `C:\Users\<username>\.pqchub\binaries\<platform>\`

To re-download (e.g., after an update):
```bash
# Remove cache
rm -rf ~/.pqchub/binaries/

# Or on Windows
Remove-Item -Recurse -Force $env:USERPROFILE\.pqchub\binaries
```

## Error Handling

```javascript
async function safeExample() {
    try {
        const lib = await loadLibrary();
        const falcon = new Falcon512(lib);
        const { publicKey, secretKey } = falcon.keypair();
        // ... use keys
    } catch (error) {
        console.error('PQC Error:', error.message);
        // Common issues:
        // - Network error (can't download binary)
        // - Unsupported platform
        // - Invalid signature during verify()
    }
}
```

## Troubleshooting

**Q: `npm install` fails with node-gyp errors?**  
A: Install build tools:
- **Windows**: `npm install --global windows-build-tools`
- **macOS**: Install Xcode Command Line Tools
- **Linux**: `sudo apt-get install build-essential`

**Q: Binary download fails?**  
A: Check internet connection. GitHub raw URLs must be accessible.

**Q: "Unsupported platform" error?**  
A: Your OS/architecture might not be supported yet. Open a GitHub issue.

**Q: Signature verification fails?**  
A: Ensure you're using the same public key that generated the signature.

**Q: Slow first run?**  
A: Binary is downloaded on first use. Subsequent runs are instant (uses cache).

## Using in Web Applications

### Express.js Example

```javascript
const express = require('express');
const { loadLibrary, Falcon512 } = require('./pqchub');

const app = express();
app.use(express.json());

let falcon;

// Initialize library on startup
(async () => {
    const lib = await loadLibrary();
    falcon = new Falcon512(lib);
    
    app.listen(3000, () => {
        console.log('PQC API running on port 3000');
    });
})();

// Generate keypair endpoint
app.get('/keypair', (req, res) => {
    const { publicKey, secretKey } = falcon.keypair();
    res.json({
        publicKey: publicKey.toString('hex'),
        secretKey: secretKey.toString('hex')
    });
});

// Sign message endpoint
app.post('/sign', (req, res) => {
    const message = Buffer.from(req.body.message);
    const secretKey = Buffer.from(req.body.secretKey, 'hex');
    const signed = falcon.sign(message, secretKey);
    res.json({ signed: signed.toString('hex') });
});

// Verify signature endpoint
app.post('/verify', (req, res) => {
    const signed = Buffer.from(req.body.signed, 'hex');
    const publicKey = Buffer.from(req.body.publicKey, 'hex');
    try {
        const message = falcon.verify(signed, publicKey);
        res.json({ valid: true, message: message.toString() });
    } catch (error) {
        res.json({ valid: false, error: error.message });
    }
});
```

## TypeScript Support

Create `pqchub.d.ts`:

```typescript
/// <reference types="node" />

export function loadLibrary(): Promise<any>;

export class Falcon512 {
    constructor(lib: any);
    keypair(): { publicKey: Buffer; secretKey: Buffer };
    sign(message: Buffer, secretKey: Buffer): Buffer;
    verify(signedMessage: Buffer, publicKey: Buffer): Buffer;
}

export class Falcon1024 {
    constructor(lib: any);
    keypair(): { publicKey: Buffer; secretKey: Buffer };
    sign(message: Buffer, secretKey: Buffer): Buffer;
    verify(signedMessage: Buffer, publicKey: Buffer): Buffer;
}
```

## Contributing

Want to improve this wrapper? See the main [CONTRIBUTING](../../CONTRIBUTING.md) guide.

Ideas:
- Add TypeScript definitions
- Add more algorithms (Kyber KEM)
- Improve error messages
- Add streaming API for large files
- Add browser compatibility (WebAssembly)

## License

MIT License - see [LICENSE](../../LICENSE) file.
