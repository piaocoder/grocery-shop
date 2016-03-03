#include <stdio.h>
#include <stdlib.h>
#include <sys/reg.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <sys/user.h>

#define ORIG_EAX 1

int main()
{
    pid_t child;
    long orig_eax;

    child = fork();
    if(child == 0) {
        // 表示让别人跟踪自己，之后所有发送到当前
        // 进程的信号都被转发给父进程，此时当前进程
        // 状态为task_traced.
        printf("子进程ID：%d\n", getpid());
        ptrace(PTRACE_TRACEME, 0, NULL, NULL);
        printf("xxxx\n");
        execl("/bin/ls", "ls", NULL);
    } else {
        wait(NULL);
        // 通过ptrace，跟踪者获取被跟踪者的详细信息
        orig_eax = ptrace(PTRACE_PEEKUSER, 
                          child, 4 * ORIG_EAX, 
                          NULL);
        printf("The child made a "
               "system call %ld \n", orig_eax);
        // ptrace_cont表示使子进程继续系统调用过程
        ptrace(PTRACE_CONT, child, NULL, NULL);
    }
    return 0;
}
