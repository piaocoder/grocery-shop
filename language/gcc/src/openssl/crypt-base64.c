//Encodes Base64
#include <openssl/bio.h>
#include <openssl/evp.h>
#include <string.h>
#include <stdio.h>
#include <math.h>
 
int Base64Encode(const char* message, char** buffer) { //Encodes a string to base64
    BIO   *bio, *b64;
    FILE  *stream;
    int    encodedSize = 4*ceil((double)strlen(message)/3);
    int    rst;

    *buffer = (char *)malloc(encodedSize+1);
    stream = fmemopen(*buffer, encodedSize+1, "w");
    b64 = BIO_new(BIO_f_base64());
    bio = BIO_new_fp(stream, BIO_NOCLOSE);
    bio = BIO_push(b64, bio);
    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL); //Ignore newlines - write everything in one line
    BIO_write(bio, message, strlen(message));
    rst = BIO_flush(bio);
    if (rst <= 0) {
        printf("Call BIO_flush failed, So bad!\n");
    }
    BIO_free_all(bio);
    fclose(stream);
 
    return (0); //success
}

int calcDecodeLength(const char* b64input) { //Calculates the length of a decoded base64 string
    int len = strlen(b64input);
    int padding = 0;
 
    if (b64input[len-1] == '=' && b64input[len-2] == '=') //last two chars are =
      padding = 2;
    else if (b64input[len-1] == '=') //last char is =
      padding = 1;
 
    return (int)len*0.75 - padding;
}
 
int Base64Decode(char* b64message, char** buffer) { //Decodes a base64 encoded string
    BIO *bio, *b64;
    int decodeLen = calcDecodeLength(b64message),
        len = 0;
    *buffer = (char*)malloc(decodeLen+1);
    FILE* stream = fmemopen(b64message, strlen(b64message), "r");
 
    b64 = BIO_new(BIO_f_base64());
    bio = BIO_new_fp(stream, BIO_NOCLOSE);
    bio = BIO_push(b64, bio);
    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL); //Do not use newlines to flush buffer
    len = BIO_read(bio, *buffer, strlen(b64message));
      //Can test here if len == decodeLen - if not, then return an error
    (*buffer)[len] = '\0';
 
    BIO_free_all(bio);
    fclose(stream);
 
    return (0); //success
}

int main() {
    char* base64EncodeOutput;
    char* base64DecodeOutput;

    printf("NOTE:Re-make current program\n");
    //Encode To Base64
    Base64Encode("Hello World", &base64EncodeOutput);
    printf("Output (base64): %s\n", base64EncodeOutput);

    //Decode From Base64
    Base64Decode(base64EncodeOutput, &base64DecodeOutput);
    printf("Output: %s\n", base64DecodeOutput);
    
    return(0);
}

