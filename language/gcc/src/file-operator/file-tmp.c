#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/*
 * 功能：测试tmpnam函数的功能
 * 1，产生唯一路径文件名，并保存到数组参数中，并返回数组地址
 * 2，其中静态数组会一直存在，直到再次调用tmpnam或者程序停止
 * 3，返回一个唯一路径，但是文件并没有创建
 */
int 
tmpnam_test()
{
    char        name[L_tmpnam];
    FILE        *fp = NULL;
    char        *temp = NULL;
    char        tempName[L_tmpnam];

    printf("Tmpname:使用tmpnam创建一个临时文件:%s\n", 
                        (temp=tmpnam(NULL)));
    printf("Tmpname:拷贝文件并重新调用tmpnam函数:\n");
    strcpy(tempName, temp);
    printf("    新文件名:%s\n"
           "    旧指针名:%s\n"
           "    旧文件名:%s\n", 
                        tmpnam(NULL), temp, tempName);
    
    (void)fp;
    (void)name;
    /*
    fp = fopen(tempName, "w+");
    if (!fp) {
        printf("Temp file %s is open failure.\n", tempName);
    }
    fp.close();

    fp = fopen(temp, "w+");
    if (!fp) {
        printf("Temp file %s is open failure.\n", temp);
    }
    fp.close();

    tmpnam(name);
    printf("name=%s\n", name); 
    */

    return 0;
}

int tmpfile_test()
{
    FILE            *fp;
    char            line[128];

    fp = tmpfile();
    if (!fp) {
        printf("Tmpfile create failure!\n");
        return 0;
    }

    fputs("Whahahahhhah ahah  (~!_!~)\n", fp);
    rewind(fp);
    if (fgets(line, 128, fp) == NULL) {
        printf("Read information failure!\n");
        return 0;
    }

    printf("Line: %s\n", line);

    return 0;
}

int 
main(int argc, char **argv)
{
    printf("=====================tmpfile=================\n");
    tmpfile_test();
    printf("\n=====================tmpfile=================\n");
    tmpnam_test();

    printf("\n");
    return 0;
}
