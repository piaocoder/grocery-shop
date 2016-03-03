#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <openssl/des.h>
#include <openssl/rand.h>
#include "hex.h"
 
/************************************************************************
 * 3DES-ECB加密方式
 * 8字节密钥，加密内容8位补齐，补齐方式为：PKCS7。
 *
 * file: test_des3_ecb.c
 * gcc -Wall -O2 -o test_des3_ecb test_des3_ecb.c hex.c -lcrypto
 *
 * author: tonglulin@gmail.com by www.qmailer.net
 ************************************************************************/
int main(int argc, char *argv[])
{
    int i = 0;
    int len = 0;
    int nlen = 0;
 
    char ch = '\0';
    char *key1 = "0000000000000000";  /* 原始密钥, 十六进制字符串 */
    char *key2 = "0000000000000000";  /* 原始密钥, 十六进制字符串 */
    char *key3 = "0000000000000000";  /* 原始密钥, 十六进制字符串 */
    char *data = "12345678123456781234567812345678";  /* 原始明文, 十六进制字符串 */
    unsigned char src[64] = {0};
    unsigned char out[64] = {0};
    unsigned char tmp[64] = {0};
 
    unsigned char *ptr  = NULL;
    unsigned char block[8] = {0};
    DES_key_schedule ks1, ks2, ks3;
 
    /* 设置密码表 */
    ptr = hex2bin(key1, strlen(key1), &nlen);
    memcpy(block, ptr, sizeof(block));
    free(ptr);
    DES_set_key_unchecked((C_Block *)block, &ks1);
 
    ptr = hex2bin(key2, strlen(key2), &nlen);
    memcpy(block, ptr, sizeof(block));
    free(ptr);
    DES_set_key_unchecked((C_Block *)block, &ks2);
 
    ptr = hex2bin(key3, strlen(key3), &nlen);
    memcpy(block, ptr, sizeof(block));
    free(ptr);
    DES_set_key_unchecked((C_Block *)block, &ks3);
 
    ptr = hex2bin(data, strlen(data), &nlen);
    memcpy(src, ptr, nlen);
    free(ptr);
 
    len = (nlen / 8 + (nlen % 8 ? 1: 0)) * 8;
 
    ch = 8 - nlen % 8;
    memset(src + nlen, ch, (8 - nlen % 8) % 8);
 
    printf("加密前数据: ");
    for (i = 0; i < len; i++) {
        printf("%02X", *(src + i));
    }
    printf("\n");
 
    for (i = 0; i < len; i += 8) {
        DES_ecb3_encrypt((C_Block *)(src + i), (C_Block *)(out + i), &ks1, &ks2, &ks3, DES_ENCRYPT);
    }
 
    printf("加密后数据: ");
    for (i = 0; i < len; i++) {
        printf("%02X" , *(out + i));
    }
    printf("\n");
 
    for (i = 0; i < len; i += 8) {
        DES_ecb3_encrypt((C_Block *)(out + i), (C_Block *)(tmp + i), &ks1, &ks2, &ks3, DES_DECRYPT);
    }
 
    printf("解密后数据: ");
    for (i = 0; i < len; i++) {
        printf("%02X", *(tmp + i));
    }
    printf("\n");
    printf("%s\n", tmp);
 
    return 0;
}
