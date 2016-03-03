#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <openssl/rc4.h>
#include "crypt.h"
#include "symmetry.h"

int 
test(RC4_KEY  key, unsigned int buflen, unsigned char *buf, unsigned char *result) 
{
    RC4(&key, buflen, buf, result);
    return 0;
}

int my_crypt()
{
    RC4_KEY key1;
    RC4_KEY key2;
    unsigned char const key_data[8] = { 0x01, 0x23, 0x45, 0x67, 
        0x89, 0xab, 0xcd, 0xef };
    unsigned char *raw_data = (unsigned char *)"this is a rc4 test case";
    unsigned char outBuf[256] = {0};
    unsigned char outBuf1[256] = {0};
    int           i = 0;

    RC4_set_key(&key1, sizeof(key_data), key_data);
    RC4_set_key(&key2, sizeof(key_data), key_data);

    memset(outBuf, 0, sizeof(outBuf));
    test(key1, strlen((char*)raw_data), raw_data, outBuf);

    printf("第一次加密后的字符串: 长度为%lu\n", strlen((char*)outBuf));
    for (i=0; i<256; i++) {
        printf("%c", outBuf[i]);
    }
    test(key2, strlen((char*)raw_data), outBuf, outBuf1);
    printf("\n第一次解密后的字符串:%s\n", outBuf1);

    test(key2, strlen((char*)raw_data), outBuf, outBuf1);
    printf("\n第二次解密后的字符串:%s\n", outBuf1);

    return 0;
}

int crypt_second()
{
    RC4_KEY key1;
    RC4_KEY key2, tempKey2;
    unsigned char const key_data[8] = { 0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef };
    unsigned char *raw_data = (unsigned char *)"this is a rc4 test casexxxx";
    unsigned char outBuf[256] = {0};
    unsigned char outBuf1[256] = {0};
    int           i = 0;

    RC4_set_key(&key1, sizeof(key_data), key_data);
    RC4_set_key(&key2, sizeof(key_data), key_data);

    memset(outBuf, 0, sizeof(outBuf));
    RC4(&key1, strlen((char*)raw_data), raw_data, outBuf);

    printf("+++++++++++++++++++++++++++++\n");
    printf("第一次加密后的字符串: 长度为%lu\n", strlen((char*)outBuf));
    for (i=0; i<256; i++) {
        printf("%c", outBuf[i]);
    }

    tempKey2 = key2;
    RC4(&tempKey2, strlen((char*)raw_data), outBuf, outBuf1);
    printf("\n第一次解密后的字符串:%s\n", outBuf1);

    RC4(&key2, strlen((char*)raw_data), outBuf, outBuf1);
    printf("\n第二次解密后的字符串:%s\n", outBuf1);

    return 0;
}


int crypt_third()
{
    RC4_KEY key1, tempKey1;
    RC4_KEY key2, tempKey2;
    unsigned char const key_data[8] = { 0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef };
    unsigned char *raw_data = (unsigned char *)"this is a rc4 test casexxxx";
    unsigned char *raw_data2 = (unsigned char *)"this is a rc4 test caseshitege";
    unsigned char outBuf[256] = {0};
    unsigned char outBuf1[256] = {0};
    unsigned char outBufSecond[256] = {0};
    unsigned char outBufSecond1[256] = {0};
    int           i = 0;

    RC4_set_key(&key1, sizeof(key_data), key_data);
    RC4_set_key(&key2, sizeof(key_data), key_data);

    memset(outBuf, 0, sizeof(outBuf));
    tempKey1 = key1;
    RC4(&tempKey1, strlen((char*)raw_data), raw_data, outBuf);

    printf("+++++++++++++++++++++++++++++\n");
    printf("第一次加密后的字符串: 长度为%lu\n", strlen((char*)outBuf));
    for (i=0; i<256; i++) {
        printf("%c", outBuf[i]);
    }

    tempKey2 = key2;
    RC4(&tempKey2, strlen((char*)raw_data), outBuf, outBuf1);
    printf("\n第一次解密后的字符串:%s\n", outBuf1);

    tempKey1 = key1;
    tempKey2 = key2;
    memset(outBufSecond, 0, sizeof(outBufSecond1));
    memset(outBufSecond, 0, sizeof(outBufSecond));
    RC4(&tempKey1, strlen((char*)raw_data2), raw_data2, outBufSecond);
    RC4(&tempKey2, strlen((char*)raw_data2), outBufSecond, outBufSecond1);
    printf("\n第二次解密后的字符串:%s\n", outBufSecond1);

    tempKey2 = key2;
    memset(outBuf1, 0, sizeof(outBuf1));
    RC4(&tempKey2, strlen((char*)raw_data), outBuf, outBuf1);
    printf("\n第三次解密后的字符串(对应第一次加密):%s\n", outBuf1);

    return 0;
}

int main(int argc, char * argv[])
{
    unsigned char       password[256] = {0};
    unsigned char       src[128] = {0};
    char                *key = "gelgejlgjelgjelgjlejglegjlegjlegjlegjelj";
    char                *string = "This is a test string for encrypt or decrypt";
    char                dest[256] = {0};
    char                source[256] = {0};

    my_crypt();
    crypt_second();
    printf("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n");
    crypt_third();

    printf("==============================================================================\n");
    printf("==============================================================================\n");
    printf("==============================================================================\n");
    topwaf_crypt_base64_init();
    waf_encrypt_base64((unsigned char*)"hello, worlagelgejl", password, 256);
    printf("加密后的串%s\n", password);
    waf_decrypt_base64(password, src);
    printf("解密后的串%s\n", src);

    printf("******************************************************************************\n");
    printf("******************************************************************************\n");
    printf("******************************************************************************\n");
    /*
    int i = 0;
    while (!i) {
        sleep(1);
    }
    */
    string = "MYLOVE2014\0gegege";
    printf("初始字符串:%s\n", string);
    memset(source, 0, 256);
    waf_encrypt(key, string, strlen(string), source);
    printf("加密后的串为:%s\n", source);
    waf_decrypt(key, source, strlen(source), dest);
    printf("解密后的串为:%s\n", dest);

    printf("###############################################################################\n");
    printf("###############################################################################\n");
    printf("###############################################################################\n");
    string = "liu_huichao789";
    printf("初始字符串:%s\n", string);
    memset(source, 0, 256);
    memset(dest, 0, 256);
    waf_encrypt_base64_1(string, strlen(string), source);
    printf("加密后的串为:%s\n", source);
    
    /*
    int i = 0;
    while (!i) {
        sleep(1);
    }
    */
    waf_decrypt_base64_1(source, strlen(source), dest);
    printf("解密后的串为:%s\n", dest);

    return 0;
}
