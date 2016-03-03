#include <stdio.h>  
#include <stdlib.h>  
#include <string.h>  
#include <unistd.h>
#include <ev.h>  
#include <netinet/in.h>  
#include <sys/prctl.h>
#include <sys/socket.h>
#include <sys/un.h>
  
#define MAX_ALLOWED_CLIENT 10240  
#define UNIX_SOCKET_FILE   "/data/agentServer/nginx-redis.sock"
  
struct socket_data_package {                                        
    char                name[32];                     
    int                 data_len;           /* the length of data */
    char                data[];             /* data */              
    /* can't set any field here */                                  
};                                                                  

typedef struct socket_data_package  socket_data_package;

/*
 * func:connect server socket 
 */
static inline int
socket_handle(char *name, char *string)
{
    int                  clifd;
    int                  plen;
    struct sockaddr_un   servaddr;
    socklen_t            socklen;
    socket_data_package  *sendD;
    
    /* socket client */
    if ( (clifd = socket(AF_UNIX, SOCK_STREAM, 0 )) < 0 ) {
        return -1;
    }

    //bzero(&servaddr, sizeof(servaddr));
    servaddr.sun_family = AF_UNIX;
    strcpy(servaddr.sun_path, UNIX_SOCKET_FILE);

    socklen = sizeof(servaddr); 
    if (connect(clifd, (struct sockaddr *)&servaddr, socklen) < 0) {
        return -1;
    }

    /* send info by socket */
    plen = sizeof(socket_data_package) + strlen(string) + 1;
    //plen = sizeof(socket_data_package);
    sendD = (socket_data_package*)malloc(plen);
    memset(sendD, 0, plen);
    strcpy(sendD->data, string);
    sendD->data_len = strlen(string) + 1;
    strcpy(sendD->name, name);
    printf("name = %s   data_len=%d  data=%s\n", sendD->name, sendD->data_len, sendD->data);

    int ret;
    ret = write(clifd, (char*)sendD, plen);
    printf("ret = %d\n", ret);
    if (ret != plen) {
        printf("-------------\n");
        close(clifd);
        return -1;
    }

    /* close this connect */
    //sleep(5);
    close(clifd);  
    return 0;
}


int 
main(int argc, char **argv)
{
    /*char            name[32] = {0};*/
    /*char            data[1024] = {0};*/

    /*
    do {
        printf("Please input name:\t");
        scanf("%s", name);
        printf("Please input data:\t");
        scanf("%s", data);

        if (strlen(name) == 0) {
            break;
        }

        socket_handle(name, data);
    }while(1);
    */
    socket_handle("xxxxxxxxx", "bbbbbbbbb");

    return 0;
}
