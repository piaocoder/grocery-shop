#include "file.h"

/*
 * 功能：测试一个文件是否可以同时写入以及读出
 * 1，fputs同write函数，写入文件时，不会删除为覆盖的字节
 */
int file_rw() 
{
    FILE            *fp = NULL;
    char            buf[1024];
    //const char      *desc = "Input data into buffer!\nI'm a super hero!";
    const char      *desc = "I'm a superman";
    long            pos = 0;

    fp = fopen(FILENAME_RW, "a+");
    if (!fp) {
        printf("打开文件失败\n");
        return 0;
    }
    // clear filename
    if (file_clear(FILENAME_RW) < 0) {
        goto end;
    }

    buf[0] = '\0';
    printf("RW:写入字符串:%s\n", desc);
    if (fputs(desc, fp) < 0) {
        printf("文件写入失败!\n");
        goto end;
    }
    if (fputs(desc, fp) < 0) {
        printf("文件写入失败!\n");
        goto end;
    }
    if (fgets(buf, 1024, fp) < 0) {
        printf("读取文件信息失败！\n");
        goto end;
    }
    if (strlen(buf) == 0) {
        printf("RW：文件已经到末尾，当前文件偏移量-%ld\n", (pos=ftell(fp)));
        printf("    尝试跳转偏移量到文件头部并刷新缓存，此时读取字符串:\n");
        fseek(fp, 0L, SEEK_SET);
        fflush(fp);
        if (fgets(buf, 1024, fp) < 0) {
            printf("    读取文件信息失败！\n");
        }
        printf("    读取文件：%s\n", buf);
    } else {
        printf("RW:读取文件：%s\n", buf);
    }
    printf("\n");

end:
    if (fp) {
        fclose(fp);
    }
    return 0;
}

/*
 * 功能：将一个结构体数据写入到文件中并读取
 */
int file_binary_rw()
{
    FILE                *fp = NULL;
    long                pos = 0;
    int                 i, ret, j;
    fileObjectUnit      objectArray[128], *tmpUnit, unit;

    fp = fopen(FILENAME_BINARY_RW, "a+");
    if (!fp) {
        printf("打开文件失败\n");
        return 0;
    }
    // clear file
    if (file_clear(FILENAME_BINARY_RW) < 0) {
        goto end;
    }
    
    printf("目标文件：%s\n", FILENAME_BINARY_RW);
    printf("BinaryRw：构建结构体单元数据, 写入128单元数据\n");
    for (i=0; i<128; i++) {
        tmpUnit = &objectArray[i];
        tmpUnit->id = i;
        sprintf(tmpUnit->desc, "单元-%d", i);
    }
    ret = fwrite((void*)&objectArray[0], sizeof(fileObjectUnit), 128, fp);
    if (ret != 128) {
        printf("Warnning:读入的单元数为:%d\n", ret);
    }

    printf("BinaryRw：刷新缓存并开始读取(6-10)单元数据\n");
    fflush(fp);
    fseek(fp, 0L, SEEK_SET);
    memset(&objectArray[0], 0, sizeof(objectArray));
    pos = sizeof(fileObjectUnit) * 5;
    fseek(fp, pos, SEEK_SET); 
    ret = fread((void*)&objectArray[5], sizeof(fileObjectUnit), 5, fp);
    if (ret != 5) {
        printf("Warnning:读取的单元数为:%d\n", ret);
    }
    for (j=5; j<10; j++) {
        printf("ID=%d 描述:%s\n", objectArray[j].id, objectArray[j].desc);
    }
    printf("BinaryRw：读取126号单元数据:\n");
    memset(&unit, 0, sizeof(fileObjectUnit));
    fseek(fp, (long)sizeof(fileObjectUnit)*125, SEEK_SET);
    if ((ret = fread(&unit, sizeof(fileObjectUnit), 1, fp)) < 0) {
        printf("Warnning:读取信息失败\n");
    }
    printf("ID=%d 描述:%s\n", unit.id, unit.desc);
    printf("\n");

end:
    if (fp) {
        fclose(fp);
    }
    return 0;
}

#define FILE_BUFSIZE    50
    char        outbuf[FILE_BUFSIZE];
/*
 * 功能:测试setbuf函数
 * 疑惑：如果缓存过小，并且不再fflush的话，会出现一些问题
 */
int
file_setbuf(void)
{
    setbuf(stdout, outbuf);
    memset(outbuf, 0, FILE_BUFSIZE);

    if (puts("This output will go into outbuf, so what?") < 0) {
        printf("-----------1\n");
        return -1;
    }
    memset(outbuf, 0, FILE_BUFSIZE);
    //fflush(stdout);

    if (puts("This is a test of buffered output._") < 0) {
        printf("-----------1\n");
        return -1;
    }
    memset(outbuf, 0, FILE_BUFSIZE);
    //fflush(stdout);


    if (puts("and won't appear until the buffer") < 0) {  
        printf("-----------1\n");
        return -1;
    }
    memset(outbuf, 0, FILE_BUFSIZE);
    //fflush(stdout);


    if (puts("fills up or we flush the stream.") < 0) {
        printf("-----------1\n");
        return -1;
    }
    memset(outbuf, 0, FILE_BUFSIZE);

    return 0;
}

/*
 * 功能:缓冲区问题
 * 实现：当缓冲区过小时，多次重复读取fgets函数
 */
#define BUF_SIZE    4
int
file_buf_verify()
{
    char        buf[BUF_SIZE];

    setbuf(stdout, NULL);
    while (fgets(buf, BUF_SIZE, stdin) != NULL) {
        if (fputs(buf, stdout) == EOF) {
            printf("output error!\n");
        }
        printf("\t\t-=\n");
    }

    return 0;
}

int main(int argc, char **argv)
{
    printf("===================RW===================\n");
    file_rw(); 

    printf("===================BinaryRW===================\n");
    file_binary_rw(); 

    printf("===================Setbuf=====================\n");
    file_setbuf();

    printf("===================buf verify=====================\n");
    file_buf_verify();

    printf("\n");
    return 0;
}
