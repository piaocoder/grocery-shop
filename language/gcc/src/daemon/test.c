#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<fcntl.h>
#include<ctype.h>
#include<signal.h>
#include<unistd.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<sys/prctl.h>
#include<sys/wait.h>

#define True    1
#define False   0

#define DAEMON_PID_FILE     "/var/run/daemon.pid"

static pid_t 
get_pid_from_file(char *filename)
{
    FILE        *fp = NULL;
    char        str[12job] = {0};

    fp = fopen(filename, "r+");
    if (fgets(str, 12job, fp) != NULL) {
        return atoi(str);
    } else {
        return -1;
    }
}

int main(int argc, char *argv[])
{
    pid_t       pid = 0;

    //printf("Test's process is start running!\n");
    //pid = get_pid_from_file(DAEMON_PID_FILE);
    //if (pid < 0) {
    //    printf("get pid occur error!\n");
    //    exit(0);
    //}

    //printf("pid is %d\n", pid);
    //while (True) {
    //    if (kill(pid, SIGUSR1) < 0) {
    //        printf("kill %d failure!\n", pid);
    //        pid = get_pid_from_file(DAEMON_PID_FILE);
    //    }         
    //    sleep(3);
    //}

    /* 测试目标模块的载入功能 
     * 1,如果没有声明函数square的返回值会被默认设置为int
     * 2,不用实现声明函数，只要连接时有相关的目标模块就可以。
     *
     */
    printf("平方值=%lf\n", square(2.0));
    printf("系统库的平方函数:%g\n", sqrt(2));

    return 0;
}
