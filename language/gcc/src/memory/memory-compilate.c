/**
 * @file memory-compilate.c
 * @brief 测试简介
 * @author unlessbamboo@gmail.com
 * @version 1.0
 * @date 2016-08-16
 */

#include <stdio.h>

 
/**
 * @brief showmsg 
 *
 * @param szMsg
 */
void showmsg(char *szMsg)
{
    printf("%s\n", szMsg);
}
 
int main(int argc, char **argv)
{
    char szMsg[] = "Hello, world!";
    showmsg(szMsg);
 
    return 0;
}
