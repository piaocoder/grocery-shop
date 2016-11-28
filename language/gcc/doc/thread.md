---
线程的知识点
---


### 1 Introduction
> 关于线程控制，为了简单化，请将使用和控制分离开来，见APUE详细介绍

#### 1.1 Reason
线程产生的原因、优势。
#### 1.2 LWP
LWP、thread ID、pstree输出的线程ID。
#### 1.3 Usages
线程的基本操作函数。
#### 1.4 pid and threadid
进程和线程的某些操作共通之处。
#### 1.5 synchronized
同步操作使用的场景。
#### 1.6 Reentrancy
可重入机制介绍
#### 1.7 Private
线程私有数据。
#### 1.8 embrace
死锁产生的情景以及解决办法。


### 2 Reason
#### 2.1 需求
- 简化处理异步事件
- 改善程序的吞吐量
- 改善程序的响应时间，特别是交互程序
- 多核时代，多线程在多处理器上结合多进程
#### 2.2 并发和并行
关于同步操作的使用场景，见下面的Synchronized章节说明。
- 并发：伪并行
- 并行：多核时代


### 3 LWP
#### 3.1 含义
各个值所代表的含义如下：
```
    getpid()            获取进程pid_t值信息
    gettid()            获取线程LWP值信息，见pstree或者ps -Lf输出
    pthread_self()      获取线程id标识符pthrea_t值信息
```
#### 3.2 原因
Glibc实现*用户态线程*，Linux内核加了线程支持后，内核线程和用户态线程
形成一种对应关系（一一/一对多）,每一个POSIX thread id对应一个kernel 
thread id，但是两者的实际值时不一样的，其中POSIX thread id由于平台
无关性，是一个unsigned long int的唯一值：
```
    Kernel thread id == gettid() == LWP
    POSIX thread id == pthread_self()
```
#### 3.3 使用
以下是使用例子
```
    #include <pthread.h>
    #include <linux/unistd.h>
    #include <sys/syscall.h>

    void *printid(void *ptr)
    {
        printf("thread ID:%u, LWP:%u.\n", 
                syscall(__NR_gettid),
                (unsigned int)pthread_self());
    }

    int main() 
    {
        pthread_t   p;
        pthread_create(&p, NULL, printid, "thread1");
        pthread_join(p, NULL);

        return 0;
    }
```


### 4 Usages
> 具体用法请见APUE以及相关资料，这里仅仅作为一个线程概况，从而加深理解
#### 4.1 基本操作
##### 4.1.1 标识
```gcc
    #include <pthread.h>

    // 获取线程自身ID，返回unsigned long int的线程ID
    pthread_t pthread_self(void);

    // 比较两个线程，类似strcmp的返回值
    int pthread_equal(pthread_t p1, pthread_t p2);
```
##### 4.1.2 创建
```gcc
    #include <pthread.h>
    
    // 创建线程，类似信号处理函数（信号处理和线程不一样哦）加入回调函数
    // 失败返回错误的正值编号，见<sys/errno.h>
    int pthread_create(pthread_t *tp, const pthread_attr_t *attr, 
            void*(*cb)(void *), void *arg);
```
##### 4.1.3 关闭
线程退出有三种方式：
- 启动例程执行完毕，自动返回，即cb函数返回，返回值为线程的<u>退出状态码</u>
- 被其他线程终止
- 启动例程本身调用pthrea_exit提前终止

见如下：
```gcc
    #include <pthread.h>

    // 第二种
    // 该方式其实少用，并且目标线程本身可以忽略该请求，具体见APUE线程控制章节
    int pthread_cancel(pthread_t tid);
    
    // 第三种
    void pthread_exit(void *ptr);
```
另外，关闭时的辅助函数有
```gcc
    // 阻塞等待线程，类似pid中的waitpid函数
    // 其中线程的返回状态码通过Ptr来返回
    int pthread_join(pthread_t tid, void* ptr);

    // 线程的退出回调函数，类似atexit函数
    void pthread_cleanup_push(void (*cb)(void*), void *arg);
    void pthread_cleanup_pop(int execute);
```
##### 4.1.4 分离
线程状态：可汇合（joinable），脱离的（detached）  
其中joinable线程在终止时会将tid和退出状态码返回给pthread_join调用者，后者
detached则会释放所有资源，不给他人留下任何信息。
```gcc
    #include <pthread.h>

    // 将指定线程设置为detached状态
    // 成功返回0，失败返回Exxx值
    int pthread_detach(pthread_t tid);
```

