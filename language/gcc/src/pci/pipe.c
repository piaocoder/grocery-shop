#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <ev.h>


static void 
ev_io_cb(struct ev_loop *loop, ev_io *w, int revents)
{
    sleep(1);
    printf("+++++++++++++++++++++++++\n");
    printf("Children:detect father process is closing.\n");
    printf("+++++++++++++++++++++++++\n");
    sleep(3);
    //exit(0);
}

void 
children(int fd[])
{
    struct ev_loop *loop = ev_default_loop(0);
    static ev_io       fd_read;

    close(fd[1]);

    ev_io_init(&fd_read, ev_io_cb, fd[0], EV_READ);
    ev_io_start(loop, &fd_read);
    ev_run(loop, 0);
}

int 
pipeCommunicate(int fd[])
{
    pid_t           pid;

    pipe(fd);

    if ((pid = fork()) < 0) {
        printf("Fork children failure!\n");
        return -1;
    } else if (pid == 0) {
        children(fd);
        exit(0);
    } else {
        close(fd[0]);           //close read point
        while(1) {
            sleep(3);
        }
        printf("Parent prcocess is closing!!\n");
    }

    return 0;
}

int 
main(int argc, char **argv)
{
    int     pipeFd[2];

    pipeCommunicate(pipeFd);

    return 0;
}
