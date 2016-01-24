#include <stdio.h>  
#include <stdlib.h>  
#include <stddef.h>
#include <string.h>  
#include <unistd.h>
#include <netinet/in.h>  
#include <ev.h>  
#include <sys/types.h>
#include <sys/prctl.h>
#include <sys/un.h>
  
#define MAX_ALLOWED_CLIENT 10240  
#define UNIX_SOCKET_FILE   "/tmp/a.socket"
  
struct socket_data_package {                                        
    char                name[32];                     
    int                 data_len;           /* the length of data */
    char                data[];             /* data */              
    /* can't set any field here */                                  
};                                                                  
typedef struct socket_data_package  socket_data_package;


static void accept_cb(struct ev_loop *loop, struct ev_io *watcher, int revents);  
static void timer_cb(struct ev_loop *loop, ev_timer *w, int revents);

static ev_timer         mytimer;
  
int main()  
{  
    struct ev_loop *loop=ev_default_loop(0);  
    int sd;  
    struct sockaddr_un  addr;
    socklen_t           addrlen;
      
    //创建一个io watcher和一个timer watcher  
    struct ev_io socket_accept;  
    //创建socket连接  
    if ((sd = socket(AF_UNIX, SOCK_STREAM, 0)) < 0) { 
        printf("socket error\n");  
        return -1;  
    }  

    bzero(&addr, sizeof(struct sockaddr_un));
    addr.sun_family = AF_UNIX;  
    strcpy(addr.sun_path, UNIX_SOCKET_FILE);
    addrlen = offsetof(struct sockaddr_un, sun_path) + strlen(addr.sun_path);
    // 地址复用
    unlink(UNIX_SOCKET_FILE);

    if(bind(sd, (struct sockaddr*)&addr, addrlen) != 0)  
    {  
        printf("bind error\n");  
        return -1;  
    }  

    if(listen(sd, SOMAXCONN) < 0)  
    {  
        printf("listen error\n");  
        return -1;  
    }  
    chmod(UNIX_SOCKET_FILE,00777);//设置通信文件权限
     
    //初始化io watcher，用于监听fd  
    ev_io_init(&socket_accept, accept_cb, sd, EV_READ);  
    ev_io_start(loop, &socket_accept);  

    ev_timer_init(&mytimer, timer_cb, 0., 5.);
    ev_timer_start(loop, &mytimer);

    ev_run(loop, 0);  
      
    close(sd);  
    ev_io_stop(loop, &socket_accept);  
    return 0;  
}  
  
static void
timer_cb(struct ev_loop *loop, ev_timer *w, int revents)
{
    printf("%s===================================\n", __func__);
}

static void 
accept_cb(struct ev_loop *loop, struct ev_io *watcher, int revents)  
{  
    // 收到连接，处理客户端fd
    struct sockaddr_un   client_addr;
    socklen_t            client_len = sizeof(client_addr);  
    socket_data_package  recvbuf;
    char                 buffer[1024] = {0};
    int                  client_sd, buflen;  

    ev_timer_stop(loop, &mytimer);
    ev_timer_set(&mytimer, 0., 15.0);
    ev_timer_start(loop, &mytimer);

    buflen = sizeof(socket_data_package);
    if(EV_ERROR & revents)  
    {  
        printf("error event in accept\n");  
        return ;  
    }  
      
    //获取与客户端相连的fd  
    client_sd = accept(watcher->fd, (struct sockaddr*)&client_addr, &client_len);  
    if(client_sd < 0)  
    {  
        printf("accept error\n");  
        return;  
    }  

    //如果连接数超出指定范围，则关闭连接  
    if (client_sd > MAX_ALLOWED_CLIENT) {  
        printf("fd too large[%d]\n", client_sd);  
        close(client_sd);  
        return ;  
    }  
      
    int ret; 
    ret = read(client_sd, (char*)&recvbuf, buflen);
    if (ret < 0) {
        printf("read socket failure!\n");
        return;
    }

    buflen = recvbuf.data_len;
    if (buflen < 0) {
        printf("package data is null.\n");
        return; 
    }

    if (read(client_sd, buffer, buflen) < 0) {
        printf("read socket failure!\n");
        return;
    }
   
    printf("name=%s data=%s\n", recvbuf.name, buffer);
    return;
}  
