#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv)
{
    char        *a = "algelge";
    char        pre[100] = {"gegegegegeggege"};

    printf("%d\n", strlen(a));
    a = "";
    printf("%d\n", strlen(a));

    strcpy(pre, "assss");
    printf("%s\n", pre);

    return 0;
}
