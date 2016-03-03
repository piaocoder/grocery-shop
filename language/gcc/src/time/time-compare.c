#include "time-config.h"

int 
main(int argc, char **argv)
{
    time_t              t1 = 1450332981;
    time_t              t2 = 1450332992;
    time_t              now;
    struct tm           tm1, tm2;
    struct tm          *ptm = NULL, *ptm2 = NULL;

    time(&now);

    printf("T1=%ld, T2=%ld, now:%ld.\n", t1, t2, now);

    memcpy(&tm1, localtime(&t1), sizeof(struct tm));
    memcpy(&tm2, localtime(&t2), sizeof(struct tm));
    printf("TM1:%d, TM2:%d.\n", tm1.tm_sec, tm2.tm_sec);

    ptm = localtime(&t1);
    ptm2 = localtime(&t2);
    printf("PTM1:%d, PTM2:%d.\n", ptm->tm_sec, ptm2->tm_sec);
    printf("Time:%ld\n", mktime(ptm));
    return 0;

    return 0;
}
