/*
 * 功能:非缓存IO操作实例
 */
#include "file.h"

/*
 * 功能:测试多次打开同一个文件并读取和写入
 */
int
file_uncache_open_multi(const char *filename)
{
    int         fd1,fd2;
    char        buf[128];
    int         ret, i;

    fd1 = open(filename, O_RDWR|O_CREAT|O_TRUNC);
    if (fd1 < 0) {
        printf("打开文件失败！\n");
        return -1;
    }
    if ((ret=read(fd1, buf, 128)) < 0) {
        printf("读取失败!\n");
    }
    buf[ret] = '\0';
    printf("读取的字符串为:%s\n", buf);

    fd2 = open(filename, O_WRONLY);
    if (fd2 < 0) {
        printf("打开文件失败！\n");
        return -1;
    }
    for (i=0; i<120; i++) {
        buf[i] = 'a';
    }
    buf[i] = '\0';
    if ((ret = write(fd2, buf, 100)) < 0) {
        printf("写入文件失败！\n");
        return -1;
    }

    printf("通过fd再次读取字符，如果读取到字符，表示同一个进程只有"
            "一个files结构\n");
    if ((ret = read(fd1, buf, 20)) < 0) {
        printf("读取失败!\n");
        return -1;
    }
    buf[ret] = '\0';
    printf("现在读取的字符串为:%s\n", buf);

    close(fd1);
    return 0;
}


/*
 * 功能:从指定文件中读取指定字节数目的字符
 * 1，验证读取n个字节时是否包含'\0'
 * 2，验证缓存区溢出问题并不一定会造成错误
 */
int
file_uncache_read(const char *filename)
{
    int         fd;
    char        buf[32];
    int         i;

    // 为了验证尾部字符串是否自动填0
    for (i=0; i<32; i++) {
        buf[i] = (char)('a' + i);
    }

    if (access(filename, F_OK) == -1) {
        printf("文件不存在!\n");
        return -1;
    }

    printf("从文件%s中读取8个字节到缓存中，是否自动加串尾？\n", filename);
    fd = open(filename, O_RDONLY);
    if (fd < 0) {
        printf("打开文件失败！\n");
        return -1;
    }

    if (read(fd, buf, 8) != 8) {
        printf("读取8个字节失败！\n");
        return -1;
    }

    printf("判断读取数据后的缓存的最后一个字节内容，正确就输出:\n");
    if (buf[8] == '\0') {
        printf("不正确----不应该有串结束符的！！\n"
                "读取的值为:%s, 长度为:%lu\n", buf, strlen(buf));
    } else {
        buf[8] = '\0';
        printf("正确的结果----现在开始添加串结束符，结果为:%s", buf);
    }

    return 0;
}

/*
 * 功能:使用open创建文件并写入指定数目的字节
 * 1，打开一个文件并重头开始写入之后，后面的所有字节不会清空
 */
int
file_uncache_write(const char *filename)
{
    int         fd;
    char        buf[10] = "123456789\n";

    if (access(filename, F_OK) == -1) {
        fd = open(filename, O_RDWR|O_CREAT|O_TRUNC, 0666);
    } else {
        fd = open(filename, O_WRONLY);
    }
    if (fd < 0) {
        printf("文件创建或者打开失败！\n");
        return -1;
    }

    // 清空文件内容
    if (ftruncate(fd, 0) == -1) {
        printf("清空文件失败!\n");
    }
    lseek(fd, 0, SEEK_SET);
    
    // 写入
    if (write(fd, buf, 10) != 10) {
        printf("写入文件失败!\n");
    }
    printf("写入文件成功！\n");

    close(fd);
    return 0;
}

/*
 * 功能:测试dup函数的使用，没有使用文件锁保证不互斥
 * 实现：拷贝一个读写权限的fd，之后利用第二个文件描述符
 *      进行文件的输入，最后利用第一个文件描述符实现输出
 *  1,newfd = dup(oldfd);
 *  2,newfd = dup(oldfd, targetfd);
 */
int
file_uncache_dup(const char *filename)
{
   // int         fd1, fd2;

    return 0;
}

/*
 * 功能：利用fsync实现输入缓冲区的清除
 */
int
file_uncache_sync()
{
    char        c;

    do {
        printf("读取字符，请输入一个字符串:");
        scanf("%c", &c);
        if (c == 'q') {
            break;
        }
        printf("读取的字符为:%c\n", c);
        printf("使用fsync实现能否清除输入缓冲区!\n");
        fflush(stdin);
        fsync(0);
    }while(1);

    return 0;
}

/*
 * 功能:F_GETFD, F_SETTF
 */
