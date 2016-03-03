#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sched.h>
#include <getopt.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <asm/unistd.h>
#include <unistd.h>
#include <linux/unistd.h>
#include <sys/klog.h>
#include <syslog.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/prctl.h>
#include <fcntl.h>
#include <ctype.h>
#include <errno.h>

#define DAEMON_PID_FILE     "/var/run/daemon.pid"
#define True    1
#define False   0

static int pidArray[3] = {0};

static void
sig_daem_usr_handle(int signal)
{
    printf("Receive a signal from other process!\n");
}

static void 
sig_daem_stop_handle(int signal)
{
    int         i = -1;
    int         ret = -1;

    printf("Preparing to exit the process.\n");
    for (i=0; i<3; i++) {
        ret = kill(pidArray[i], SIGTERM);
        printf("ret = %d -=0=0=0=0=0=0\n", ret);
    }
    exit(0);
}

static void
sig_first_stop_handle(int signal)
{
    sleep(15);
    printf("%s\n", __func__);
}

static void
sig_second_stop_handle(int signal)
{
    sleep(15);
    printf("second process quit!\n");
}

static void
sig_third_stop_handle(int signal)
{
    sleep(15);
    printf("third process quit!\n");
}

static int
firstProcess(void)
{
    // listen SIGTERM signal
    signal(SIGTERM, sig_first_stop_handle);

    while (True) {
        sleep(10);
        printf("first process running!\n");
    }

    return 0;
}

static int
secondProcess(void)
{
    // listen SIGTERM signal
    signal(SIGTERM, sig_second_stop_handle);

    while (True) {
        sleep(15);
        printf("second process running!\n");
    }

    return 0;
}

static int
thirdProcess(void)
{
    // listen SIGTERM signal
    signal(SIGTERM, sig_third_stop_handle);

    while (True) {
        sleep(5);
        printf("third process running!\n");
    }

    return 0;
}


static void
kill_fork_child(int num)
{
    pid_t   pid = 0;
    int     ret = -1;
    int     i = 0;
    
    for (i=0; i<num; i++) {
        if ((pid=fork()) < 0) {
            return;
        } else if (pid == 0) {
            if (i == 0) {
                ret = firstProcess();
            } else if (i == 0) {
                ret = secondProcess();
            } else {
                ret = thirdProcess();
            }
            exit(0);
        } else {
            pidArray[i] = pid;
            printf("进程%d创建成功！\n", pid);
        }
    }
}

int 
main(int argc, char *argv[])
{
    int                 lock_fd = -1;
    struct flock        lock;
    char                str[64];
    pid_t               pid;
    int                 mode = 1;

    // file lock
    lock_fd = open(DAEMON_PID_FILE, O_CREAT | O_RDWR, 0666);
    if (lock_fd == -1) {
        printf("Can't open lock file '%s' , error : '%s'\n", DAEMON_PID_FILE, strerror(errno));
        return -1;
    }

    // run background, 0 stdin/stdou/stdout--->/dev/null
    //if (daemon(1, 1) < 0) {
    //    printf("switch to backgroud failed.\n");
    //    return -1;
    //}

    lock.l_whence = SEEK_SET;
    lock.l_type = F_WRLCK;
    lock.l_start = 0;
    lock.l_len = 0;
    lock.l_pid = 0;

    if (argc == 1 || (argc == 2 && (strcmp(argv[1], "start") == 0))) {
        printf("\n(~_~)Readying start wafalarmd......\n");
        mode = 1;
    } else if (argc == 2 && (strcmp(argv[1], "stop") == 0)) {
        mode = 2;
        printf("\n(>_<)Readying stop wafalarmd......\n");
    } else {
        printf("\n(v_v)unknown option, usage: wafalarmd [start|stop|reload]\n");
        close(lock_fd);
        return -1;
    }

    if (mode == 1) {
        if (fcntl(lock_fd, F_SETLK, &lock) < 0 ) {
            printf("\n(v_v)Other wafalarmd process is running!\n");
            close(lock_fd);
            return 0;
        }
    }

    if (mode == 2) {
        if (read(lock_fd, str, 64) < 0) {
            close(lock_fd);
            return -1;
        }

        pid = atol(str);
        kill(pid, SIGTERM);
        return 0;
    }

    // write a new pid to lock file.
    snprintf(str, 63, "%lu", (unsigned long)getpid());
    str[63] = '\0';
    printf("Current pid is :%s\n", str);
    ftruncate(lock_fd, 0);
    if (write(lock_fd, str, strlen(str)) != strlen(str)) {
        printf("Can't write lock file, error : '%s'\n", strerror(errno));
        return -1;
    }

    signal(SIGUSR1, sig_daem_usr_handle);
    signal(SIGTERM, sig_daem_stop_handle);
    // fork child proc.
    kill_fork_child(3);
    // loop and test inp is dead. 
    while (True) {
        sleep(10);
    }//while

    return 0;
}

