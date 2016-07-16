#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <sys/select.h>//use select() for multiplexing
#include <sys/fcntl.h> // for non-blocking

#if !defined(__bool_true_false_are_defined) && !defined(__cplusplus)
typedef int bool;                                                   
#define true 1                                                      
#define false 0                                                     
#define __bool_true_false_are_defined                               
#endif                                                              

#define UDP_SERVER_PORT     5000
#define MAX_LENGTH          1024

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

bool socket_init(int *sockfd, struct sockaddr_in *saddr)
{
    int         cfd;
    int         flags;
    int         rst;

    if ((cfd = socket(AF_INET, SOCK_DGRAM, 0)) == -1) {
        _error("socket()");
        return false;
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

    printf("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n");
    plen = recvfrom(sockfd, receive_data, MAX_LENGTH, 0, 
            (struct sockaddr *)caddr, (socklen_t*)caddrLen);
    if (plen <= 0) {
        printf("pLen is less or equal to zero.\n");
        return false;
    }

    receive_data[plen] = '\0';
    if((strcmp(receive_data, "q") == 0) || 
            (strcmp(receive_data , "Q") == 0)) {
        printf("\nClient has exited the chat.\n");
        return false;
    }

    printf("\n(%s , %d) said: %s\n",inet_ntoa(caddr->sin_addr), 
            ntohs(caddr->sin_port), receive_data);

    return true;
}

/*
 * 从stdin读取信息，会阻塞
 */
bool write_msg(int sockfd, char *sbuf, 
        struct sockaddr_in *caddr, unsigned int *caddrLen)
{
    printf("SERVER: ");

    //input the name with a size limit of MAX_LENGTH
    fgets(sbuf, MAX_LENGTH, stdin); 
    if ((strlen(sbuf)>0) && (sbuf[strlen (sbuf) - 1] == '\n')) {
        sbuf[strlen(sbuf) - 1] = '\0';
    }
    if ((strcmp(sbuf , "q") == 0) || (strcmp(sbuf , "Q") == 0)) {
        sendto(sockfd, sbuf, strlen(sbuf), 0,
                    (struct sockaddr *)&caddr, sizeof(struct sockaddr));
        return false;
    }

    sendto(sockfd, sbuf, strlen(sbuf), 0,
            (struct sockaddr *)&caddr, sizeof(struct sockaddr));

    return true;
}

int main()
{
    fd_set          original_socket, original_stdin;
    fd_set          readfds, writefds;
    struct          timeval tv;
    int             numfd, receive;
    int             sockfd = 0;
    unsigned int    addrLen;
    char            receive_data[MAX_LENGTH];
    struct sockaddr_in caddr, saddr;
    bool            rst;

    // clear the set ahead of time
    // 清空
    FD_ZERO(&original_socket);
    FD_ZERO(&original_stdin);
    FD_ZERO(&readfds);
    FD_ZERO(&writefds);

    rst = socket_init(&sockfd, &saddr);
    if (rst != true) {
        return -1;
    }

    // add our descriptors to the set (0 - stands for STDIN)
    // 将sockfd存入到备份描述符集合／读描述符集合中
    FD_SET(sockfd, &original_socket);//instead of 0 put sockfd
    FD_SET(sockfd, &readfds);
    FD_SET(0,&original_stdin);
    FD_SET(0, &writefds);

    // 设置描述符最大值
    numfd = sockfd + 1;
    addrLen = sizeof(struct sockaddr);
    printf("\nUDP_Server Waiting for client to respond...\n");
    printf("Type (q or Q) at anytime to quit\n");
    fflush(stdout);

    while (1) {
        tv.tv_sec = 1;
        tv.tv_usec = 500000;
        // 从备份中读取描述符信息
        readfds = original_socket;
        writefds = original_stdin;

        receive = select(numfd, &readfds, &writefds,/*NULL,*/ NULL, &tv);
        if (receive == -1) {
            _error("select"); // error occurred in select()
        }  else if (receive == 0)  {
            printf("Timeout occurred!  No data after 10.5 seconds.\n");
        } else {
            // one or both of the descriptors have data
            if (FD_ISSET(sockfd, &readfds)) { 
                FD_CLR(sockfd, &readfds);
                read_msg(sockfd, receive_data, &caddr, &addrLen);
            } else {
                printf("\nOOPS! What happened? SERVER");
            }
        } //end else
    }//end while

    close(sockfd);
    return 0;
}
