#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<signal.h>

int
main(int argc, char **argv)
{
    int         ret = -1;

    ret = kill(3222, SIGTERM);
    printf("return status is :%d\n", ret);

    return 0;
}
