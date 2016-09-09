---
IO Knowledge
---


### 1 Introduction
#### 1.1 fcntl
fcntl——file control，用于执行各种描述符控制相关的操作

#### 1.2 ioctl
ioctl——作为哪些不适合加入其他“精细定义类别”的特性的系统接口

#### 1.3 Std IO and File IO
- 文件IO——IO例程
- 标准IO——IO流处理

#### 1.4 Format IO
- scanf族  
- printf族

#### 1.5 IO Model
- Blocking IO
- Nonblock IO
- IO Multicomplexing
- Signal-driven IO
- Asynchronous IO


### 2 fcntl
#### 2.1 fcntl/ioctl/route-socket
> 下表是对于某一个固定操作，fcntl/ioctl/路由socket的
不同执行动作。
注意，除了以下功能，还存在她们各自的独特功能，例如fcntl的文件锁

操作小结如下：见UNP-182页

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
> 参考APUE-358
##### 2.7.1 定义
```gcc
    /*
     * 其中cmd可以为
     *      F_GETLK     判断第三个参数中描述的锁是否被阻塞
     *      F_SETLK     设置flockptr指针所描述的锁，失败返回Eacces
     *      F_SETLKW    F_SETLK的阻塞版本
     *
     * 第三个参数为flock指针，具体见APUE-359页
     */
    int fcntl(int filedes, int cmd, ...);
```

##### 2.7.2 规则
- 读写锁的兼容性见APUE-359页说明
- 同一个进程对一个文件区间进行多次加锁时，不会有任何额外信息，新锁替换旧锁
- 使用F\_GETLK可以测试一个文件的记录锁PID信息，除了本人的PID之外
- 加读锁-读打开，加写锁-写打开
- 因为GETLK和SETLK不是原子操作，一般不用会使用GETLK，直接使用SETLK，再判断返回值

##### 2.7.2 例子
测试锁
```gcc
    #include <fcntl.h>
    #include "apue.h"

    pid_t lock_test(int fd, int type, off_t offset, int whence, off_t len)
    {
        // 根据参数填充flock结构
        struct flock lock;
        // 锁的类型
        lock.l_type = type;
        // Relative to l_whence
        lock.l_start = offset;
        // 见lseek函数
        lock.l_whence = whence;
        // 范围
        lock.l_len = len;

        // 使用F_GETLK测试是否阻塞
        if (fcntl(fd, F_GETLK, &lock) < 0) {
            err_sys("Occur error.");
        }

        // 根据lock.l_type判断是否存在锁
        if (lock.l_type == F_UNLK) {
            return 0;
        } else {
            return lock.l_pid;
        }
    }
```


### 3 ioctl
> 无法精细归类的接口，但是POSIX一直在努力中

特别功能：获取接口信息，访问路由表，访问ARP高速缓存等
重复功能：文件操作(fcntl)，套接字操作，流系统

#### 3.1 函数定义
```gcc
    #include <unistd.h>
    // 第三个参数为指针，依赖于request的值
    int ioctl(int fd, int request, ...);
```
关于request和args的关系以及总结，见UNP-366

#### 3.2 获取接口配置
```gcc
    struct ifconf ifc;

    // 初始容量，内核会自动填充<=该长度的接口信息并更新ifc_len
    len = 100*sizeof(struct ifreq);
    buf = (char*)malloc(len);
    ifc.ifc_len = len;
    ifc.ifc_buf = buf;

    if (ioctl(sockfd, SIOCGIFCONF, &ifc) < 0) {
        if (errno != EINVAL) {
            err_sys("ioctl error.");
        }
    } else {
        // 判断是否获取到所有的接口信息
        if (ifc.ifc_len == lastlen) {
            // 见UNP-373
            break;
        }
        lastlen = ifc.ifc_len;
    }
    ...
```

### 4 IO and Std IO
> 在设计ANSI函数库时，可移值性和完整性是考虑的关键（并没有性能哦），见Pointers on C-298页
#### 4.1 Diagram
##### 4.1.1 架构
> StdIO一般仅仅用于普通文件的操作，对于接近底层的文件操作，例如socket/driver等等，都是使用IO例程来操作的。
> 当然，普通文件操作占据所有文件操作的大部分(二八原则)

