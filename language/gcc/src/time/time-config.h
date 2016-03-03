#ifndef _CONFIGTIME_H_
#define _CONFIGTIME_H_
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <time.h>

#define TRUE                1
#define FALSE               0

#define MONTH_YEAR_SIZE     12
#define DAY_WEEK_SIZE       7
#define DAY_YEAR_SIZE       365
#define DAY_MONTH_SIZE      30

#define SECOND_DAY_SIZE     86400
#define SECOND_HOUR_SIZE    3600
#define SECOND_MIN_SIZE     60
#define SECOND_SIZE         1

/*
 * func:get max day of specific month
 */
int get_max_days(void);

/*
 * func:converset YYYY-MM-DD HH:MM:SS to time_t
 */
int time_specific_set(struct tm *dst, char *time);

/*
 * func:add months base on current time
 */
int time_arithmetic_month_handle(struct tm *timeT, int months);

/*
 * func:arithmetic handle of current time.
 */
int time_arithmetic_opt(struct tm *timeTm, char item, int num);

/*
 * func:operation of localtime
 */
int time_local_show(void);

/*
 * function:clear stdin
 */
void clear_iobuff(void);

#endif
