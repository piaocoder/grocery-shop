#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int    buf[4096] = {1,2,3};
int    temp[2048];


/** 
 * @brief   
 * 
 * @param   argc
 * @param   argv
 * 
 * @return  
 */
int main(int argc, char **argv)
{
    pid_t           pid;
    //FILE            *fd;
    int             ret = -1;

    /*printf("测试exec执行完成后，是否仍旧执行!\n");*/

    if ((pid=fork()) == 0) {
        printf("子进程启动:\n");
        //fd = fopen("b.sh", "w+");
        //dup2(fileno(fd), 1);
        //dup2(fileno(fd), 2);
        if ((ret = execlp("ps", "ps" " -ef", NULL)) < 0) {
            printf("调用execl函数失败！\n");
            exit(-1);
        }
        printf("调用execl函数结束!\n");
    }

    //sleep(5);
    //printf("父进程结束等待!!!!\n");

    return 0;
}
