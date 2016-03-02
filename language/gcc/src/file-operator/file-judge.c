#include "file.h"

void statDesc(int value)
{
    switch (value) {
        case EINVAL:
            printf("模式值无效\n");
            break;
        case EACCES:
            printf("文件或路径名中包含的目录不可访问\n");
            break;
        case ELOOP:
            printf("解释路径名过程中存在太多的符号连接\n");
            break;
        case ENAMETOOLONG:
            printf("路径名太长\n");
            break;
        case ENOENT:
            printf("路径名中的目录不存在或是无效的符号连接\n");
            break;
        case ENOTDIR:
            printf("路径名中当作目录的组件并非目录\n");
            break;
        case EROFS:
            printf("文件系统只读\n");
            break;
        case EFAULT:
            printf("路径名指向可访问的空间外\n");
            break;
        case EIO:
            printf("IO错误\n");
            break;
        case ENOMEM:
            printf("不能获取足够的内存\n");
            break;
        case ETXTBSY:
            printf("程序写入错误\n");
            break;
        default:
            printf("Other\n");
    } 
}

void fileInformation(struct stat *buf)
{
    mode_t          old;

    printf("文件的设备编号  :%u\n", (unsigned int)buf->st_dev);
    printf("文件的硬链接数目:%u\n", (unsigned int)buf->st_nlink);
    printf("用户ID          :%u\n", buf->st_uid);
    printf("文件大小        :%u\n", (unsigned int)buf->st_size);
    printf("文件属性        :\n");
    if (S_ISLNK(buf->st_mode)) {
        printf("%40s\n", "符号链接文件");
    }
    if (S_ISREG(buf->st_mode)) {
        printf("%40s\n", "普通文件");
    }
    if (S_ISDIR(buf->st_mode)) {
        printf("%40s\n", "目录文件");
    }
    if (S_ISCHR(buf->st_mode)) {
        printf("%40s\n", "字符设备文件");
    }
    if (S_ISBLK(buf->st_mode)) {
        printf("%40s\n", "块文件");
    }
    if (S_ISSOCK(buf->st_mode)) {
        printf("%40s\n", "SOCKET文件");
    }

    // 目录一般没有设置用户ID位以及设置用户组ID位
    if (!S_ISDIR(buf->st_mode)) {
        printf("文件的访问权限  :\n");
        if (S_ISUID&buf->st_mode) {
            printf("%40s\n", "设置用户ID位有效");
        }
        if (S_ISGID&buf->st_mode) {
            printf("%40s\n", "设置用户组ID位有效");
        }
    }
    printf("当前的权限为mask值为:\n");
    old = umask(S_IRUSR|S_IWGRP|S_IROTH);
    printf("%40s%o\n", " ", old);
}

/*
 * 功能:验证文件或者文件夹是否存在，如果是文件夹，返回>0的值
 * access:判断文件权限
 */
int fileHandle(char *name)
{
    int         ret = -1;
    struct stat buf; 

    ret = access(name, F_OK);
    if (ret < 0) {
        statDesc(errno);// 验证access的错误返回值和stat是一样的
        goto end;
    }

    ret = lstat(name, &buf);
    if (ret < 0) {
        statDesc(errno);
        goto end;
    }

    printf("FileExist:文件本身具有的属性如下:\n");
    fileInformation(&buf);

    /* 判断是否为一个文件夹 */
    if (S_ISDIR(buf.st_mode)) {
        ret = 1;
    }

end:
    return ret;
}

/*
 * 功能:遍历目录，其中depth决定扫描的层数
 */
int
file_directory_scan(const char *filepath, int depth)
{
    DIR                 *dp;
    struct dirent       *entry;
    struct stat         statbuf;

    if (!filepath) {
        return -1;
    }

    if ((dp = opendir(filepath)) == NULL) {
        printf("DirectoryScan:打开目录失败!\n");
        goto end;
    }
    /* 跳转到目标目录 */
    chdir(filepath);
    /* 开始扫描 */
    while ((entry=readdir(dp)) != NULL) {
        lstat(entry->d_name, &statbuf);
        if (S_ISDIR(statbuf.st_mode)) {
            if (strcmp(".", entry->d_name) == 0 ||
                    strcmp("..", entry->d_name) == 0) {
                continue;
            }
            printf("%*s%s%*c目录\n", 
                    depth, " ", entry->d_name,
                    8, '\t');
            if (depth == 1) {
                continue;
            }
            file_directory_scan(entry->d_name, depth-1);
        } else {
            printf("%*s%s%*c其他\n", 
                    depth, " ", entry->d_name, 
                    8, '\t');
        }
    }
    /* 跳转回前一个目录 */
    chdir("..");
    closedir(dp);

end:
    return 0;
}

void clear_stdbuf()
{
    int         c;
    while((c=getchar()) != '\n');
}

int main(int argc, char **argv)
{
    char            name[256] = {0};
    int             ret = -1;
    int             c = 0;

    do {
        printf("=======================================\n");
        printf("输入路径名称:");
        scanf("%s", name);
        if (strcmp(name, "quit") == 0) {
            break;
        }
        clear_stdbuf();
        ret = fileHandle(name);
        if (ret > 0) {
            printf("是否要遍历目录并打印:(y/n):");
            scanf("%c", (char*)&c);
            clear_stdbuf();
            if (c == 'y') {
                file_directory_scan(name, 1);
            }
        }
    } while(1);

    return 0;
}