![IO关系图](http://obbuzq2fl.bkt.clouddn.com/image/IO/io-diagram.pngio-diagram.png)

##### 4.1.2 说明
IO例程和标准IO的区别如下：
- 一个在用户态操作，一个在内核态操作，但是如果对内核态的操作不合理，可能造成更大的开销;
- 标准IO不涉及目录的相关操作，具体见filestat.md文件
- 标准IO相比IO例程，可移值性更高，但是性能不一定

流类型：
- 文本流
- 二进制流

#### 4.2 打开文件
```gcc
    // 返回fd或者-1，具体见apue-48
    int open(pathname, flag, mode);

    // 返回fp或者NULL
    FILE* fopen(pathname, const char *restrict type);

    // fp和fd的转化
    FILE* fdopen(int fd, const char *type);
    int fileno(FILE *fp);
```

#### 4.3 关闭
```gcc
    // 关闭某一个文件描述符，避免打开过多的fd，返回0或者-1
    int close(int fd);

    // 关闭某一个fp，返回0或者EOF
    int fclose(fp);
```

#### 4.4 写
```gcc
    #include <unistd.h>
    // 成功返回写入的字节数，失败返回-1
    // 其中nbytes <= strlen(buf)，避免越界读
    ssize_t write(int fd, buf, size_t nbytes);

    #include <stdio.h>
    // 字符，成功返回c，失败返回EOF
    int putc(int c, FILE *fp);
    int fputc(intc, FILE *fp);
    int putchar(int c);
    // 字符串，成功返回非负值，失败返回EOF
    int fputs(char str, FILE *fp);
    int puts(str);


    // 二进制，返回写入的对象数，否则为-1, 参考write函数
    // nobj为对象数目，size为每一个对象的大小
    ssize_t fwrite(void *ptr, size_t size, size_t nobj, FILE *fp);
```

#### 4.5 读
```gcc
    #include <unistd.h>
    // 避免越界
    ssize_t read(int fd, buf, size_t nbytes);


    #include <stdio.h>
    // 成功返回下一个字符，否则返回EOF
    int getc(FILE *fp);
    int fgetc(FILE *fp);
    int getchar(void);

    // 成功返回buf，失败或者到文件末尾返回NULL
    char* fgets(char *buf, int n, FILE *fp);
    char *gets(char *buf);


    // 二进制，返回读出的对象数，否则为-1, 参考write函数
    // nobj为对象数目，size为每一个对象的大小
    ssize_t fread(void *ptr, size_t size, size_t nobj, FILE *fp);
```

#### 4.6 File Buffer
##### 4.6.1 缓冲关系链
Std IO<----(fflush(stdout))---->App buf<--->IO例程<--(fsync)-->Kernel buf

##### 4.6.2 问答
问：IO为何被成为非缓冲IO？
> IO例程在用户态不存在任何的缓冲机制，所有的输入输出都会进入
内核缓冲中，所以，应该说相对于用户态是非缓冲的

问：fflush的限制
> 仅仅对stdout以及其他输出做限制

问：如何解决stdin缓冲导致的字符读入
> 利用while循环while ((c=getchar()) != '\n')清空多余的字符

问：标准IO中的缓冲区设置
```gcc
    // buf为0表示关闭，成功返回0
    setbuf(fp, buf)

    setvbuf(fp, buf, mode, size);
```

#### 4.7 Location
快速的移动文件中的指针
```gcc
    #include <unistd.h>
    // 成功返回新的文件偏移量，错误返回-1
    off_t lseek(int fd, off_t offset, int whence);


    #include <stdio.h>
    // 获取当前位置，python也有此函数以及相关用法
    // 成功返回文件位置，出错返回-1L
    long ftell(FILE *fp);
    // 设置文件游标，成功返回0
    int fseek(FILE *fp, long offset, int whence);
    // 指向文件头
    void rewind(FILE *fp);

    // 通用版本
    off_t ftello(FILE *fp);
    int fseeko(FILE *fp, off_t offset, int whence);
    int fgetpos(FILE *fp, fpos_t *pos);
    int fsetpos(FILE *fp, const fpos_t *pos);
```


### 5 Format IO
> printf和scanf都属于流IO，即标准IO

#### 5.1 Define
未格式化行IO
```gcc
    char* fgets(char*, int, FILE*);
    char* gets(char*);

    int fputs(char*, FILE*);
    int puts(char*);
```
格式化行IO
```gcc
    int fscanf(FILE*, char* format, ...);
    int sscanf(char*, char* format, ...);
    int scanf(char* format, ...);

    int fprintf(FILE*, char* format, ...);
    int snprintf(char*, size_t, char*format, ...);
    int sprintf(char*, char* format, ...);
    int printf(char* format, ...);
```
#### 5.2 Format
> 参考Pointer On C 308页，这里是介绍最为详细的，当然结合APUE中的介绍更好

scanf协议族：
```gcc
    格式：%[*][fldwidth][lenmodified]convtype
        *表示匹配的内容直接丢弃，不存储，用于跳过某些串，在printf不是该含义
        fldwidth表示输入字符的个数(最大)，如果不设置，默认读取到空白字符为止
        lenmodified限定符

    format字段可能包含的内容：
        空白字符——匹配输入串多个连续的空白字符
        格式代码——见C Primer Plus-68/APUE-124/Pointer On C 310说明
        其他字符——必须在输入串中找到相同的匹配串
```
printf协议族：
```gcc
    格式：%[flags][fldwidth][precision][lenmodifier]convtype]
        *表示宽度必须由参数指定
        flags（对齐输出/转换输出/0填充/符号输出，见Pointer On C 313页）
        fldwidth表示最小个数，注意和scanf协议族的区别
        precision表示精度
```


### 6 IO Model
同步和异步的对比关系：
- Synchronous IO：导致请求阻塞，知道IO操作完成
- Asynchronous IO：不导致请求阻塞
比较关系图：见UNP-127页

#### 6.1 Blocking IO
> 关于模型结构见UNP-123

IO例程/标准IO都属于阻塞IO，广泛意义上来说，IO复用，信号驱动IO都属于阻塞IO。

#### 6.2 NonBlock IO
> 关于模型结构见UNP-123；非阻塞说明见UNP-341

告知内核：如果请求的IO操作非的将当前进程投入睡眠状态等候时，返回一个错误信息，表示IO没有准备完毕。
非阻塞select/非阻塞connect/非阻塞accept

#### 6.3 IO Multicomplexing
> 关于模型结构见UNP-124；
> 阻塞过程相当于阻塞IO，当时可以返回多个文件状态；
> IO复用说明见UNP-127；

阻塞在select/poll/epoll系统调用上，而不是阻塞在真正的IO调用上。

#### 6.4 Signal-driven IO
> 关于模型结构见UNP-126; 
> 信号驱动式IO见UNP-626;

信号处理函数，由内核主动向进程递交SIGIO信号，告知IO完成，不过
仅仅适用于一个文件描述符。
##### 6.4.1 套接字
步骤：
- 建立SIGIO信号处理函数以及注册该信号
- 设置socket的属主
- 开启socket的信号驱动式IO
##### 6.4.2 适用场景
UDP-适用
TCP-几乎不适用


#### 6.6 Asynchronous IO
> 关于模型结构见UNP-126;
> Linux 2.6开始支持;

告知内核执行某一个IO操作，然后应用不用关注任何，内核自动的完成
IO的所有操作，这个不同于上面的所有操作

##### 6.6.1 基本API
```gcc
    aio_read            异步读操作
    aio_write           异步写操作
    aio_error           检查异步请求的状态
    aio_return          获得异步请求完成时的返回值
    aio_suspend         挂起调用进程，直到一个或者多个异步请求完成
    aio_cancel          取消异步请求
    lio_list            发起一系列异步IO请求
```


### 7 错误处理
#### 7.1 errno
> errno——number of last error，见<errno.h>

当系统调用或者库函数调用发生错误时，该值被重新设定，需要注意：
- 如果系统调用正确，errno不会清0，即君子从不给人面子，所以小人很烦心
- 系统调用正确，不能保证errno不会更改，反复无常还耍流氓
- 任何错误号都是非0

#### 7.2 Std IO
```gcc
    #include <stdio.h>
    // 判断是否存在错误或者是否eof，为真返回非0值
    int ferror(FILE *fp);
    int feof(FILE *fp);
    // 清楚错误标志位
    void clearerr(FILE *fp);


    // 自动获取errno的错误信息，和str一起输出到stdout
    // 在工程上并不适用
    #include <stdio.h>
    void perror(char *str);
```

#### 7.3 String
```gcc
    #include <sting.h>

    // 返回errno的字符串描述
    char* strerror(int errnum);

    // 指定缓存大小，更加安全
    int strerror_r(int errnum, char *buf, size_t n);
```
