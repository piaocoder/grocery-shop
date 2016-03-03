/**
 * @file orphan-test.c
 * @brief   孤儿进程测试代码
 * @author unlessbamboo
 * @version 1.0
 * @date 2015-11-03
 */

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>

int main()
{
    pid_t pid;
    //创建一个进程
    pid = fork();
    //创建失败
    if (pid < 0)
    {
        perror("fork error:");
        exit(1);
    }
    //子进程
    if (pid == 0)
    {
        printf("Children:I am the child process.\n");
        //输出进程ID和父进程ID
        printf("Children:pid: %d\tppid:%d\n",getpid(),getppid());
        //睡眠5s，保证父进程先退出
        while(1);
        printf("Children:pid: %d\tppid:%d\n",getpid(),getppid());
        printf("Children:child process is exited.\n");
    }
    //父进程
    else
    {
        printf("Father:I am father process.\n");
        //父进程睡眠1s，保证子进程输出进程id
        sleep(1);
        printf("Father:father process is  exited.\n");
    }
    return 0;
}
