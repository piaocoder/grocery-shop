#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <glob.h>

int main(int argc, char **argv)
{
    int         i = -1;

    for (i=0; i<10; ++i) {
        if (i == 5) {
            break;
        }
    }

    printf("i =%d\n", i);

    return 0;
}
