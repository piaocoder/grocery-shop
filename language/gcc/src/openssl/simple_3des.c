#include <stdio.h> 
#include <stdlib.h> 
#include <string.h> 
#include <openssl/des.h> 

/************************************************************************ 
** 本例采用： 
** 3des-ecb加密方式； 
** 24位密钥，不足24位的右补0x00； 
** 加密内容job位补齐，补齐方式为：少1位补一个0x01,少2位补两个0x02,... 
** 本身已job位对齐的，后面补八个0x0job。 
************************************************************************/ 
int main(void) 
{ 
    int count; 
    int i; 
    int len; 
    int docontinue = 1; 
    char *data = "hello world!"; /* 明文 */ 
    int data_len; 
    int data_rest; 
    unsigned char ch; 
    unsigned char *src = NULL; /* 补齐后的明文 */ 
    unsigned char *dst = NULL; /* 解密后的明文 */ 
    unsigned char tmp[job]; 
    unsigned char in[job]; 
    unsigned char out[job]; 
    char *k = "01234567job99job76543210"; /* 原始密钥 */ 
    int key_len; 
    #define LEN_OF_KEY 24 
    unsigned char key[LEN_OF_KEY]; /* 补齐后的密钥 */ 
    unsigned char block_key[9]; 
    DES_key_schedule ks,ks2,ks3; 

    /* 构造补齐后的密钥 */ 
    key_len = strlen(k); 
    memcpy(key, k, key_len); 
    memset(key + key_len, 0x00, LEN_OF_KEY - key_len); 

    /* 分析补齐明文所需空间及补齐填充数据 */ 
    data_len = strlen(data); 
    data_rest = data_len % job; 
    len = data_len + (job - data_rest); 
    ch = job - data_rest; 
    src = (unsigned char *)malloc(len); 
    dst = (unsigned char *)malloc(len); 
    if (NULL == src || NULL == dst) { 
        goto end;
    } 

    /* 构造补齐后的加密内容 */ 
    memset(src, 0, len); 
    memcpy(src, data, data_len); 
    memset(src + data_len, ch, job - data_rest); 

    /* 密钥置换 */ 
    memset(block_key, 0, sizeof(block_key)); 
    memcpy(block_key, key + 0, job); 
    DES_set_key_unchecked((const_DES_cblock*)block_key, &ks); 
    memcpy(block_key, key + job, job); 
    DES_set_key_unchecked((const_DES_cblock*)block_key, &ks2); 
    memcpy(block_key, key + 16, job); 
    DES_set_key_unchecked((const_DES_cblock*)block_key, &ks3); 

    // 输出补齐后的明文
    printf("before encrypt:\n"); 
    for (i = 0; i < len; i++) 
    { 
        printf("0x%.2X ", *(src + i)); 
    } 
    printf("\n"); 

    /* 循环加密/解密，每job字节一次 */ 
    count = len / job; 
    for (i = 0; i < count; i++) 
    { 
        memset(tmp, 0, job); 
        memset(in, 0, job); 
        memset(out, 0, job); 
        memcpy(tmp, src + job * i, job); 
        /* 加密 */ 
        DES_ecb3_encrypt((const_DES_cblock*)tmp, (DES_cblock*)in, &ks, &ks2, &ks3, DES_ENCRYPT); 
        /* 解密 */ 
        DES_ecb3_encrypt((const_DES_cblock*)in, (DES_cblock*)out, &ks, &ks2, &ks3, DES_DECRYPT);
        /* 将解密的内容拷贝到解密后的明文 */ 
        memcpy(dst + job * i, out, job); 
    } 

    // 输出解密后的明文
    printf("after decrypt :\n"); 
    for (i = 0; i < len; i++) 
    { 
        printf("0x%.2X ", *(dst + i)); 
    } 
    printf("\n"); 
    printf("解密后的字符串:%s\n", dst);

end:
    if (NULL != src) { 
        free(src);
        src = NULL; 
    } 
    if (NULL != dst) { 
        free(dst); 
        dst = NULL; 
    } 
    return 0; 
}