int
file_uncache_fcntl_fd(const char *firstname, const char *secondname)
{
    int         fd1, fd2;
    int         flags;
    char        fdstr[10];
    const char* buf = "--父进程写入的信息--\n";
    pid_t       pid;
    
    fd1 = open(firstname, O_RDWR|O_CREAT|O_TRUNC);
    if (fd1 < 0) {
        printf("打开文件%s失败。\n", firstname);
        return -1;
    }
    fd2 = open(secondname, O_RDWR|O_CREAT|O_TRUNC);
    if (fd2 < 0) {
        printf("打开文件%s失败。\n", secondname);
        return -1;
    }
    printf("打开文件:\n"
            "\t%s\n"
            "\t%s\n", firstname, secondname);
    printf("\t设置%s描述符close_on_exec标志位为1。\n", firstname);
    // set close_on_exec flag
    flags = fcntl(fd1, F_GETFD);
    flags |= FD_CLOEXEC;            // 一般都使用1代替FD_CLOEXEC
    fcntl(fd1, F_SETFD, flags);
    // fork   
    if ((pid = fork()) == 0) {
        sprintf(fdstr, "%d", fd1);
        execl("./testfcntl", "testfcntl", fdstr, NULL);
        close(fd1);
        exit(0);
    } else {
        wait(NULL);
        printf("父进程：pid=%d-写入文件%s\n", pid, buf);
        write(fd1, buf, strlen(buf));
    }
    // fork   
    if ((pid = fork()) == 0) {
        sprintf(fdstr, "%d", fd2);
        execl("./testfcntl", "testfcntl", fdstr, NULL);
        close(fd2);
        exit(0);
    } else {
        wait(NULL);
        printf("父进程：pid=%d-写入文件%s\n", pid, buf);
        write(fd2, buf, strlen(buf));
    }

    close(fd1);
    close(fd2);
    return 0;
}

/*
 * 功能:打印文件标志
 * 1，0,1,2都是可以读写的，但是可以利用重定向来改变，可以设置fd为0进行测试
 */
int
file_uncache_fcntl_fl_display(int fd)
{
    int         val;

    if ((val = fcntl(fd, F_GETFL, 0)) < 0) {
        printf("获取文件状态标志失败！\n");
        return -1;
    }

    // 前三个特殊标志
    switch (val & O_ACCMODE) {
        case O_RDONLY:
            printf("\t+++[文件只读]\n");
            break;
        case O_WRONLY:
            printf("\t+++[文件只写]\n");
            break;
        case O_RDWR:
            printf("\t+++[文件可读可写]\n");
            break;
        default:
            printf("错误的文件访问标志位，返回！\n");
            return -1;
    }

    if (val & O_APPEND) {
        printf("\t+++[文件可追加]\n");
    }
    if (val & O_NONBLOCK) {
        printf("\t+++[文件非阻塞]\n");
    }
#if defined(O_SYNC)
    if (val & O_SYNC) {
        printf("\t+++[文件同步写]\n");
    }
#endif

    printf("\n");
    return 0;
}

/*
 * 功能:测试FL的选项
 * 1，F_GETFL以及F_SETFL仅仅是对open函数的补充以及数据提取
 * 2，open函数中O_RDWR,O_RDONLY,O_WRONLY三者必须且只能有一个
 */
int 
file_uncache_fcntl_fl(const char *filename)
{
    int         fd;
    int         ret;

    printf("标准输入的文件标志：\n");
    ret = file_uncache_fcntl_fl_display(0);
    if (ret < 0) {
        return ret;
    }
    printf("标准输出的文件标志：\n");
    ret = file_uncache_fcntl_fl_display(1);
    if (ret < 0) {
        return ret;
    }
    printf("标准错误的文件标志：\n");
    ret = file_uncache_fcntl_fl_display(2);
    if (ret < 0) {
        return ret;
    }

    fd = open(filename, O_RDWR|O_APPEND|O_SYNC);
    if (fd < 0) {
        printf("打开文件%s失败!\n", filename);
        return -1;
    }

    printf("1--获取并打印当前打开文件的文件标志:\n");
    ret = file_uncache_fcntl_fl_display(fd);
    if (ret < 0) {
        goto end;
    }

    printf("2--清除文件中的《追加》标志位并打印文件标志:\n");
    if ((ret = fcntl(fd, F_GETFL, 0)) < 0) {
        printf("获取文件标志失败！\n");
        goto end;
    }
    ret &= ~O_APPEND;
    if ((ret = fcntl(fd, F_SETFL, ret)) < 0) {
        printf("设置文件标志失败！\n");
        goto end;
    }
    ret = file_uncache_fcntl_fl_display(fd);
    if (ret < 0) {
        goto end;
    }

end:
    close(fd);
    return ret;
}

/*
 * 功能：fcntl函数的部分测试
 * 1，测试dup函数功能
 * 2，测试F_GETFD和F_SETFD的用途
 * 3，测试F_GETFL和F_SETFL的功能
 */
int
file_uncache_fcntl(const char *filename)
{
    int         ret;

    // 测试F_SETFD文件描述符标志的功能
    printf("\t\t+++++++++++fcntl-fd+++++++++++++\n");
    ret = file_uncache_fcntl_fd(FILENAME_FCNTL, FILENAME_FCNTL2);    
    if (ret < 0) {
        return ret;
    }
    file_display(FILENAME_FCNTL);
    file_display(FILENAME_FCNTL2);

    // 测试F_SETFL文件表标志的功能
    printf("\t\t+++++++++++fcntl-fl+++++++++++++\n");
    ret = file_uncache_fcntl_fl(FILENAME_FCNTL);
    if (ret < 0) {
        return ret;
    }

    return 0;
}

