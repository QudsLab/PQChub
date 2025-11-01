/*
 * PQChub C Binary Test
 * Simple test for direct library usage from C
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Falcon-512 function declarations
int PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair(unsigned char *pk, unsigned char *sk);
int PQCLEAN_FALCON512_CLEAN_crypto_sign(unsigned char *sm, size_t *smlen,
                                         const unsigned char *m, size_t mlen,
                                         const unsigned char *sk);
int PQCLEAN_FALCON512_CLEAN_crypto_sign_open(unsigned char *m, size_t *mlen,
                                              const unsigned char *sm, size_t smlen,
                                              const unsigned char *pk);

// Library info functions
const char* pqchub_get_version(void);
const char* pqchub_get_platform(void);

#define FALCON512_PUBLICKEYBYTES 897
#define FALCON512_SECRETKEYBYTES 1281
#define FALCON512_BYTES 666

int main() {
    printf("==========================================================\n");
    printf("PQChub C Binary Test\n");
    printf("==========================================================\n\n");
    
    // Test library info
    printf("Library version: %s\n", pqchub_get_version());
    printf("Platform: %s\n", pqchub_get_platform());
    
    printf("\n[TEST] Falcon-512 Digital Signature\n");
    
    // Allocate buffers
    unsigned char *public_key = malloc(FALCON512_PUBLICKEYBYTES);
    unsigned char *secret_key = malloc(FALCON512_SECRETKEYBYTES);
    
    if (!public_key || !secret_key) {
        printf("  [FAILED] Memory allocation failed\n");
        return 1;
    }
    
    // Generate keypair
    int result = PQCLEAN_FALCON512_CLEAN_crypto_sign_keypair(public_key, secret_key);
    if (result != 0) {
        printf("  [FAILED] Keypair generation failed: %d\n", result);
        free(public_key);
        free(secret_key);
        return 1;
    }
    printf("  [OK] Keypair generated\n");
    
    // Sign message
    const char *message = "Test message from C";
    size_t message_len = strlen(message);
    unsigned char *signed_msg = malloc(message_len + FALCON512_BYTES);
    size_t signed_len;
    
    if (!signed_msg) {
        printf("  [FAILED] Memory allocation failed\n");
        free(public_key);
        free(secret_key);
        return 1;
    }
    
    result = PQCLEAN_FALCON512_CLEAN_crypto_sign(
        signed_msg, &signed_len,
        (unsigned char*)message, message_len,
        secret_key
    );
    
    if (result != 0) {
        printf("  [FAILED] Signing failed: %d\n", result);
        free(public_key);
        free(secret_key);
        free(signed_msg);
        return 1;
    }
    printf("  [OK] Message signed (signature size: %zu bytes)\n", signed_len);
    
    // Verify signature
    unsigned char *verified_msg = malloc(message_len);
    size_t verified_len;
    
    if (!verified_msg) {
        printf("  [FAILED] Memory allocation failed\n");
        free(public_key);
        free(secret_key);
        free(signed_msg);
        return 1;
    }
    
    result = PQCLEAN_FALCON512_CLEAN_crypto_sign_open(
        verified_msg, &verified_len,
        signed_msg, signed_len,
        public_key
    );
    
    if (result != 0) {
        printf("  [FAILED] Verification failed: %d\n", result);
        free(public_key);
        free(secret_key);
        free(signed_msg);
        free(verified_msg);
        return 1;
    }
    
    // Check if message matches
    if (verified_len != message_len || memcmp(verified_msg, message, message_len) != 0) {
        printf("  [FAILED] Verified message doesn't match original\n");
        free(public_key);
        free(secret_key);
        free(signed_msg);
        free(verified_msg);
        return 1;
    }
    
    printf("  [OK] Signature verified\n");
    printf("  [SUCCESS] Falcon-512 test passed\n");
    
    // Clean up
    free(public_key);
    free(secret_key);
    free(signed_msg);
    free(verified_msg);
    
    printf("\n==========================================================\n");
    printf("[SUCCESS] All C tests passed!\n");
    printf("==========================================================\n");
    
    return 0;
}
