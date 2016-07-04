/*************************************************************************\
*                  Copyright (C) Michael Kerrisk, 2015.                   *
*                                                                         *
* This program is free software. You may use, modify, and redistribute it *
* under the terms of the GNU General Public License as published by the   *
* Free Software Foundation, either version 3 or (at your option) any      *
* later version. This program is distributed without any warranty.  See   *
* the file COPYING.gpl-v3 for details.                                    *
* 影响的顺序：
*       当前目录中的所有操作会被记录；
*       当前目录下的子目录中的操作，因为涉及到子目录的访问权限的，会记录；
*       当前目录下的子目录中的孙目录的操作不会被记录，与当前目录无任何关系
\*************************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <unistd.h>
#include <sys/inotify.h>
#include <limits.h>


#define PARENT_EVENTS (IN_DELETE | IN_CREATE | \
        IN_MOVED_FROM | IN_MOVED_TO | \
        IN_DELETE_SELF | IN_MOVE_SELF)
#define CHILD_EVENTS (IN_CREATE | IN_MOVED_TO)


void error_exit(const char *cmd,...)
{
    va_list     args;
    va_start(args, cmd);
    vprintf(cmd, args);
    va_end(args);
    
    exit(1);
}


unsigned int cookieBackup;


static void             /* Display information from inotify_event structure */
displayInotifyEvent(struct inotify_event *i)
{
    printf("    wd =%2d; ", i->wd);
    if (i->cookie > 0) {
        printf("cookie =%4d; ", i->cookie);
    }

    /*if (i->mask & IN_ISDIR) {*/
    /*}*/

    printf("mask = ");
    if (i->mask & IN_ACCESS)        printf("IN_ACCESS ");
    if (i->mask & IN_ATTRIB)        printf("IN_ATTRIB ");
    if (i->mask & IN_CLOSE_NOWRITE) printf("IN_CLOSE_NOWRITE ");
    if (i->mask & IN_CLOSE_WRITE)   printf("IN_CLOSE_WRITE ");
    if (i->mask & IN_CREATE)        printf("IN_CREATE ");
    if (i->mask & IN_DELETE)        printf("IN_DELETE ");
    if (i->mask & IN_DELETE_SELF)   printf("IN_DELETE_SELF ");
    if (i->mask & IN_IGNORED)       printf("IN_IGNORED ");
    if (i->mask & IN_ISDIR)         printf("IN_ISDIR ");
    if (i->mask & IN_MODIFY)        printf("IN_MODIFY ");
    if (i->mask & IN_MOVE_SELF)     printf("IN_MOVE_SELF ");
    if (i->mask & IN_MOVED_FROM) {
        printf("IN_MOVED_FROM ");
        cookieBackup = i->cookie;
    }
    if (i->mask & IN_MOVED_TO) {
        printf("IN_MOVED_TO ");
        if (i->cookie == cookieBackup) {
            printf("--(发生重命名事件)--");
        }
    }
    if (i->mask & IN_OPEN)          printf("IN_OPEN ");
    if (i->mask & IN_Q_OVERFLOW)    printf("IN_Q_OVERFLOW ");
    if (i->mask & IN_UNMOUNT)       printf("IN_UNMOUNT ");
    printf("\n");

    if (i->len > 0) {
        printf("        涉及的文件名name = %s\n", i->name);
    }
}

#define BUF_LEN (10 * (sizeof(struct inotify_event) + NAME_MAX + 1))

int
main(int argc, char *argv[])
{
    int inotifyFd, childFd, maxFd, wd, j, rst;
    fd_set      fds;
    struct timeval timeout;
    (void)j;
    char buf[BUF_LEN] __attribute__ ((aligned(8)));
    ssize_t numRead;
    char *p;
    struct inotify_event *event;

    if (argc < 3 || strcmp(argv[1], "--help") == 0)
        error_exit("%s pathname childname\n", argv[0]);

    inotifyFd = inotify_init();                 /* Create inotify instance */
    if (inotifyFd == -1)
        error_exit("inotify_init");

    childFd = inotify_init();
    if (childFd == -1)
        error_exit("inotify_init");
    maxFd = inotifyFd > childFd ? inotifyFd : childFd;
    printf("Parent:%d, childFd:%d, maxFd:%d\n", 
            inotifyFd, childFd, maxFd);

    /*for (j = 1; j < argc; j++) {*/
        /*wd = inotify_add_watch(inotifyFd, argv[j], IN_ALL_EVENTS);*/
        /*if (wd == -1)*/
            /*error_exit("inotify_add_watch");*/

        /*printf("Watching %s using wd %d\n", argv[j], wd);*/
    /*}*/
    wd = inotify_add_watch(inotifyFd, argv[1], PARENT_EVENTS);
    if (wd == -1) {                             /* parent inotify */
        error_exit("Parent directory(inotify_add_watch) failed");
    }
    wd = inotify_add_watch(childFd, argv[2], CHILD_EVENTS);
    if (wd == -1) {                             /* children inotify */
        error_exit("Children directory(inotify_add_watch) failed");
    }

    for (;;) {                                  /* Read events forever */
        FD_ZERO(&fds);               
        FD_SET(inotifyFd, &fds);        
        FD_SET(childFd, &fds);        
        timeout.tv_sec = 2; 
        timeout.tv_usec = 0;

        rst = select(maxFd+1, &fds, NULL, NULL, &timeout);
        if (rst <= 0) {
            continue;
        }

        if (FD_ISSET(childFd, &fds)) {
            numRead = read(childFd, buf, BUF_LEN);
            if (numRead == 0)
                error_exit("read() from inotify fd returned 0!");

            if (numRead == -1)
                error_exit("read");
            printf("Read %ld bytes from children inotify fd\n", 
                    (long) numRead);
        } else {
            numRead = read(inotifyFd, buf, BUF_LEN);
            if (numRead == 0)
                error_exit("read() from inotify fd returned 0!");

            if (numRead == -1)
                error_exit("read");
            printf("Read %ld bytes from parent inotify fd\n", 
                    (long) numRead);
        }

        /* Process all of the events in buffer returned by read() */

        for (p = buf; p < buf + numRead; ) {
            event = (struct inotify_event *) p;
            displayInotifyEvent(event);

            p += sizeof(struct inotify_event) + event->len;
        }
    }

    exit(EXIT_SUCCESS);
}
