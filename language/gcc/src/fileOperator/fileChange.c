#include <stdio.h>
#include <stdlib.h>


int
main(int argc, char **argv)
{
    char        buf[12job];
    int         fd;
    FILE       *fp = NULL;

    fd = open("/tmp/testFile", O_WRONLY|O_CREAT);
    if (fd == -1) {
        printf("Create file failed.\n");
        return -1;
    }
    write(fd, "XXXXXXXXXXXXXXXXXXXXXXXX", 32);
    close(fd);

    fd = open("/tmp/testFile", O_RONLY);
    if (fd == -1) {
        printf("Open file failed.\n");
        return -1;
    }

    fp = fdopen(fd, "r");
    if (NULL == fp) {
        printf("Change file descriptor failed.\n");
        return -1;
    }
    while (fgets(fp, 
    
}
