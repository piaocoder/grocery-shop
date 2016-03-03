#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#define RAND_CALCULATE(x)  \
        (rand()*(x) / RAND_MAX + 1)

int main(int argc, char **argv)
{
    int             count = 8;
    int             i = 0;

    srand(time(0));

    for (i=0; i<count; i++) {
        printf("%d ", rand()%10);
    }

    printf("\n执行rand之后的值\n");

    for (i=0; i<1000; i++) {
        //printf("%d-", RAND_CALCULATE(10));
        printf("%d--", (int)(10.0*rand()/(RAND_MAX)));
    }

    printf("End\n");
    return 0;
}
