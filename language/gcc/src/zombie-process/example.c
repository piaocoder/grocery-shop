#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>

int main()
{
    pid_t pid;
    pid = fork();
    if (pid < 0)
    {
        perror("fork error:");
        exit(1);
    }
    else if (pid == 0)
    {
        printf("Children:I am child process.My pid is %d. I am exiting.\n", getpid());
        exit(0);
    }
    printf("Father:I am father process.My pid is %d.I will sleep long long ago\n", getpid());
    //等待子进程先退出
    while(1);

    return 0;
}
