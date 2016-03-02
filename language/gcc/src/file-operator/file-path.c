#include "file.h"

/*
 * 功能:获取当前目录的绝对路径
 * 1,realpath在开机启动时会出现错误
 * 2,getcwd在开机启动时会出现错误
 * 3,readlink会将首参数的内容连接到buf空间，返回不以NULL结尾
 *      的字符串，返回字符数目
 */
int
file_absolute_path()
{
    char        absPath[256];
    char        exePath[128];
    int         i, rslt;

    /* 获取当前目录的绝对路径 */
    if (NULL == realpath("./", absPath)) {
        printf("Get absolute path failure when call realpath!\n");
        goto end;
    }
    strcat(absPath, "/");
    printf("Realpath:\n"
            "\t当前工作目录绝对路径--%s\n", absPath);

    if (NULL == getcwd(absPath, 256)) {
        printf("Get absolute path failure when call getcwd!\n");
        goto end;
    }
    strcat(absPath, "/");
    printf("Getcwd:\n"
            "\t当前工作目录绝对路径--%s\n", absPath);

    rslt = readlink("/proc/self/exe", absPath, 256);
    if (rslt < 0 || rslt >= 256) {
        printf("Get absolute path failure when call readlink!\n");
        goto end;
    }
    absPath[rslt] = '\0';
    exePath[0] = '\0';
    for (i=rslt; i>=0; i--) {
        if (absPath[i] == '/') {
            strncpy(exePath, &absPath[i+1], rslt-i);
            exePath[rslt-i+1] = '\0'; 
            absPath[i+1] = '\0';
            break;
        }
    }
    printf("Reallink:\n"
            "\t工作目录绝对路径为:%s\n"
            "\t执行文件名为:%s\n",
            absPath, exePath);

end:
    return 0;
}

/*
 * 功能：验证dirname以及basename函数
 * 1,可能会更改参数的值，所以调用strdup进行拷贝
 */
int
file_path_phase(char *filepath)
{
    char        *temp = NULL;

    if (!filepath) {
        return -1;
    }

    temp = strdup(filepath);
    printf("PathPhase:\n"
            "\t全路径为:    %s\n"
            "\t目录为:      %s\n"
            "\t文件名为:    %s\n",
            filepath, dirname(temp), basename(temp));

    return 0;
}

int
main(int argc, char **argv)
{
    printf("===========================absolute-path=============\n");
    file_absolute_path();
    printf("\n");

    printf("===========================path-phase=============\n");
    file_path_phase("/home/grocery-shop/language/"
                    "python/requestsPackage/sendRequest.py");

    printf("\n");
    return 0;
}
