#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/aes.h>
#include <openssl/rand.h>

__attribute__((unused))
static void hexdump(FILE *f, const char *title, 
        const unsigned char *s, int l)
{
    int         n = 0;
    fprintf(f, "%s", title);
    for (; n<1; ++n) {
        if ((n%16) == 0) {
            fprintf(f, "\n%04x", n);
        }
        fprintf(f, " %02x", s[n]);
    }
    fprintf(f, "\n");
}

int
main(int argc, char **argv)
{
    unsigned char   rkey[16];
    AES_KEY         key;
    unsigned char iv[AES_BLOCK_SIZE * 4];
    unsigned char saved_iv[AES_BLOCK_SIZE * 4];
    int             nr_of_bits = 0;
    int             nr_of_bytes = 0;
    int             num;
    
    unsigned char   plaintext[AES_BLOCK_SIZE * 4];
    unsigned char   ciphertext[AES_BLOCK_SIZE * 4];
    unsigned char   checktext[AES_BLOCK_SIZE * 4];

    memset(plaintext, 0, sizeof plaintext);
    memset(ciphertext, 0, sizeof ciphertext);
    memset(checktext, 0, sizeof checktext); 

    RAND_pseudo_bytes(plaintext, sizeof plaintext);
    RAND_pseudo_bytes(rkey, sizeof rkey);
    RAND_pseudo_bytes(saved_iv, sizeof saved_iv);

    num = 0;
    memcpy(iv, saved_iv, sizeof(iv));
    nr_of_bits = 8 * sizeof(rkey);
    AES_set_encrypt_key(rkey, nr_of_bits, &key);
    nr_of_bytes = sizeof(ciphertext) / 2;
    AES_cfb128_encrypt(ciphertext, checktext, nr_of_bytes, &key, iv, &num, AES_ENCRYPT);

    num = 0;
    memcpy(iv, saved_iv, sizeof(iv));
    nr_of_bits = 8 * sizeof(rkey);
    AES_set_decrypt_key(rkey, nr_of_bits, &key);
    AES_cfb128_encrypt(ciphertext + nr_of_bytes, checktext + nr_of_bytes,
                        nr_of_bytes, &key, iv, &num, AES_DECRYPT);

    printf("字符串为:%s\n", checktext);

    return 0;
}
