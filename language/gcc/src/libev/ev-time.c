#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "ev-time.h"

/*
 * func:get max days of current month
 */
static int 
get_maxDay(void) 
{
    struct tm       when;
    time_t          result, now;

    time(&now);
    when = *localtime(&now);
    when.tm_mon ++;
    when.tm_mday = 0;
    result = mktime(&when);
    if (result == -1) {
        return 0;
    }
    when = *localtime(&result);
    return when.tm_mday;
}

void
copy_time_tm(struct tm *dst, struct tm *src)
{
    dst->tm_year  = src->tm_year;
    dst->tm_mon   = src->tm_mon;
    dst->tm_mday  = src->tm_mday;
    dst->tm_hour  = src->tm_hour;
    dst->tm_min   = src->tm_min;
    dst->tm_sec   = src->tm_sec;
    dst->tm_wday  = src->tm_wday;
    dst->tm_yday  = src->tm_yday;
    dst->tm_isdst = src->tm_isdst;
}

/*
 * func:Get interval second between current local time
 *      and the nearest enable attime about days/weeks/none.
 */
double
get_interval_by_time(unsigned int date_f, time_t attime, int flags)
{
    unsigned int            shiftPos = 0;
    unsigned int            dateNum =0,common, maxDay;
    int                     index = 0;
    double                  total = -1.0;
    struct tm               *tmNow = NULL, *tmAttime = NULL;
    struct tm               tmTemp;
    time_t                  nowtime = 0;

    // init
    if ( date_f == 0 ) { 
        return -1; 
    }
    maxDay = get_maxDay();
    if (maxDay == 0) { 
        return -1; 
    }
    nowtime = time(NULL);
    tmNow = localtime(&nowtime);
    copy_time_tm(&tmTemp, tmNow);

    if(flags == DIFF_TIME_FLAG_MONTH){
        dateNum = tmTemp.tm_mday;
        common = MONTH_SIZE;

    }else if(flags == DIFF_TIME_FLAG_WEEK){
        dateNum = tmTemp.tm_wday;
        common = WEEK_SIZE;

    }else{
        dateNum = 1;
        common = DAY_SIZE;
    }
    shiftPos = (0x1<<(dateNum-1));

    // get time total 
    tmAttime = localtime(&attime);
    printf("当前的日期：year=%d month=%d day=%d hour=%d min=%d sec=%d\n", 
            tmTemp.tm_year, tmTemp.tm_mon, tmTemp.tm_mday,
            tmTemp.tm_hour, tmTemp.tm_min, tmTemp.tm_sec);
    printf("配置的日期：year=%d month=%d day=%d hour=%d min=%d sec=%d\n", 
            tmAttime->tm_year, tmAttime->tm_mon, tmAttime->tm_mday,
            tmAttime->tm_hour, tmAttime->tm_min, tmAttime->tm_sec);
    while (True) {
        if (date_f & shiftPos) {
            total = index * SECOND_DAY +
               (tmAttime->tm_hour - tmTemp.tm_hour)*SECOND_HOUR + 
               (tmAttime->tm_min  - tmTemp.tm_min)*SECOND_MINUTE + 
               (tmAttime->tm_sec  - tmTemp.tm_sec) ;
            if (total > 0) { 
#if DD
                printf("%s:total=%lf\n", __func__, total);
#endif
                return total; 
            }
        }

        // 31->1 or 28->1
        if (dateNum == common || dateNum>=maxDay) {    
            shiftPos = 1;
            dateNum = 1;
        } else {
            shiftPos = shiftPos<<1;
            dateNum ++;
        }

        index++;
    }
}


/*
 * func:converse string to time
 */
int string_to_attime(char *str, time_t *time)
{   
    struct tm tm;
        
    if (sscanf(str, "%2d:%2d:%2d", &tm.tm_hour, &tm.tm_min, &tm.tm_sec) != 3) {
        return -1;
    }       
    *time = tm.tm_hour * 3600 + tm.tm_min * 60 + tm.tm_sec;
    //++*time; 
    return 0;   
}           
