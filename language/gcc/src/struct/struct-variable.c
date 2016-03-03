#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct socket_data_package {                                        
    unsigned int        type;
    unsigned int        data_len;           /* the length of data */
    char                data[];             /* data */              
    /* can't set any field here */                                  
};                                                                  
typedef struct socket_data_package  socket_data_package;

int
main(int argc, char **argv)
{
    socket_data_package         *sendpackage;
    char                        buffer[128];

    memset(buffer, 0, 128);

    sendpackage = (socket_data_package*)buffer;
    sendpackage->type = 0;
    sendpackage->data_len = 10;
    memcpy(sendpackage->data, "abcdelgelgegej", 10);

    printf("Sizeof(package)=%lu, Type=%d Len=%d data=%s\n", 
            sizeof(socket_data_package), sendpackage->type, 
            sendpackage->data_len, sendpackage->data);

    return 0;
}
