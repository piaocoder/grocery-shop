#ifndef _SRC_LIBSERVERS_BASE64_H_
#define _SRC_LIBSERVERS_BASE64_H_
#include "common.h"

bool kv_base64_encode(const void *data, int data_len, 
                        char *buffer, int *bufLen);

bool kv_base64_decode(const void *data, int data_len, 
                        char *buffer, int *bufLen);

#endif
