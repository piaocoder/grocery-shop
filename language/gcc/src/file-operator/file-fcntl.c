#include "file.h"

int main(int argc, char **argv)
{
    int         fd;
    const char  *buf = "--testfcntl写入的数据--\n";

    fd = atoi(argv[1]);
    printf("\t\t\t*******************\n");
    printf("子进程：pid=%d, fd=%d, 调用testfcntl执行文件:\n", getpid(), fd);
    write(fd, (void*)buf, strlen(buf));
    close(fd);

    return 0;
}

