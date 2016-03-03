/*
 * 功能:验证ev_periodic
 */
#include "ev-time.h"
#include <pthread.h>

ev_periodic         t1,t2;
pthread_t           thread1;
struct ev_loop      *loop = NULL;

/*
 * 功能:ev_periodic的回调函数
 * 疑问：为何系统时间的更改会有一定的滞后性？
 */
void
periodic_callback(struct ev_loop *loop, ev_periodic *w, int revents)
{
    time_t      now;

    printf("ev_iteration=%d\n", ev_iteration(loop));
    printf("ev_pending_count=%d\n", ev_pending_count(loop));
    printf("offset:%f,interval:%f\n", w->offset, w->interval);
    
    time(&now);
    printf("now timestamp:%lu\n", now);
}

typedef struct TT{
    time_t      t;
    int         a;
}TT;

void *
periodic_thread_cb(void *tTime)
{
    time_t      now;
    TT          *tempTT = (TT*)tTime;

    sleep(2);
    now = tempTT->t - 20;
    if (stime(&now)) {
        printf("Occur error!\n");
        return NULL;
    }
    printf("Change system time to: %s.\n", ctime(&now));
    free(tempTT);
    pthread_exit(NULL);
}

void 
periodic_thread_create(time_t tTime)
{
    // 如果不是动态内存或者全局变量，会出错
    TT      *t = (TT*)malloc(sizeof(TT));

    memset(&thread1, 0, sizeof(pthread_t));
    t->t = tTime;
    if (pthread_create(&thread1, NULL, periodic_thread_cb, t)!=0) {
        printf("Create a new thread failure!\n");
        return;
    }
}

/*
 * 功能:手动输入触发时间
 */
int 
periodic_time_test(void)
{
    char        timeStr[128] = {0};
    time_t      now;
    time_t      scheduleTime;
    struct tm   *tmNow = NULL;
    struct tm   tmSchedule;
    int         ret = -1;

    time(&now);
    printf("Please input a periodic time, now time is: %s", ctime(&now));
    scanf("%s", timeStr);

    ret = string_to_attime(timeStr, &scheduleTime);
    if (ret < 0) {
        printf("occur error!\n");
        return -1;
    }
    tmNow = localtime(&now);
    copy_time_tm(&tmSchedule, tmNow);
    tmSchedule.tm_hour = scheduleTime/3600; 
    tmSchedule.tm_min = (scheduleTime%3600)/60; 
    tmSchedule.tm_sec = (scheduleTime%3600)%60; 
    printf("Configure time is: %s\n", asctime(&tmSchedule));
    scheduleTime = mktime(&tmSchedule);
    
    ev_periodic_init(&t1, periodic_callback, (ev_tstamp)scheduleTime, 0.0, NULL);
    ev_periodic_start(loop, &t1);

    return 0;
}

int 
periodic_interval_time_test(void)
{
    char        timeStr[128] = {0};
    char        timeInter[128] = {0};
    time_t      now;
    time_t      scheduleTime;
    struct tm   *tmNow = NULL;
    struct tm   tmSchedule;
    int         ret = -1;

    time(&now);
    printf("Please input a periodic time, now time is: %s", ctime(&now));
    printf("periodic-time:\n");
    scanf("%s", timeStr);
    printf("interval-time:\n");
    scanf("%s", timeInter);

    ret = string_to_attime(timeStr, &scheduleTime);
    if (ret < 0) {
        return -1;
    }
    tmNow = localtime(&now);
    copy_time_tm(&tmSchedule, tmNow);
    tmSchedule.tm_hour = scheduleTime/3600; 
    tmSchedule.tm_min = (scheduleTime%3600)/60; 
    tmSchedule.tm_sec = (scheduleTime%3600)%60; 
    printf("Configure time is: %s\n", asctime(&tmSchedule));
    scheduleTime = mktime(&tmSchedule);
    
    ev_periodic_init(&t1, periodic_callback, scheduleTime, (double)atoi(timeInter), NULL);
    ev_periodic_start(loop, &t1);

    return 0;
}


/*
 * 功能:设置触发时间在一个小时之后，之后通过代码修改系统时间
 */
int 
periodic_time_now_test(void)
{
    time_t      now;
    time_t      trigger_time;

    time(&now);
    printf("Time before add: %s\n", ctime(&now));
    trigger_time = now + 3600;
    printf("Time after add 1 hours is: %s\n", ctime(&trigger_time));
    printf("Timestamp of trigger_time time:%lu\n", trigger_time);
    
    // create a new thread
    periodic_thread_create(trigger_time);
    // ev
    ev_periodic_init(&t2, periodic_callback, trigger_time, 0.0, NULL);
    ev_periodic_start(loop, &t2);
    return 0;
}

int
main(int argc, char **argv) 
{
    loop = EV_DEFAULT;

    periodic_time_test();
    //periodic_interval_time_test();
    //periodic_time_now_test();

    ev_run(loop, 0);
    return 0;
}
