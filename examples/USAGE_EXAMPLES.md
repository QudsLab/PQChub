# PQChub Example: Python Kyber KEM

This example demonstrates how to use the Python wrapper to perform key encapsulation and decapsulation with Kyber512.

```python
from pqchub import Kyber512

# Create Kyber512 instance
kyber = Kyber512()

# Generate keypair
public_key, secret_key = kyber.keypair()
print(f"Public key: {public_key.hex()}")
print(f"Secret key: {secret_key.hex()}")

# Encapsulate shared secret
ciphertext, shared_secret = kyber.encapsulate(public_key)
print(f"Ciphertext: {ciphertext.hex()}")
print(f"Shared secret: {shared_secret.hex()}")

# Decapsulate shared secret
recovered_secret = kyber.decapsulate(ciphertext, secret_key)
print(f"Recovered secret: {recovered_secret.hex()}")

assert shared_secret == recovered_secret
print("✅ Kyber KEM roundtrip successful!")
```

---

# PQChub Example: Python Dilithium Signature

This example demonstrates how to use the Python wrapper to sign and verify messages with Dilithium2.

```python
from pqchub import Dilithium2

# Create Dilithium2 instance
dilithium = Dilithium2()

# Generate keypair
public_key, secret_key = dilithium.keypair()
print(f"Public key: {public_key.hex()}")
print(f"Secret key: {secret_key.hex()}")

# Sign a message
message = b"Hello, PQChub!"
signature = dilithium.sign(message, secret_key)
print(f"Signature: {signature.hex()}")

# Verify the signature
is_valid = dilithium.verify(message, signature, public_key)
print(f"Signature valid: {is_valid}")

assert is_valid
print("✅ Dilithium signature roundtrip successful!")
```

---

# PQChub Example: Node.js Kyber KEM

This example demonstrates how to use the Node.js wrapper to perform key encapsulation and decapsulation with Kyber512.

```javascript
const { Kyber512 } = require('./index.js');

const kyber = new Kyber512();

// Generate keypair
const { publicKey, secretKey } = kyber.keypair();
console.log('Public key:', publicKey.toString('hex'));
console.log('Secret key:', secretKey.toString('hex'));

// Encapsulate shared secret
const { ciphertext, sharedSecret } = kyber.encapsulate(publicKey);
console.log('Ciphertext:', ciphertext.toString('hex'));
console.log('Shared secret:', sharedSecret.toString('hex'));

// Decapsulate shared secret
const recoveredSecret = kyber.decapsulate(ciphertext, secretKey);
console.log('Recovered secret:', recoveredSecret.toString('hex'));

console.assert(sharedSecret.equals(recoveredSecret));
console.log('✅ Kyber KEM roundtrip successful!');
```

---

# PQChub Example: Node.js Dilithium Signature

This example demonstrates how to use the Node.js wrapper to sign and verify messages with Dilithium2.

```javascript
const { Dilithium2 } = require('./index.js');

const dilithium = new Dilithium2();

// Generate keypair
const { publicKey, secretKey } = dilithium.keypair();
console.log('Public key:', publicKey.toString('hex'));
console.log('Secret key:', secretKey.toString('hex'));

// Sign a message
const message = Buffer.from('Hello, PQChub!');
const signature = dilithium.sign(message, secretKey);
console.log('Signature:', signature.toString('hex'));

// Verify the signature
const isValid = dilithium.verify(message, signature, publicKey);
console.log('Signature valid:', isValid);

console.assert(isValid);
console.log('✅ Dilithium signature roundtrip successful!');
```

---

# PQChub Example: Go Kyber KEM

This example demonstrates how to use the Go wrapper to perform key encapsulation and decapsulation with Kyber512.

```go
package main

import (
    "fmt"
    "github.com/qudslab/pqchub/wrappers/go/pqc"
)

func main() {
    kyber := pqc.NewKyber512()
    publicKey, secretKey := kyber.Keypair()
    fmt.Printf("Public key: %x\n", publicKey)
    fmt.Printf("Secret key: %x\n", secretKey)

    ciphertext, sharedSecret := kyber.Encapsulate(publicKey)
    fmt.Printf("Ciphertext: %x\n", ciphertext)
    fmt.Printf("Shared secret: %x\n", sharedSecret)

    recoveredSecret := kyber.Decapsulate(ciphertext, secretKey)
    fmt.Printf("Recovered secret: %x\n", recoveredSecret)

    if string(sharedSecret) == string(recoveredSecret) {
        fmt.Println("✅ Kyber KEM roundtrip successful!")
    } else {
        fmt.Println("❌ Roundtrip failed!")
    }
}
```

---

# PQChub Example: Rust Kyber KEM

This example demonstrates how to use the Rust wrapper to perform key encapsulation and decapsulation with Kyber512.

```rust
use pqchub::kyber::Kyber512;

fn main() {
    let kyber = Kyber512::new().unwrap();
    let (public_key, secret_key) = kyber.keypair().unwrap();
    println!("Public key: {:x?}", public_key);
    println!("Secret key: {:x?}", secret_key);

    let (ciphertext, shared_secret) = kyber.encapsulate(&public_key).unwrap();
    println!("Ciphertext: {:x?}", ciphertext);
    println!("Shared secret: {:x?}", shared_secret);

    let recovered_secret = kyber.decapsulate(&ciphertext, &secret_key).unwrap();
    println!("Recovered secret: {:x?}", recovered_secret);

    assert_eq!(shared_secret, recovered_secret);
    println!("✅ Kyber KEM roundtrip successful!");
}
```

---

# PQChub Example: Rust Dilithium Signature

This example demonstrates how to use the Rust wrapper to sign and verify messages with Dilithium2.

```rust
use pqchub::dilithium::Dilithium2;

fn main() {
    let dilithium = Dilithium2::new().unwrap();
    let (public_key, secret_key) = dilithium.keypair().unwrap();
    println!("Public key: {:x?}", public_key);
    println!("Secret key: {:x?}", secret_key);

    let message = b"Hello, PQChub!";
    let signature = dilithium.sign(message, &secret_key).unwrap();
    println!("Signature: {:x?}", signature);

    let is_valid = dilithium.verify(message, &signature, &public_key).unwrap();
    println!("Signature valid: {}", is_valid);

    assert!(is_valid);
    println!("✅ Dilithium signature roundtrip successful!");
}
```

---

For more examples and advanced usage, see the [API documentation](./API.md) and language-specific wrapper directories.