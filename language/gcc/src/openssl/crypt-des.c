#include <openssl/des.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int
encrypt_des(DES_cblock *cblock, DES_key_schedule *ks1, DES_key_schedule *ks2, DES_key_schedule *ks3,
                char *cipher, char *string, int stringLen)
{
   DES_ede3_cbc_encrypt((const unsigned char*)string,
                         (unsigned char*)cipher,
                          stringLen, ks1, ks2, ks3,
                                  cblock, DES_ENCRYPT);
   printf("Encrypted : %32.32s\n",cipher);

   return 0;
}

int decrypt_des(char *cipher, char *text, DES_key_schedule *ks1, DES_key_schedule *ks2, 
                    DES_key_schedule *ks3, DES_cblock *cblock, int cipherLen)
{
   // You need to start with the same cblock value
   memset(cblock,0,sizeof(DES_cblock));
   DES_set_odd_parity(cblock);
   //-----------------------------------------------
   // I think you need to use 32 for the cipher len.
   // You can't use strlen(cipher) because if there
   // is a 0x00 in the middle of the cipher strlen
   // will stop there and the length would be short
   DES_ede3_cbc_encrypt((const unsigned char*)cipher,
                         (unsigned char*)text,
                          cipherLen, ks1, ks2, ks3,
                                     cblock,DES_DECRYPT);
   printf("Decrypted : %s\n",text);

   return 0;
}

int main() {
   DES_cblock cb1 = { 0xAE, 0xAE, 0xAE, 0xAE, 0xAE, 0xAE, 0xAE, 0xAE };
   DES_cblock cb2 = { 0xAE, 0xAE, 0xAE, 0xAE, 0xAE, 0xAE, 0xAE, 0xAE };
   DES_cblock cb3 = { 0xAE, 0xAE, 0xAE, 0xAE, 0xAE, 0xAE, 0xAE, 0xAE };

   DES_key_schedule ks1,ks2,ks3;

   DES_cblock cblock = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };

   char string[] = "I am a software developer, bbbxxxxxxxxxx, gjeogjeogjeojsb";
   int  ret = -1;
   // ---------------------------------------------
   // I use sizeof instead of strlen because I want
   // to count the '\0' at the end, strlen would
   // not count it
   int stringLen = strlen(string) + 1;
   int cipherLen = stringLen *2;

   printf("Plain Text : %s\n",string);
   char *cipher = (char*)malloc(cipherLen);
   char *text = (char*)malloc(stringLen);
   memset(cipher, 0, cipherLen);
   memset(text,0,stringLen);

   DES_set_odd_parity(&cblock);
   if (DES_set_key_checked(&cb1, &ks1) ||
        DES_set_key_checked(&cb2, &ks2) ||
         DES_set_key_checked(&cb3, &ks3)) {
      printf("Key error, exiting ....\n");
      return 1;
   }
   // ks1的值是根据解密是的数据变化的，所以该方法失败。
   ret = encrypt_des(&cblock, &ks1, &ks2, &ks3, cipher, string, stringLen);
   if (ret < 0) {
       return ret;
   }

   ret = decrypt_des(cipher, text, &ks1, &ks2, &ks3, &cblock, cipherLen);
   if (ret < 0) {
       return ret;
   }

   return 0;
}
