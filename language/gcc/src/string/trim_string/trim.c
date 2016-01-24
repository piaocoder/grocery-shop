/*
 * 功能：除去字符串首尾的字符
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * 功能:尾部字符
 */
int
string_trim_right(const char *src, char *dst, char *module)
{
    const char  *temp = src;
    char        c;

    if (!src || !dst || !module) {
        return -1;
    }

    // move to tail
    while (*(++temp) != '\0');

    while ((--temp) != src) {
        c = *temp;
        if (strchr(module, c) == NULL) {
            break;
        }
    }
    strncpy(dst, src, temp-src+1);
    dst[temp-src+1] = '\0';

    return 0;
}

int 
main(int argc, char **argv)
{
    char            *src = NULL;
    char            *module = NULL;
    char            dst[256];

    /* 去除字符串尾部的无效字符 */
    printf("******************************\n");
    src = "agege g egegge ge\t\n#\n";
    module = "\t\n#";
    dst[0] = '\0';
    if (string_trim_right(src, dst, module) < 0) {
        printf("函数调用错误！\n");
        exit(-1);
    }
    printf("源字符串:%s\n"
            "模式字符串:%s\n"
            "结果字符串:%s\n\n",
            src, module, dst);
    printf("******************************\n");

    return 0;
}
