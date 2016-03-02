#ifndef _FILECONFIG_H_
#define _FILECONFIG_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <errno.h>
#include <libgen.h>
#include <dirent.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

#define FILENAME_RW             "./filedir/fileTestRw"
#define FILENAME_BINARY_RW      "./filedir/fileTestBinary"
#define FILENAME_UNCACHE        "./filedir/fileTestUncache"
#define FILENAME_UNCACHE_LINK   "./filedir/fileTestUncache.link"
#define FILENAME_UNCACHE_PROC   "./filedir/fileTestUncache.proc"
#define FILENAME_FCNTL          "./filedir/uncacheTest.fcntl"
#define FILENAME_FCNTL2         "./filedir/uncacheTest.fcntl2"

typedef struct fileObjectUnit fileObjectUnit;


/* 写入文件的基本单元 */
struct fileObjectUnit{
    int         id;
    char        desc[128];
};

int file_clear(const char *filename);

int file_display(const char *filename);

#endif
