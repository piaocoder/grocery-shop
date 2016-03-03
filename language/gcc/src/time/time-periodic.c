/*
 * 功能:测试周期间隔发送的测试用例
 *      get_periodic_of_month--每月固定的号数发送响应的信息
 *      get_periodic_of_week --每周固定的星期发送响应信息
 */
#include "time-config.h"

#define MONTH_SIZE                  31
#define WEEK_SIZE                   7
#define DAY_SIZE                    1
#define YEAR_SIZE                   12

time_t
get_periodic_of_month(unsigned int bits, time_t attime)
{
    unsigned int            shiftPos = 0;
    unsigned int            maxDay = 0;
    struct tm               *tmAttime = NULL;
    struct tm               tmTemp;
    time_t                  nowtime = 0;
    time_t                  scheduletime;

    maxDay = get_max_days();
    if (maxDay == 0) { 
        return 0; 
    }
   
    nowtime = time(NULL);
    memcpy(&tmTemp, localtime(&nowtime), sizeof(struct tm));
    shiftPos = (0x1<<(tmTemp.tm_mday-1));
    // attime
    tmAttime = localtime(&attime);
    tmTemp.tm_hour = tmAttime->tm_hour;
    tmTemp.tm_min = tmAttime->tm_min;
    tmTemp.tm_sec = tmAttime->tm_sec;
    // current time         
    nowtime = time(NULL);   
    
    do {
        if (bits&shiftPos) {
            scheduletime = mktime(&tmTemp);
            if (scheduletime > nowtime) {
                return scheduletime;
            }
        }
    
        if (tmTemp.tm_mday == maxDay) {  
            shiftPos = 1;
            tmTemp.tm_mday = 1;
            tmTemp.tm_year += (tmTemp.tm_mon+1)/12;
            tmTemp.tm_mon = (tmTemp.tm_mon+1)%12;
        } else {
            shiftPos = shiftPos<<1;
            tmTemp.tm_mday++;
        }
    } while (TRUE);

    return 0;
}

time_t
get_periodic_of_week(unsigned int bits, time_t attime)
{
    unsigned int            shiftPos = 0;
    unsigned int            maxDay;
    struct tm               *tmAttime = NULL;
    struct tm               tmTemp;
    time_t                  nowtime = 0;
    time_t                  scheduletime;

    maxDay = get_max_days();
    if (maxDay == 0) {
        return 0;
    }
    nowtime = time(NULL);
    memcpy(&tmTemp, localtime(&nowtime), sizeof(struct tm));
    shiftPos = (0x1<<(tmTemp.tm_wday-1));
    // attime
    tmAttime = localtime(&attime);
    tmTemp.tm_hour = tmAttime->tm_hour;
    tmTemp.tm_min = tmAttime->tm_min;
    tmTemp.tm_sec = tmAttime->tm_sec;
    // current time
    nowtime = time(NULL);

    do {
        if (bits&shiftPos) {
            scheduletime = mktime(&tmTemp);
            if (scheduletime>nowtime) {
                return scheduletime;
            }
        }

        if (tmTemp.tm_wday == WEEK_SIZE-1) {
            shiftPos = 1;
            tmTemp.tm_wday = 0;
        } else {
            shiftPos = shiftPos<<1;
            tmTemp.tm_wday++;
        }

        // Increment day
        if (tmTemp.tm_mday == maxDay) {
            tmTemp.tm_mday = 1;
            tmTemp.tm_year += (tmTemp.tm_mon+1)/YEAR_SIZE;
            tmTemp.tm_mon = (tmTemp.tm_mon+1)%YEAR_SIZE;
        } else {
            tmTemp.tm_mday++;
        }
    } while (TRUE);

    return 0;
}

#define MONTH_TEST          1121576 //(4,6,9,11,12,13,17,21)
#define WEEK_TEST           86 //2,3,5,7

int 
main(int argc, char **argv)
{
    char        buf[128] = {0};
    char        timeStr[128] = {0};
    //time_t      timeT;
    time_t      now;
    struct tm   *tmTime;

    now = time(NULL);
    tmTime = localtime(&now); 
    do {
        printf("请输入欲测试的功能(month或者week):\n");
        scanf("%s", buf);
        if (!strcmp(buf, "quit")) {
            break; 
        } else {
            printf("当前日期:%s.当前星期%d.\n", asctime(tmTime), tmTime->tm_wday);
            printf("请输入你要测试的时间(HH:MM:SS):\n");
            scanf("%s", timeStr);
            if (!strcmp(buf, "month")) {
            } else if (!strcmp(buf, "week")) {
            }
        }
    } while (1);
    
    return 0;
}
