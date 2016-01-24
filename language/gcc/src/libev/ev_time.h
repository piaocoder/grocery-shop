#ifndef _EV_TIME_H_
#define _EV_TIME_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <ev.h>

#define True                    1
#define False                   0

#define SECOND_HOUR             3600
#define SECOND_MINUTE           60
#define SECOND_DAY              24*SECOND_HOUR
#define MONTH_SIZE              31
#define WEEK_SIZE               7
#define DAY_SIZE                1

enum {
    DIFF_TIME_FLAG_DAY = 0,
    DIFF_TIME_FLAG_WEEK,
    DIFF_TIME_FLAG_MONTH,
};
#define DAY 1

/*
 * argv:date_f--1,2,31
 * attime:
 * flags:month, week, day
 */
double get_interval_by_time(unsigned int date_f, time_t attime, int flags);

/*
 * func:converse string to time
 */
int string_to_attime(char *str, time_t *time);

/*
 * func:copy
 */
void copy_time_tm(struct tm *dst, struct tm *src);

#endif
