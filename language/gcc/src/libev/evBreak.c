#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <ev.h>

pthread_t      test_thread;
struct ev_loop *loop;
ev_timer       timer_watcher;

void *
thread_impl(void *arg)
{
    sleep(10);
    printf("线程准关闭所有的EV_Timer:\n");
    ev_break(loop, EVBREAK_ALL);
    exit(0);
}

void
timer_callback(struct ev_loop *loop, ev_timer *w, int revents)
{
    while (1) {
        sleep(1);
        printf("TIMER ......\n");
    }
}

int 
main(int argc, char **argv)
{
    /*
     * 1,创建一个定时器，设定定时时间以及回调函数；
     * 2，新建一个线程
     * 3，开始计时
     */
    loop = EV_DEFAULT;
    if (pthread_create(&test_thread, NULL, thread_impl, NULL) != 0) {
        printf("创建线程失败!\n");
        return -1;
    }
    ev_timer_init(&timer_watcher, timer_callback, 0.0, 5.0);
    ev_timer_start(loop, &timer_watcher);
    ev_run(loop, 0);

    printf("结束!\n");

    return 0;
}