/*
 * 功能:测试link和unlink函数
 * 1,硬链接;
 * 2,软连接；
 * 实现：先连接一个文件并打印该文件的stat结构体信息
 */
int 
file_uncache_link(const char *filename)
{
    int             ret;
    struct stat     buf;
    struct stat     oldbuf;

    printf("\t\t\t硬链接测试***\n");
    while ((ret = link(filename, FILENAME_UNCACHE_LINK) < 0)) {
        if (access(FILENAME_UNCACHE_LINK, F_OK) == -1) {
            printf("创建文件链接失败！\n");
            return ret;
        }
        /* 删除已经存在的文件或者目录 */
        if (remove(FILENAME_UNCACHE_LINK) == -1) {
            printf("删除文件%s失败！\n", FILENAME_UNCACHE_LINK);
            return -1;
        }
        printf("文件已经存在，删除旧有的文件！\n");
    }
    
    if ((ret = lstat(FILENAME_UNCACHE_LINK, &buf)) < 0) {
        printf("获取文件%s状态信息失败!\n", FILENAME_UNCACHE_LINK);
        return ret;
    }
    if ((ret = lstat(FILENAME_UNCACHE_LINK, &oldbuf)) < 0) {
        printf("获取文件%s状态信息失败!\n", FILENAME_UNCACHE);
        return ret;
    }

    printf("旧有的文件信息如下:\n"
            "\t节点号:\t%lu\n"
            "\tUID   :\t%u\n"
            "\tGID   :\t%u\n"
            "\tlink_count:\t%u\n"
            "\t文件大小:\t%ld\n",
            oldbuf.st_ino, oldbuf.st_uid, 
            oldbuf.st_gid, (unsigned)oldbuf.st_nlink, oldbuf.st_size);
    printf("新的链接文件信息如下:\n"
            "\t节点号:\t%lu\n"
            "\tUID   :\t%u\n"
            "\tGID   :\t%u\n"
            "\tlink_count:\t%u\n"
            "\t文件大小:\t%ld\n",
            buf.st_ino, buf.st_uid, 
            buf.st_gid, (unsigned)buf.st_nlink, buf.st_size);

    printf("删除硬链接-unlink：\n");
    if (unlink(FILENAME_UNCACHE_LINK) == -1) {
        printf("解除硬链接失败!\n");
        return -1;
    }
    printf("旧有（删除硬链接之后）的文件信息如下:\n"
            "\t节点号:\t%lu\n"
            "\tUID   :\t%u\n"
            "\tGID   :\t%u\n"
            "\tlink_count:\t%u\n"
            "\t文件大小:\t%ld\n",
            oldbuf.st_ino, oldbuf.st_uid, 
            oldbuf.st_gid, (unsigned)oldbuf.st_nlink, oldbuf.st_size);

    printf("\n\t\t\t软链接测试***\n");
    if ((ret = symlink(filename, FILENAME_UNCACHE_LINK)) == -1) {
        printf("创建软连接%s失败!\n", FILENAME_UNCACHE_LINK);
        return ret;
    }
    memset(&buf, 0, sizeof(struct stat));
    if (lstat(FILENAME_UNCACHE, &buf) < 0) {
        printf("获取软连接文件%s状态信息失败!\n", FILENAME_UNCACHE);
        return -1;
    }
    printf("新的软链接文件信息如下:\n"
            "\t节点号:\t%lu\n"
            "\tUID   :\t%u\n"
            "\tGID   :\t%u\n"
            "\tlink_count:\t%u\n"
            "\t文件大小:\t%ld\n",
            buf.st_ino, buf.st_uid, 
            buf.st_gid, (unsigned)buf.st_nlink, buf.st_size);
    printf("旧有的文件信息如下:\n"
            "\t节点号:\t%lu\n"
            "\tUID   :\t%u\n"
            "\tGID   :\t%u\n"
            "\tlink_count:\t%u\n"
            "\t文件大小:\t%ld\n",
            oldbuf.st_ino, oldbuf.st_uid, 
            oldbuf.st_gid, (unsigned)oldbuf.st_nlink, oldbuf.st_size);
    if (unlink(FILENAME_UNCACHE_LINK) == -1) {
        printf("删除链接%s失败！\n", FILENAME_UNCACHE_LINK);
        return -1;
    }

    return 0;
}


int main(int argc, char **argv)
{
    int         ret = -1;

    printf("======================Judge=======================\n");
    ret = file_uncache_open_multi(FILENAME_UNCACHE_PROC);
    printf("======================WRITE=======================\n");
    ret = file_uncache_write(FILENAME_UNCACHE);
    printf("\n======================READ=======================\n");
    ret = file_uncache_read(FILENAME_UNCACHE);
    printf("\n======================sync=======================\n");
    ret = file_uncache_sync();
    printf("\n======================fcntl=======================\n");
    ret = file_uncache_fcntl(FILENAME_UNCACHE);
    printf("\n======================link/unlink=================\n");
    ret = file_uncache_link(FILENAME_UNCACHE);

    printf("\n");
    return ret;
}
