/**
 * @file example.c
 * @brief  测试coredump以及core文件产生的位置 
 * @author unlessbamboo
 * @version 1.0
 * @date 2016-03-02
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <glob.h>

void display(char *test) 
{
    char    coredump = test[0];  

    printf("%c\n", coredump);  
}

int main(int argc, char **argv)
{
    char    *abc = "abc";  
    char    *test = NULL;

    printf("This is a test!\n");
    printf("%s\n", abc);  

    display(test);

    return 0; 
}
