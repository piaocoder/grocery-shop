#include "base64.h"
#include "common.h"

#include <stdlib.h>
#include <string.h>
#include <openssl/pem.h>

bool kv_base64_encode(const void *data, int data_len, 
                        char *buffer, int *bufLen)
{
    int              slen;
    BIO             *b64 = BIO_new(BIO_f_base64());
    BIO             *bio = BIO_new(BIO_s_mem());
    BUF_MEM         *bptr = NULL;

    if (!data || !buffer) {
        return false;
    }

    bio = BIO_push(b64, bio);
    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL);
    BIO_write(bio, data, data_len);
    BIO_ctrl(bio, BIO_CTRL_FLUSH, 0, NULL);

    BIO_get_mem_ptr(bio, &bptr);
    slen = bptr->length;
    memcpy(buffer, bptr->data, slen);
    buffer[slen] = '\0';

    BIO_free_all(bio);

    *bufLen = slen;
    return true;
}

bool kv_base64_decode(const void *data, int data_len, 
                        char *buffer, int *bufLen)
{
    int              slen;
    BIO             *b64 = BIO_new(BIO_f_base64());
    BIO             *bio = BIO_new(BIO_s_mem());
    BUF_MEM         *bptr = NULL;

    if (!data || !buffer) {
        return false;
    }

    bio = BIO_push(b64, bio);
    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL);
    BIO_write(bio, data, data_len);
    BIO_ctrl(bio, BIO_CTRL_FLUSH, 0, NULL);

    BIO_get_mem_ptr(bio, &bptr);
    slen = bptr->length;
    memcpy(buffer, bptr->data, slen);
    buffer[slen] = '\0';

    BIO_free_all(bio);

    *bufLen = slen;
    return true;
}


