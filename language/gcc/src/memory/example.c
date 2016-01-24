/*
 * func:verify the memory freed.
 */
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>

static void
freeMemory(char **buf)
{
    if (buf == NULL && *buf == NULL) {
        return;
    }

    //free(*buf);
    *buf = NULL;
}

int main()
{
    char        *buf = NULL;

    printf("My process ID is %d\n", getpid());
    buf = (char*)malloc(10000);
    strcpy(buf, "aljgelgje");

    freeMemory(&buf);
    if (buf == NULL) {
        printf("Free memory success in other scope.\n");
    } else {
        printf("failure!\n");
        free(buf);
    }

    return 0;
}
