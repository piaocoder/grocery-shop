#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>


int main(int argc, char **argv)
{
    FILE        *fp;

    fp = fopen("./store.sh", "w+");

    while (1) {
        fputs("test test\n", fp);
        fflush(fp);
        sleep(2);
    }

    fclose(fp);
    return 0;
}
