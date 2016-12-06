---
title: socket
date:  2016-09-18 19:00:00  
tags: c  
---


### 1 Introduction
- 大小端
- socket地址结构
- 基本socket操作
- socket选项
- socket高级用法
- socket错误


### 2 大小端
参考APUE-440,UNP-63页
- 主机字节序和网络字节序； 
- 大小端  

#### 2.1 定义
大小端表示字节的哪一端(小/大)存储在内存的起始位置
- 小端——低端（低字节）存储在内存的起始位置
- 大端——高端（高字节）存储在内存的起始位置

#### 2.2 例子
通过union联合来输出本机的大小端信息（见UNP-64页）


### 3 socket地址结构
#### 3.1 命名规范
不包含通用地址结构struct sockaddr {}

##### 3.1.1 地址结构
> 参考unp-61页  

```
    sockaddr_XX，例如sockaddr_in，sockaddr_un
    struct sockaddr_in {
        ...
    };
```
##### 3.1.2 结构体成员
> 参考unp-61页  

```
    sXX_名称，其中XX标识上一节地址结构中的末尾值，例如
        对于IPV4，其地址结构为-sockaddr_in，则其成员命名：sin_名称
    其他由：sin6_名称，sun_名称，sdl_名称，sa_名称

    struct sockaddr_in {
        uint8_t         sin_len;
        sa_family_t     sin_family;
        in_port_t       sin_port;

        struct in_addr  sin_addr;
        char            sin_zero[8];
    };
```
##### 3.1.3 ipv4地址/ipv6地址
```gcc
    格式：XX_addr
    例如：in_addr，in6_addr，这两者都是结构体

    结构体中的地址一般为整型，此时可能需要进行字节序的转换
```

#### 3.2 通用地址结构
因为历史原因，（1982年还没有ASCII C，没有void \*指针）
采用struct sockaddr通用结构来支持所有的协议族的套接字地址结构。
#### 3.2.1 定义
```gcc
    // 注意这里的结构体成员也是按照3.1中的命名规范
    struct sockaddr {
        uint8_t     sa_len;
        sa_family_t sa_family;
        char        sa_data[14];
    };
```
#### 3.2.2 例子
```
    // 通过指针的强制转换来实现
    int bind(int, struct sockaddr *, socklen_t);
```


### 4 基本socket
> 关于TCP分节，见UNP-32页  

#### 4.1 定义
##### 4.1.1 创建sockfd
```gcc
    #include <sys/socket.h>
    // 适用于所有的套接字类型
    int socket(int family, int type, int protocol);
    // UNIX域：多进程中的描述符传递以及通信，UNP-327
    int socketpair(int , int , int protocol, int sockfd[2]);
```
##### 4.1.2 连接server
> 见unp-80页/apue-450页  

###### 4.1.2.1 出错返回情况
```
    ETIMEDOUT——客户没有收到SYN分节相应（75S重发）
    ECONNREFUSED——RST，refused拒绝，hard error, 产生RST的条件有
        > 消息到达，但端口上无server；
        > TCP服务器本身取消该连接；
        > Tcp服务器接收到一个根本不存在的连接的SYN分节
    EHOSTUNREACH/ENETUNREACH——网络不可达，soft error
```
###### 4.1.2.2 定义
```gcc
    #include <sys/socket.h>
    int connect(int sockfd, struct sockaddr*, socklen_t);
```

##### 4.1.3 绑定
将本地协议地址赋予一个套接字，不是用内核自动派发，从而达到一个
口头上的对外约定，一般在server端进行此类操作。

###### 4.1.3.1 定义
关于IP-port的匹配结果，见UNP-82页说明
函数定义如下：
```gcc
    #include <sys/socket.h>
    int bind(int sockfd, struct sockaddr *, socklen_t);
```
###### 4.1.3.2 获取端口信息
对于绑定的socket，无需获取ip-port信息，使用场景：
- 未使用bind的client，内核默认分配socket
- bind时端口号为0，表示内核自动填充  

使用方法：getsockname来获取Ip-port信息
```gcc
    #include <sys/socket.h>
    // 获取socket的地址族
    int getsockname(int, struct sockaddr*, socklen_t);
    // 在exec进程中，使用getpeername来获取客户端的ip-port信息
    int getpeername(int, struct sockaddr*, socklen_t);
```

##### 4.1.4 监听
> 仅仅适用于TCP Server，具体见UNP-85  

###### 4.1.4.1 队列
- Incomplete connection queue：Client发出的SYN分片，等待Server完成三次握手
- Complete connection queue:完成三次握手的client连接，即accept返回

backlog的长度在老式的代码中一般为5，但是当前繁忙的server中，该值早已发生
改变，目前的backlog可以手动配置；

当ICQ队列满时，一个新的SYN到达时，Server不会做任何处理，忽略，从而让Client
进行重发操作，保证下一次有空闲在处理。

###### 4.1.4.2 定义
```gcc
    #include <sys/socket.h>
    int listen(int sockfd, int backlog);
    int accept(int sockfd, struct sockaddr*, socklen_t*);
```
##### 4.1.5 关闭
```
    #include <unistd.h>
    int close(int sockfd);
```

#### 4.2 例子
见tcpcliserv/tcpserv01.c以及相关文件
