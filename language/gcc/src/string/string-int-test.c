#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv)
{
    char        intString[100] = {0};
    int         ret = -1;

    scanf("%s", intString);
    ret = atoi(intString);
    if (ret >43200 || ret <0) {
        printf("Input error! Result=%d\n", ret);
        exit(-1);
    }
    printf("ret=%d\n", ret);

    return 0;
}
