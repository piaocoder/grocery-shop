/*
 * 功能：测试信号处理的各个函数功能
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>

static void sig_quit(int);
static void sig_action(int);
static void sig_user1(int);
static void sig_alm(int);
static int signal_mask(void);
static int signal_action(void); 
static int signal_type_user(void); 
static int signal_type_alarm(void); 

static int global_alarm;

int
main(void)
{
    int         ret = -1;

    /* 第一个测试函数 */
    printf("=====================test mask=================\n");
    //ret = signal_mask();
    if (ret < 0) {
    }
    printf("=====================test Action=================\n");
    //ret = signal_action();
    if (ret < 0) {
    }

    printf("=====================test USER1=================\n");
    //ret = signal_type_user();
    if (ret < 0) {
    }

    printf("=====================test ALARM=================\n");
    ret = signal_type_alarm();
    if (ret < 0) {
    }
    
    return 0;
}

/*
 * 功能:SIGQUIT回调函数
 * PS:默认动作为退出并生成core文件(退出 (核心已转储))
 */
static void
sig_quit(int signo)
{
    printf("监听到信号--SIGQUIT!\n");
    if (signal(SIGQUIT, SIG_DFL) == SIG_ERR) {
        printf("can't reset SIGQUIT\n");
    }
}


/** 
 * @brief   SQGQUIT回调函数
 * 
 * @param   signo
 */
static void sig_action(int signo)
{
    printf("sig_action:监听到信号SIGQUIT!\n");
}


/** 
 * @brief   SIGUSR1触发函数
 * 
 * @param   signo
 */
static void sig_user1(int signo)
{
    printf("sig_action:监听到信号SIGUSR1!\n");
}

/** 
 * @brief   SIGALRM回调函数
 * 
 * @param   信号值 
 */
static void sig_alm(int signo)
{
    if (global_alarm == 0) {
        global_alarm = 1;
    }
    printf("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n");
}

/** 
 * @brief   测试alarm函数是否阻塞
 * 
 * @return  0 或者 -1 
 */
static int signal_type_alarm()
{
    int                 ret  = 0;

    if (signal(SIGALRM, sig_alm) == SIG_ERR) {
        printf("can't catch SIGALRM");
        ret = -1;        
        goto end;
    }

    printf("ALARM:开始设置定时器（7秒）:\n");
    alarm(20);
    
    if (global_alarm == 0) {
        printf("        (v_v)没有阻塞哦！调用pause阻塞.\n");
        pause();
    } else {
        printf("        (~_~)阻塞了！\n");
    }

end:
    return ret;
}

/** 
 * @brief   测试信号发生的三个动作，以及回调函数中的处理。 
 * 
 * @return  0
 */
__attribute__((unused))
static int signal_action()
{
    /* 注册SIGQUIT监听函数 */    
    if (signal(SIGQUIT, sig_action) == SIG_ERR) {
        printf("不能触发SIGQUIT信号!\n");
        return -1;
    }
    printf("Action:延时等待5秒，检查信号并进行回调处理:\n");
    pause();

    if (signal(SIGQUIT, SIG_IGN) == SIG_ERR) {
        printf("不能触发SIGQUIT信号!\n");
        return -1;
    }
    printf("Action:延时等待5秒，检查信号发生后是否被忽略:\n");
    sleep(5);

    if (signal(SIGQUIT, SIG_DFL) == SIG_ERR) {
        printf("不能触发SIGQUIT信号!\n");
        return -1;
    }
    printf("Action:延时等待5秒，检查信号发生后的默认动作:\n");
    pause();

    printf("signal_action end!\n");
    return 0;
}

/*
 * 功能；测试1
 */
__attribute__((unused))
static int signal_mask()
{
    sigset_t newmask, oldmask, pendmask;

    /* 注册SIGQUIT监听函数 */
    if (signal(SIGQUIT, sig_quit) == SIG_ERR) {
        printf("can't catch SIGQUIT");
        return -1;        
    }

    /* 阻塞SIGQUIT，持续5秒并保存当前的信号掩码以便现场恢复 */
    sigemptyset(&newmask);
    sigaddset(&newmask, SIGQUIT);
    if (sigprocmask(SIG_BLOCK, &newmask, &oldmask) < 0) {
        printf("SIG_BLOCK error\n");
        return -1;
    }
    if (sigismember(&newmask, SIGQUIT) == 0) {
        printf("阻塞SIGQUIT信号失败!\n");
        return -1;
    }
    printf("MASK：开始忽略信号SIGQUIT，持续时间5秒(请按ctrl+d测试)"
            "这期间产生的信号处于未决状态:\n");
    pause();
 
    /* SIGQUIT here will remain pending */
    if (sigpending(&pendmask) < 0) {
        printf("获取当前信号集，函数sigpending调用失败!\n");
        return -1;
    }
    if (sigismember(&pendmask, SIGQUIT)){
        printf("\nSIGQUIT pending，表示有信号产生并处于未决状态。\n");
    }

    /*
     * Reset signal mask which unblocks SIGQUIT.
     */
    if (sigprocmask(SIG_SETMASK, &oldmask, NULL) < 0) {
        printf("SIG_SETMASK error\n");
        return -1;
    }
    printf("MASK:SIGQUIT unblocked,少年，开始测试吧(100秒的机会)：\n");

    sleep(100); /* SIGQUIT here will terminate with core file */

    return 0;
}


/** 
 * @brief  测试SIGUSR1信号的触发 
 * 
 * @return 0/-1 
 */
__attribute__((unused))
static int signal_type_user()
{
    int         ret = 0;

    /*注册监听SIG_USR1信号*/
    if (signal(SIGUSR1, sig_user1) == SIG_ERR) {
        printf("can't catch SIGUSR1");
        ret = -1;
        goto end;
    }
    printf("TYPE_USER：开启监听SIGUSER1信号:\n");
    pause();

end:
    return ret;
}
