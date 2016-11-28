#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/select.h>//use select() for multiplexing
#include <sys/fcntl.h> // for non-blocking

#include "thpool.h"


#if !defined(__bool_true_false_are_defined) && !defined(__cplusplus)
typedef int bool;                                                   
#define true 1                                                      
#define false 0                                                     
#define __bool_true_false_are_defined                               
#endif                                                              

#define UDP_SERVER_PORT     5000
#define MAX_LENGTH          1024

typedef struct sockaddr_in sockaddr_in_t;
typedef struct thd_handle thd_handle_t;
struct thd_handle {
    int             fd;
    char            buf[MAX_LENGTH];
    sockaddr_in_t   addr;
    unsigned int    addrLen;
};



/* Select() params
 * int select(int n, fd_set *readfds, fd_set *writefds, fd_set *exceptfds, struct timeval *timeout);
 * FD_SET(int fd, fd_set *set);
 * FD_CLR(int fd, fd_set *set);
 * FD_ISSET(int fd, fd_set *set);
 * FD_ZERO(fd_set *set);
*/
void _error(char *message)
{
    perror(message);
    exit(1);
}


bool socket_thpool_init(threadpool *thpool, size_t num)
{
    *thpool = thpool_init(num); 
    if (NULL == *thpool) {
        _error("thpool_init 失败\n");
    }
    return true;
}


bool socket_init(int *sockfd, struct sockaddr_in *saddr)
{
    int         cfd;
    int         flags;
    int         rst;

    if ((cfd = socket(AF_INET, SOCK_DGRAM, 0)) == -1) {
        _error("socket()");
    }

    //set socket to non-blocking
    flags = fcntl(cfd, F_GETFL);
    flags |= O_NONBLOCK;
    fcntl(cfd, F_SETFL, flags);
    //fcntl(cfd, F_SETFL, O_NONBLOCK); 
    
    // since we got s2 second, it's the "greater", 
    // so we use that for the n param in select()
    saddr->sin_family = AF_INET;
    saddr->sin_port = htons(UDP_SERVER_PORT);
    saddr->sin_addr.s_addr = INADDR_ANY;
    bzero(&(saddr->sin_zero),8);

    rst = bind(cfd,(struct sockaddr *)saddr, sizeof(struct sockaddr));
    if (rst == -1) {
        _error("bind()");
    }

    *sockfd = cfd;

    return true;
}


bool read_msg(int sockfd, char *receive_data, 
        struct sockaddr_in *caddr, unsigned int *caddrLen)
{
    int                 plen;

    plen = recvfrom(sockfd, receive_data, MAX_LENGTH, 0, 
            (struct sockaddr *)caddr, (socklen_t*)caddrLen);
    if (plen <= 0) {
        _error("package length is less then zero.");
    }

    receive_data[plen] = '\0';
    if((strcmp(receive_data, "q") == 0) || 
            (strcmp(receive_data , "Q") == 0)) {
        _error("\nClient has exited the chat.\n");
    }

    printf("\n(%s , %d) said: %s\n",inet_ntoa(caddr->sin_addr), 
            ntohs(caddr->sin_port), receive_data);

    return true;
}


bool write_msg(int sockfd, char *sbuf, 
        struct sockaddr_in *caddr, unsigned int *caddrLen)
{
    //input the name with a size limit of MAX_LENGTH
    if ((strlen(sbuf)>0) && (sbuf[strlen (sbuf) - 1] == '\n')) {
        sbuf[strlen(sbuf) - 1] = '\0';
    }
    if ((strcmp(sbuf , "q") == 0) || (strcmp(sbuf , "Q") == 0)) {
        sendto(sockfd, sbuf, strlen(sbuf), 0,
                    (struct sockaddr *)&caddr, *caddrLen);
        return false;
    }

    sendto(sockfd, sbuf, strlen(sbuf), 0,
            (struct sockaddr *)caddr, *caddrLen);

    return true;
}


void* udp_handle(void *ptr)
{
    thd_handle_t        *thandle = NULL;
    bool                 rst;

    thandle = (thd_handle_t*)ptr;
    rst = write_msg(thandle->fd, thandle->buf, 
            &thandle->addr, &thandle->addrLen);
    if (!rst) {
        return NULL;
    }
    return (void*)0;
}


int main()
{
    fd_set          original_socket;
    fd_set          readfds;
    struct          timeval tv;
    int             numfd, receive;
    int             sockfd = 0;
    unsigned int    addrLen, caddrLen;
    char            receive_data[MAX_LENGTH];
    threadpool      thpool;
    struct sockaddr_in caddr, saddr;
    thd_handle_t   *thandle = NULL;
    bool            rst;

    // clear the set ahead of time
    // 清空
    FD_ZERO(&original_socket);
    FD_ZERO(&readfds);

    // socket init
    socket_init(&sockfd, &saddr);

    // add our descriptors to the set (0 - stands for STDIN)
    // 将sockfd存入到备份描述符集合／读描述符集合中
    FD_SET(sockfd, &original_socket);//instead of 0 put sockfd
    FD_SET(sockfd, &readfds);

    // 设置描述符最大值
    numfd = sockfd + 1;
    addrLen = sizeof(struct sockaddr);
    printf("\nUDP_Server Waiting for client to respond...\n");
    printf("Type (q or Q) at anytime to quit\n");
    fflush(stdout);

    // thpool init
    socket_thpool_init(&thpool, 10);

    while (1) {
        tv.tv_sec = 1;
        tv.tv_usec = 500000;
        // 从备份中读取描述符信息
        readfds = original_socket;

        receive = select(numfd, &readfds, NULL, NULL, &tv);
        if (receive == -1) {
            _error("select"); // error occurred in select()
        }  else if (receive == 0)  {
            printf("Timeout occurred!  No data after 10.5 seconds.\n");
        } else {
            // one or both of the descriptors have data
            if (FD_ISSET(sockfd, &readfds)) { 
                //if set to read
                FD_CLR(sockfd, &readfds);
                rst = read_msg(sockfd, receive_data, 
                        (sockaddr_in_t*)&caddr, &caddrLen);
                if (!rst) {
                    _error("Read msg failed!");
                }
                // create thread
                thandle = (thd_handle_t*)malloc(sizeof(thd_handle_t));
                if (NULL == thandle) {
                    _error("Malloc memory failed!");
                }
                thandle->fd = sockfd;
                strncpy(thandle->buf, receive_data, MAX_LENGTH);
                thandle->addr = caddr;
                thandle->addrLen = addrLen;
                thpool_add_work(thpool, (void*)udp_handle, thandle);
            } else {
                printf("\nOOPS! What happened? SERVER");
            }
        } //end else
    }//end while

    thpool_destroy(thpool);
    close(sockfd);

    return 0;
}
