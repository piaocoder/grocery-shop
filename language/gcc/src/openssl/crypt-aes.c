#include <stdio.h>
#include <string.h>
#include <openssl/aes.h>
#include <openssl/rand.h>

/* file testaes.cpp */
static void hexdump(FILE *fp, const char *title, 
        const unsigned char *s, int l)
{
int             n = 0;

fprintf(fp, "%s", title);
for (; n < l; ++n) {
if ((n % 16) == 0) {
            fprintf(fp, "\n%04x", n);
}
fprintf(fp, " %02x", s[n]);
}

fprintf(fp, "\n");
}

int main(int argc, char **argv)
{
//256bits key.
unsigned char rkey[16];
//Internal key.
AES_KEY key;

//Testdata.
unsigned char plaintext[AES_BLOCK_SIZE * 4];
unsigned char ciphertext[AES_BLOCK_SIZE * 4];
unsigned char checktext[AES_BLOCK_SIZE * 4];

//Init vector.
unsigned char iv[AES_BLOCK_SIZE * 4];
//Save vector.
unsigned char saved_iv[AES_BLOCK_SIZE * 4];

int nr_of_bits = 0;
int nr_of_bytes = 0;

//Zeror buffer.
memset(plaintext, 0, sizeof plaintext);
memset(ciphertext, 0, sizeof ciphertext);
memset(checktext, 0, sizeof checktext);

//Generate random
RAND_pseudo_bytes(rkey, sizeof rkey);
RAND_pseudo_bytes(plaintext, sizeof plaintext);
RAND_pseudo_bytes(saved_iv, sizeof saved_iv);

hexdump(stdout, "== rkey ==",
rkey,
sizeof(rkey));
hexdump(stdout, "== iv ==",
saved_iv,
sizeof(saved_iv));
printf("\n");

hexdump(stdout, "== plaintext ==",
plaintext,
sizeof(plaintext));
printf("\n");

//Entrypt
memcpy(iv, saved_iv, sizeof(iv));
nr_of_bits = 8 * sizeof(rkey);
AES_set_encrypt_key(rkey, nr_of_bits, &key);
nr_of_bytes = sizeof(plaintext);
AES_cbc_encrypt(plaintext,
ciphertext,
nr_of_bytes,
&key,
iv,
AES_ENCRYPT);

hexdump(stdout, "== ciphertext ==",
ciphertext,
sizeof(ciphertext));
printf("\n");

//Decrypt
memcpy(iv, saved_iv, sizeof(iv));
nr_of_bytes = 8 * sizeof(rkey);
AES_set_decrypt_key(rkey, nr_of_bits, &key);
nr_of_bytes = sizeof(ciphertext) / 2;
//Decrypt in two step:)
AES_cbc_encrypt(ciphertext,
checktext,
nr_of_bytes,
&key, iv,
AES_DECRYPT);
AES_cbc_encrypt(
ciphertext + nr_of_bytes,
checktext + nr_of_bytes,
nr_of_bytes,
&key,
iv,
AES_DECRYPT);
hexdump(stdout, "== checktext ==",
checktext,
sizeof(checktext));
printf("\n");

return 0;
}
