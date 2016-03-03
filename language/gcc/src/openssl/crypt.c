#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <openssl/rc4.h>
#include <openssl/bio.h>
#include <openssl/evp.h>

#include "crypt.h"

RC4_KEY   encryptKey;    // encrypt key
RC4_KEY   decryptKey;    // decrypt key


/*
 * initialize
 */
void
topwaf_crypt_base64_init()
{
    unsigned char const key_data[8] = { 0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef };

    RC4_set_key(&encryptKey, sizeof(key_data), key_data);
    RC4_set_key(&decryptKey, sizeof(key_data), key_data);
}

/*
 * argument:
 *      src:                primary string
 *      dst:                value after encrypt and base64
 */
int
waf_encrypt_base64(unsigned char *src, unsigned char *dst, unsigned int dstLen)
{
    RC4_KEY         tempEncryptKey = encryptKey;
    unsigned char   secret_data[256];
    unsigned char   secret_data_recmb[256];
    BIO             *bio, *b64;
    FILE            *stream;
    int             encodedSize  = -1;
    int             srcLen = -1;
    int             i = -1, rst;

    if (!src || !dst ) {
        return -1;
    }

    srcLen = strlen((char*)src);
    encodedSize = 4*ceil((double)srcLen/3);
    if (srcLen > 256) {
        return -1;
    }

    memset(dst, 0, dstLen);
    memset(secret_data, 0, 256);

    // rc4
    RC4(&tempEncryptKey, srcLen, src, secret_data);

    // recored source passwd length
    secret_data_recmb[0] = (unsigned char)srcLen; 
    for (i=1; i<256; i++) {
        secret_data_recmb[i] = secret_data[i-1];
    }

    // base64
    stream = fmemopen(dst, encodedSize+1, "w");
    b64 = BIO_new(BIO_f_base64());
    bio = BIO_new_fp(stream, BIO_NOCLOSE);
    bio = BIO_push(b64, bio);
    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL); //Ignore newlines - write everything in one line
    BIO_write(bio, secret_data_recmb, strlen((char*)src) + 1);
    rst = BIO_flush(bio);
    if (rst <= 0) {
        printf("Call BIO_fulush failed, why?\n");
    }
    BIO_free_all(bio);
    fclose(stream);

    return 0;
}

/*
 * func:Calculates the length of a decoded base64 string
 */
static int 
calcDecodeLength(const char* b64input) 
{   
    int len = strlen(b64input);
    int padding = 0;
 
    if (b64input[len-1] == '=' && b64input[len-2] == '=') { //last two chars are =
        padding = 2;
    } else if (b64input[len-1] == '=') {//last char is =
        padding = 1;
    }

    return (int)len*0.75 - padding;
}

/*
 * argument:
 *      decryptKey:         decrypt key object
 *      baseSrc:            String after encrypt and base64
 *      dst:                primary value 
 */
int
waf_decrypt_base64(unsigned char *baseSrc, unsigned char *dst)
{
    RC4_KEY         tempDecryptKey = decryptKey;
    BIO             *bio, *b64;
    int             len = 0, decodeLen = 0;
    unsigned char   passwdLen = 0;
    unsigned char   buffer[256] = {0};
    FILE            *stream = NULL; 

    if (!baseSrc || !dst) {
        return -1;
    }

    // init
    decodeLen = calcDecodeLength((char*)baseSrc);
    stream = fmemopen(baseSrc, strlen((char*)baseSrc), "r");

    // base64
    b64 = BIO_new(BIO_f_base64());
    bio = BIO_new_fp(stream, BIO_NOCLOSE);
    bio = BIO_push(b64, bio);
    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL); //Do not use newlines to flush buffer
    len = BIO_read(bio, buffer, strlen((char*)baseSrc));
    if (len != decodeLen) {
        return -1;
    }
    buffer[len] = '\0';
    // free 
    BIO_free_all(bio);
    fclose(stream);

    // get the length of passwd
    passwdLen = buffer[0];
    if (passwdLen != decodeLen -1) {
        return -1;
    }
    // rc4 decrypt
    RC4(&tempDecryptKey, (int)passwdLen, (unsigned char*)&buffer[1], dst);

    return 0;
}