#### 4.2 同步机制
##### 4.2.1 mutex
```gcc
    #include <pthread.h>
    
    // 初始化互斥量，成功返回0，失败返回错误码
    int pthread_mutex_init(pthread_mutex_t *mutex,
                    const pthread_mutexattr_t *attr);
    
    // 释放互斥量
    int pthread_mutex_destroy(pthread_mutex_t *mutex);

    // 加解锁，失败返回错误码
    int pthread_mutex_lock(pthread_mutex_t *mutex);
    int pthread_mutex_trylock(pthread_mutex_t *mutex);
    int pthread_mutex_unlock(pthread_mutex_t *mutex);
```
##### 4.2.2 rwlock
```gcc
    #include <pthread.h>

    // 初始化，成功返回0，失败返回错误码
    int pthread_rwlock_init(pthread_rwlock_t *rwlock, 
                    const pthread_rwlockattr_t *attr);
    
    // 释放读写锁
    int pthread_rwlock_destroy(pthread_rwlock_t *rwlock);

    // 加读锁
    int pthread_rwlock_rdlock(pthread_rwlock_t *rwlock);
    // 加写锁
    int pthread_rwlock_wrlock(pthread_rwlock_t *rwlock);
    // 解锁
    int pthraed_rwlock_unlock(pthread_rwlock_t *rwlock);
```
##### 4.2.3 cond
> 注意，条件变量外面必须用互斥量进行保护，（^ ^)
```gcc
    #include <pthread.h>

    // 初始化，成功返回0，失败返回错误码
    int pthread_cond_init(pthread_cond_t *cond, 
                    const pthread_condattr_t *attr);
    // 释放
    int pthread_cond_destroy(pthread_cond_t *cond);


    // 阻塞等待通知
    int pthread_cond_wait(pthread_cond_t *cond, 
                    pthread_mutex_t *mutex);
    // 超时等待通知
    int pthread_cond_timewait(pthread_cond_t *cond,
                    pthread_mutex_t *mutex,
                    const struct timespec *timeout);


    // 唤醒某个线程
    int pthread_cond_signal(pthread_cond_t *cond);
    // 唤醒所有线程（广播）
    int pthread_cond_broadcast(pthread_cond_t *cond);
```


### 5 Synchronized
#### 5.1 同步机制
- 互斥量——对某一个共享资源的限定访问，使用线程个数较少情况
- 读写锁——适用于额外的第三种状态，不会资源产生副作用的操作
- 条件变量——等待共享资源，无竞争的获取共享资源，适用多线程
#### 5.2 使用场景
##### 计算密集型
- 多核CPU-可以使用多鲜橙
- 单核CPU-没有意义
##### IO密集型
- 多核CPU-多进程或者多线程
- 单核CPU-尽可能使用多线程，增加人机交互效率


### 6 Reentrancy
> 可重入，即异步操作对象是同一个函数时，是否会产生错误操作。
#### 6.1 异步-信号安全
> 适用于多进程或者信号处理函数
##### 6.1.1 不可重入原因
- 使用静态数据结构
- 调用malloc/free
- 使用标准IO函数，但是该库使用外部连接、文件作用域变量
###### 6.1.2 例子
例如信号处理函数中，errno的变化，所以在调用信号处理函数之前，尽量
保存旧有的errno值。

#### 6.2 线程安全
> 适用于多线程
##### 6.2.1 非线程安全原因
见上面描述，以及资源竞争导致的不可预知、不可复现后果。

#### 6.3 重入/线程/信号
一个函数是线程安全的，但是并不代表它是异步-信号安全的；  
反之呢？


### 7 Private
> 见UNP-534，APUE-328
#### 7.1 原因
```
    底层的实现部分不能阻止这种跨线程访问能力（线程拥有进程的整个
    地址空间访问权限），但是管理线程私有数据的函数可以提高线程见的独
    立性。
```
线程不同于进程，本身不占用资源，所以产生了此类私有数据机制，可以
独立的访问私有数据，不担心其他线程的同步访问问题。
- 虽然我是自由民主人士，但是我也希望保持一点隐私
- 提供了基于进程的接口适应于线程的机制，复用才是王道

#### 7.2 基本使用
```gcc
    #include <pthread.h>

    // 1, 创建私有数据key，成功返回0，失败返回错误编号
    // destructor是析构函数，在正常推出时调用
    int pthread_key_create(pthread_key_t *keyp, 
                        void (*destructor)(void*));

    // 2, 删除key和data的关联性
    int pthread_key_delete(pthread_key_t *key);

    // 3, 可能存在多个线程多次调用key_create，但是实际上只需要一个
    // 解决办法：pthread_once，保证key仅仅调用一次

    // 必须全局变量或者静态变量，其中initfn用于创建key
    pthread_once_t initflag = PTHREAD_ONCE_INIT 
    int pthread_once(pthread_once_t *initflag,
                    void (*initfn)(void));

    // 4, 关联key和values值，这时候才会绑定value
    void* pthread_getspecific(pthread_key_t key);
    int pthread_setspecific(pthread_key_t key, const void *value);
```
#### 7.3 原理
每一个系统支持有限数量的线程特定数据元素，其中POSIX规定不小于128，
其中，整个数组存储在pthread结构中：
```gcc
    struct pthread {
        /* 其他线程信息 */

        pkey[0];
        pkey[1];
        ...
        pkey[127];
    };
```


### 8 Embrace
情况1：
```
    同一个线程对一个资源锁定两次，没有提前预判
    A--------lock------>a
    A------->阻塞请求----->a
```
情况2：
```
    A------->lock--------->a
    B------->lock--------->b

    A-------阻塞请求------>b
    B-------阻塞请求------>a
```
