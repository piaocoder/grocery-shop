/*
 * func:验证同时有多个连续的timer生效，开始回调函数没有结束，
 *      判断，是否会同时运行两个timer_callback。
 * result:
 *      验证的结果为：同一时间，不能同时有两个timer_callback被调用，
 *                  其他的timer会被阻塞
 */
#include "ev-time.h"


ev_timer        first, second, third;
struct ev_loop      *loop = NULL;
static int      time_num = 0;

void
timer_callback(struct ev_loop *loop, ev_timer *w, int revents)
{
    int         i = 0;

    printf("ev_iteration=%d\n", ev_iteration(loop));
    printf("ev_pending_count=%d\n", ev_pending_count(loop));
    if (w == &first) {
        printf("first\n");
    } else if (w == &second) {
        printf("second\n");
    } else {
        printf("third\n");
    }

    while (i++ < 3) {
        printf("%d-----\n", time_num++);
        sleep(1);
    }
    printf("at:%f,repeat:%f\n", w->at, w->repeat);
}


int
simple_test(void)
{
    ev_timer_init(&first, timer_callback, 0.0, 4.0);
    ev_timer_start(loop, &first);
    ev_timer_init(&second, timer_callback, 0.0, 10.0);
    ev_timer_start(loop, &second);

    return 0;
}

int 
time_test(void)
{
    char        timeStr[128] = {0};
    time_t      now;
    time_t      scheduleTime;
    double      diff = 0.0;
    int         ret = -1;

    time(&now);
    printf("Please input a time, now time is: %s", ctime(&now));
    scanf("%s", timeStr);

    ret = string_to_attime(timeStr, &scheduleTime);
    if (ret < 0) {
        return -1;
    }
    diff = get_interval_by_time(1, scheduleTime, DIFF_TIME_FLAG_DAY); 
    printf("diff = %lf\n", diff);
    if (diff > 0) {
        ev_timer_init(&third, timer_callback, diff, diff);
        ev_timer_start(loop, &third);
    }

    return 0;
}

int
main(int argc, char **argv) 
{
    loop = EV_DEFAULT;

    //simple_test();
    time_test();

    ev_run(loop, 0);
    return 0;
}
