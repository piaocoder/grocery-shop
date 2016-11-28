---
进程知识点
---


### 1 Introduction
#### 1.1 Reason
进程的优势和产生原因
#### 1.2 Usages
进程的基本操作
#### 1.3 IPC通信
管道/FIFO/消息队列/信号/共享内存/socket/UNIX socket
#### 1.4 Signal
信号详解
#### 1.5 others
关于进程环境/控制等内容见APUE介绍


### 2 Reasons
多task系统，操作系统进行某一个task调度的最小基本单位，每一个
task都是一个闭合环，拥有自己的资源和空间，不同的task之间一般
不会相互影响。  
程序是指令，进程是实体。  
> 关于并发并行等信息见concurrency.md文档说明那


### 3 Usages
#### 3.1 标识
唯一ID，例如0为调度进程，1为init进程，2为pagedaemon守护
##### 3.1.1 获取
```gcc
    #include <unistd.h>

    // 获取进程id
    pid_t getpid(void);
    pid_t getppid(void);

    // 获取该进程所属的实际用户ID
    pid_t getuid(void);

    // 获取进程的有效用户ID
    pid_t geteuid(void);

    // 获取进程所属组ID
    gid_t getgid(void);

    // 获取有效组ID
    gid_t getegid(void);

    
    // 获取登陆的用户名（用处不大）
    char* getlogin(void);
```
##### 3.1.2 设置
```gcc
    # include <unistd.h>

    // 实际用户ID
    int setuid(pid_t uid);
    int setgid(gid_t gid);

    // 有效用户ID
    int seteuid(pid_t uid);
    int setegid(gid_t gid);
```

#### 3.2 创建
> 写时复制，所以fork一个进程时代价不是非常高。
##### 3.2.1 子进程
```gcc
    #include <unistd.h>

    // 子进程返回0，父进程返回子进程ID，有理有据
    pid_t fork(void);

    // 伪fork，阻塞父进程，直到子进程调用exit或者exec
    pid_t vfork(void);
```
##### 3.2.2 覆盖进程
全新的程序替代当前的正文/数据/堆栈，但是pid_t值不变。
```gcc
    #include <unistd.h>

    // 基本操作list或者vector
    int execl(const char *path, const char *arg0, ...);
    int execv(const char *path, char* const argv[]);


    // 添加环境变量
    int execle(const char *path, const char *arg0, ..., 
                char* const envp[]);
    int execve(const char *path, char* const argv[], 
                char* const envp[]);


    // 文件名，在PATH中查找文件
    int execlp(const char *file, const char *arg0, ...);
    int execvp(const char *file, char* const argv[]);
```
##### 3.2.3 封装者
利用fork和exec系列、wait函数，封装进程的创建，从而更加简单的提供
新进程的创建接口。
```gcc
    #include <stdlib.h>

    // 系统调用，返回-1(fork失败),-127(exec失败)，或者终止码
    int system(const char *cmdstring);

    // 利用fork/exec/pipe技术，进行单向通信
    FILE* popen(const char* cmd, const char* type);
```

#### 3.3 关闭
##### 3.3.1 进程退出情况
- main返回
- exit
- 最后一个线程例程返回
- 最后一个线程pthread_exit退出

- abort异常退出
- 捕捉信号异常并关闭所有
- 最后一个线程出发pthread_cancel

##### 3.3.2 函数
```gcc
    #include <stdlib.h>
    void exit(int status);
    int atexit(void (*func)(void));
    #include <unistd.h>
    void _exit(int status);

    // 异常终止
    void abort(void);
    // 睡眠
    unsigned int sleep(unsigned int seconds);
```
##### 3.3.2 善后处理
等待一个进程的退出状态码，判断是否正常执行完毕，popen就是利用该函数
返回值说明：
```
    pid == -1           等待任意子进程
    pid > 0             等待某一个指定进程
    pid == 0            等待同组ID进程
    pid < -1            等待|pid|绝对值相同的组ID
```
statloc状态码说明：
```
    WIFEXITED(status):
        正常exit返回

    WIFSIGNALED(status):
        信号异常返回，利用Wtermsig(status)来获取子进程信号编号

    WIFSTOPPED(status):
        子进程暂停返回，利用Wstopsig(status)获取信号编号

    WIFCONTINUED(status):
        子进程暂停后继续，仅仅适用于waitpid
```
函数
```gcc
    #include <sys/wait.h>

    // 阻塞等待所有子进程返回，其中statloc返回终止状态码
    pid_t wait(int* statloc);


    // 等待指定或者所有
    pid_t waitpid(pid_t pid, int *statloc, int options);
```


