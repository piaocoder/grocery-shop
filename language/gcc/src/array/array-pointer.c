#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(int argc, char **argv)
{
    int     array[3][3] = {{3,4,5},{10,5,6},{0,1,1}};
    int     **p = NULL;
    int     *l = NULL;

    p = (int **)array;
    l = *p+1;
    printf("%p, %p, %p, %p\n", p, l, array, array[0]);
    //printf("%d\n", *l);

    int s = 3;
    printf("%d %d\n", (s<<1), (s<<2));

    int     *head = NULL;

    head = (int *)malloc(100);
    if (NULL == head) {
        return -1;
    }
    memset(head, 0, 100);
    printf("address:%p\n", head);

    int (*pt)[3] = array;
    printf("%p, %p, %d, %d\n", pt+1, *pt, *(*pt+1), *(*pt+2));

    int abc[4] = {1, 2, 0};
    printf("%p %p \n", abc, &abc);

    return 0;
}
