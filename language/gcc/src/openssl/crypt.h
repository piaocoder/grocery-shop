#ifndef _TOPWAF_CRYPT_H
#define _TOPWAF_CRYPT_H

/*
 * func:encrypt key initialize 
 */
void topwaf_crypt_base64_init();

/*
 * argument:
 *      decryptKey:         decrypt key object
 *      baseSrc:            String after encrypt and base64
 *      dst:                primary value 
 *      dstLen:             the length of primary string.
 */
extern int waf_decrypt_base64(unsigned char *baseSrc, unsigned char *dst);

/*
 * argument:
 *      src:                primary string
 *      dst:                value after encrypt and base64
 */
extern int waf_encrypt_base64(unsigned char *src, unsigned char *dst, unsigned int dstLen);


#endif