### 4 IPC
#### 4.1 管道
半双工，在具有公共祖先的进程之间使用，例如父子。
> pclose/popen就是利用管道来实现
```gcc
    #include <unistd.h>
    // 成功返回0，出错返回-1，其中fd[0]读，fd[1]写
    // 例如父进程读取子进程数据，则关闭父进程的fd[1]，子进程fd[0]
    int pipe(int filedes[2]);
```

#### 4.2 命名管道
命名管道，在任意进程之间，创建FIFO类型文件，依托中介来进行。其中
文件IO函数可以用于该文件。
> 其实就是一个简化版/单机版的socket，自己处理数据原子同步问题
```gcc
    #include <sys/stat.h>

    // 成功返回0，失败返回-1
    int mkfifo(const char* pathname, mode_t mode);
```

#### 4.3 消息队列
消息队列——消息的链接表，每一个节点是一个结构体
消息组成——类型字段、非负长度、实际数据字节
##### 4.3.1 创建
```gcc
    #include <sys/msg.h>
    // 打开或者创建一个消息队列，成功返回消息队列ID
    int msgget(key_t key, int flag);
```
##### 4.3.2 入队
```gcc
    #include <sys/msg.h>
    // 成功返回0
    int msgsnd(int msgid, const void*ptr, size_t nbytes, int flag);

    // 消息结构的一种可能形式
    struct mymsg {
        long    mtype;      // 类型
        char    mtext;      // 数据
    };
```
##### 4.3.3 出队
```gcc
    #include <sys/msg.h>
    // 成功返回消息的数据部分长度
    ssize_t msgrcv(int msgid, void*ptr, size_t nbytes, int flag);
```
##### 4.3.4 控制
> 参考ioctl杂项全能函数
```gcc
    #include <sys/msg.h>
    // 成功返回0
    int msgctl(int msgid, int cmd, struct msgid_ds *buf);
```

#### 4.4 信号量
semaphore——计数器，类似条件变量，用于多进程对于共享数据对象的访问
##### 4.4.1 获取资源过程
- 测试控制某一个资源的信号量
- 如果信号量值为正，使用该资源，同时-1
- 如果信号量值为0，阻塞休眠
##### 4.4.2 使用
```gcc
    #include <sys/sem.h>

    // 获取一个信号量集ID，关于key_t见APUE-415页
    int semget(key_t key, int nsems, int flag);

    // 控制信号量的执行，类似fcntl函数
    int semctl(int semid, int semnum, int cmd, ...);

    // 根据设置好的信号量集合，执行相应数组
    int semop(int semid, struct sembuf semoparrray[], size_t nops);
```
> 关于信号量和记录锁的耗时比较，见APUE-426，前者效率高，但是复杂

#### 4.5 共享内存
##### 4.5.1 获取共享存储
```gcc
    #include <sys/shm.h>
    // 成功返回共享存储ID
    int shmget(key_t key, size_t size, int flag);

    // 链接共享内存，成功返回指向共享内存的指针
    void* shmat(int shmid, const void*addr, int flag);

    // 脱离共享内存
    int shmdt(void *addr);

    // 控制函数，参考前面以及fcntl/ioctl函数
    int shmctl(int shmid, int cmd, struct shmid_ds *buf);
```

#### 4.6 socket
网络IPC最常用形态，变形金刚-擎天柱，具体见socket.md

#### 4.7 unix socket
单机网络IPC，考虑程序的兼容以及编程习惯嘛，速度用于socket
##### 4.7.1 创建
```gcc
    #include <sys/socket.h>
    // 成功返回0
    int socketpair(int domain, int type, 
                    int protocol, int sockfd[2]);
```
##### 4.7.2 命名unix socket
```gcc
    #include <sys/socket.h>
    #include <sys/un.h>

    struct socketaddr_un un;
    un.sun_family = AF_UNIX;
    strcpy(un.sun_path, "unix.socket");
    fd = socket(AF_UNIX，SOCK_STREAM, 0);
    ...
```

#### 4.8 基于STREAMS的管道
