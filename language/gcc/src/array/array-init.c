/*
 * 功能：验证数组的初始化
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * 功能：初始化列表中出现多余逗号的用途
 */
int
array_extra_comma()
{
    int     array[] = {3, 4, 5, 8, 9, 10,};
    int     i;

    for(i=0; i<sizeof(array)/4; i++) {
        printf("%d\n", array[i]);
    }

    return 0;
}

int
main(int argc, char **argv)
{
    array_extra_comma();

    return 0;
}
