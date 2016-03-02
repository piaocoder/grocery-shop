#include "file.h"

/*
 * 功能:清空文件
 */
int file_clear(const char *filename)
{
    int     ret = -1;

    if (!filename) {
        return -1;
    }

    if ((ret=truncate(filename, 0)) < 0) {
        printf("%s\n", strerror(errno));
        return -1;
    }

    return 0;
}

/*
 * 功能：打印文件中的所有数据，每次读取一行
 */
int
file_display(const char *filename)
{
    char        buf[1024];
    FILE        *fp = NULL;

    if (filename == NULL) {
        return -1;
    }

    fp = fopen(filename, "r");
    if (fp == NULL) {
        return -1;
    }

    printf("OUTPUT:文件%s内容为:\n", filename);
    while (fgets(buf, 1024, fp) != NULL) {
        printf("%s", buf);
    }
    printf("\n");

    return 0;
}
