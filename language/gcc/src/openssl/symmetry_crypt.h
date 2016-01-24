/*
 * Author: Du Xiaoyu mail:du_xiaoyu@topsec.com.cn
 */
#ifndef _SYMMETRY_CRYPT_H
#define _SYMMETRY_CRYPT_H 1

int waf_encrypt_base64_1(char *src, int srcLen, char *dst);

int waf_decrypt_base64_1(char *src, int srcLen, char *dst);

void waf_encrypt (char *mykey, char *src, int slen, char *dest);
void waf_decrypt (char *mykey, char *src, int slen, char *dest);

#endif /* _HTTP_RULELOADER_H */
