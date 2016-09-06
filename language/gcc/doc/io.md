---
IO Knowledge
---


### 1 Introduction
#### 1.1 fcntl
fcntl——file control，用于执行各种描述符控制相关的操作

#### 1.2 ioctl
ioctl——作为哪些不适合加入其他“精细定义类别”的特性的系统接口

#### 1.3 Std IO and File IO
文件IO——IO例程
标准IO——IO流处理

#### 1.4 IO Model
- Blocked IO
- Nonblock IO
- IO Multicomplexing
- Signal-driven IO
- Asynchronous IO


### 2 fcntl
#### 2.1 fcntl/ioctl/route-socket
> 下表是对于某一个固定操作，fcntl/ioctl/路由socket的不同执行动作        
  注意，除了以下功能，还存在她们各自的独特功能，例如fcntl的文件锁

操作小结如下：流
>
    -----------------------------------------------------------------------------
    Operate       |       fcntl       |      ioctl     |  路由socket |  POSIX
    -----------------------------------------------------------------------------
    Set非阻塞IO    F_SETFL,O_NONBLOCK      FIONBIO                      fcntl
    -----------------------------------------------------------------------------
    Set信号式IO    F_SETFL,O_ASYNC        FIOASYNC                      fcntl
    -----------------------------------------------------------------------------

    -----------------------------------------------------------------------------
    设置属主       F_SETOWN            SIOCSPGRP/FIOSETOWN              fcntl
    -----------------------------------------------------------------------------
    获取属主       F_GETOWN            SIOCGPGRP/FIOGETOWN              fcntl
    -----------------------------------------------------------------------------

    -----------------------------------------------------------------------------
    获取接收缓冲区字节                 FIONREAD
    -----------------------------------------------------------------------------
    测试是否处于带外标志               SIOCATMARK                      sockatmark
    -----------------------------------------------------------------------------

    -----------------------------------------------------------------------------
    获取接口列表                       SIOCGIFCONF         synctl
    -----------------------------------------------------------------------------
    接口操作                           SIOC[GS]IFxxx
    -----------------------------------------------------------------------------

    -----------------------------------------------------------------------------
    ARP高速缓存                        SIOCxARP            RTM_xxx
    -----------------------------------------------------------------------------
    路由表操作                         SIOCxxxRT           RTM_xxx
    -----------------------------------------------------------------------------

注意，其中POSIX表示POSIX标准对应该某一个操作的建议方法；
关于ioctl的接口操作/ARP/路由等操作，见UNP1-366页的说明

#### 2.2 函数定义
```gcc
    #include <fcntl.h>
    int fnctl(int fd, int cmd, ...);
```

#### 2.3 复制文件描述符
> 第三个参数为整数

```gcc
    #include <fcntl.h>
    // 获取最新的最小的fd1，和fd共享同一个文件表项
    int fcntl(int fd, int cmd, 0);
    // 等价于
    dup(fd);

    // 将fd1指向fd，即，fd和fd1共享同一个文件表项
    close(fd1);
    int fcntl(int fd, int cmd, int fd1);
    // 等价于dup2，不过后者为原子操作，且错误信息也不同
    dup2(fd, fd1);
```

#### 2.4 描述符标志
> 第三个参数为整数
> 
    close_on_exec标志在进程exec时相关，如果某一个fd的该标志位
    被设置，则执行exec之后，新的进程会自动关闭该fd，不会进行
    拷贝操作。详情见APUE-190页说明。

文件描述符标志——FD\_CLOEXEC，见APUE-190页说明，另见文件共享中的
进程表项-文件表-v节点表
```gcc
    #include <fcntl.h>

    // 获取文件描述符标志并判断
    int val;

    val = fcntl(fd, F_GETFD, 0);
    if (val < 0) {
        err_sys("Get fd flags failed.");
    }
    if (val & FD_CLOEXEC) {
        OK;
    } else {
        // 设置文件描述符标志
        val |= FD_CLOEXEC;
        ret = fcntl(fd, F_SETFD, val);
        if (ret < 0) {
            err_sys("Set fd flags failed.");
        }
    }
```

#### 2.5 设置文件状态
> 第三个参数为整数

相关的文件状态标志见APUE-63页，这里介绍两个和ioctl相关的状态标志：
>
    O_NONBLOCK，非阻塞模式，关联的ioctl标志为FIONBIO，见UNP-182
    O_ASYNC，信号驱动IO，关联的ioctl标志为FIOASYNC，见UNP-525

    其中fcntl为最新的用法，在某些系统中可能不支持，固使用ioctl，
    不过POSIX建议使用fcntl，如果系统支持。

##### 2.5.1 非阻塞
代码示例：
```gcc
    #include <fcntl.h>

    // Open非阻塞式IO
    int flags;
    if ((flags=fcntl(fd, F_GETFL, 0)) < 0) {
        err_sys("Get file flags failed.");
    }
    flags |= O_NONBLCOK;
    if (fcntl(fd, F_SETFL, flags) < 0) {
        err_sys("Set file flags failed.");
    }

    // Close非阻塞式IO
    flags &= ~O_NONBLOCK;
    if (fcntl(fd, F_SETFL, flags) < 0) {
        err_sys("Set file flags failed.");
    }
```
##### 2.5.2 信号驱动
> 第三个参数为整数
> 一般用于UDP，对TCP基本无用
```gcc
    // 见UNP-529例子
    // 步骤1,设置信号处理函数
    Signal(SIGIO, sig_io);
    // 步骤2,设置套机字或者fd的属主
    Fcntl(sockfd, F_SETOWN, getpid());
    // 步骤3,开启信号驱动IO
    Ioctl(sockfd, FIOASYNC, &on);
    // 额外步骤：非阻塞
    Ioctl(sockfd, FIONBIO, &on);
```

#### 2.6 设置套接字属主
> 第三个参数为整数
> 在信号驱动中使用

设置接收SIGIO信号的进程ID/进程组ID，其中如果args为负数，则表示
进程组ID，vice versa.
```gcc
    pid = fcntl(sockfd, F_GETOWN, 0);
    if (pid == -1) {
        err_sys("Get pid failed.");
    } else if (pid > 0) {
        // 获取Pid
    } else {
        // 获取gid
    }

    // 设置属主
    flags = fcntl(sockfd, F_SETOWN, getpid());
    if (flags == -1) {
        err_sys("Set own.");
    }
```

#### 2.7 记录锁
> 第三个参数为指向flock的指针，注意和上面的不同之处
