#include "time-config.h"

int
get_max_days(void)
{   
    struct tm       when;
    time_t          result, now;
    
    time(&now);
    when = *localtime(&now);
    when.tm_mon++;
    when.tm_mday = 0;
    result = mktime(&when);
    if (result == -1) {
        return -1;
    }
    when = *localtime(&result);
    return when.tm_mday;
}

/*
 * 功能:时间串转为struct tm结构体，结果可能不对
 * 具体可以使用strptime，该函数仅仅是为了验证结果的准确性
 */
int 
time_specific_set(struct tm *dst, char *time)
{
    if (!time || !dst) {
        return -1;
    }

    sscanf(time, "%4d-%2d-%2d %2d:%2d:%2d", 
                &dst->tm_year, &dst->tm_mon, &dst->tm_mday,
                &dst->tm_hour, &dst->tm_min, &dst->tm_sec);
    return 0;
}

/*
 * 功能：
 *  1,获取当前时间;
 *  2,解析struct tm结构体
 *  3,进行时间减法;
 */
int
time_local_show(void)
{    
    struct tm       *tmTime = NULL;
    time_t          timeT;
    char            buf[128] = {0};

    if (time(&timeT) < 0) {         // 或者time(NULL)，共享内存
        return -1;
    }

    // 获取当前时间
    strcpy(buf, ctime(&timeT));
    printf("现在时间:%s", buf);

    // 解析struct tm
    tmTime = localtime(&timeT);
    strftime(buf, 128, "%Y-%m-%d %H:%M:%S", tmTime);
    printf("year=%d month=%d day=%d hour=%d minute=%d second=%d\n"
            "week=%d yday=%d daylight=%d\n\n",
            tmTime->tm_year, tmTime->tm_mon, tmTime->tm_mday,
            tmTime->tm_hour, tmTime->tm_min, tmTime->tm_sec,
            tmTime->tm_wday, tmTime->tm_yday, tmTime->tm_isdst);

    timeT -= 3600;
    strcpy(buf, ctime(&timeT));
    printf("修改后的时间:%s", buf);
    tmTime = localtime(&timeT);
    printf("year=%d month=%d day=%d hour=%d minute=%d second=%d\n"
            "week=%d yday=%d daylight=%d\n",
            tmTime->tm_year, tmTime->tm_mon, tmTime->tm_mday,
            tmTime->tm_hour, tmTime->tm_min, tmTime->tm_sec,
            tmTime->tm_wday, tmTime->tm_yday, tmTime->tm_isdst);

    return 0;
}

/*
 * 功能:计算两个不同日期相差的天数
 */
__attribute__((unused))
int
time_arithmetic_day_interval()
{
    return 0;
}

/*
 * 功能:判断是否为闰年
 */
int 
isLeafYear(unsigned int year) {
    return (year % 400 == 0) || ((year % 100 !=0) && (year % 4 == 0));
}

/*
 * 功能：获取指定月份的天数
 */
int
getMaxDayInMonth(int year, int month)
{
    int     days;
    int     daysInMonths[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

    if (month<0 || month>=12) {
        return -1;
    }

    days = daysInMonths[month];
    if (month == 1 && isLeafYear(year)) {
        days += 1;
    }

    return days;
}

/*
 * 功能:增加num*unit之后的时间值
 */
int
time_arithmetic_common_handle(struct tm *timeTm, int num, unsigned int unit)
{
    struct tm   *tmTemp;
    time_t      timeT;

    if (!timeT) {
        return -1;
    }

    timeT = mktime(timeTm);
    timeT += num * unit;
    tmTemp = localtime(&timeT);
    if (!tmTemp) {
        return -1;
    }
    memcpy(timeTm, tmTemp, sizeof(struct tm));

    return 0;
}

/*
 * 功能：增加N个月份之后的时间值
 * 实现:
 *  调用mktime来实现
 */
int
time_arithmetic_month_handle(struct tm *timeT, int months)
{
    int         year;
    int         month;
    int         day;
    int         temp;

    year = timeT->tm_year + months/MONTH_YEAR_SIZE;
    month = timeT->tm_mon + months%MONTH_YEAR_SIZE;
    if (month > MONTH_YEAR_SIZE -1) {
        year += 1;
        month -= MONTH_YEAR_SIZE;
    }

    temp = getMaxDayInMonth(year, month);
    day = timeT->tm_mday>temp ? temp : timeT->tm_mday;

    timeT->tm_year = year;
    timeT->tm_mon = month;
    timeT->tm_mday = day;

    return 0;
}

/*
 * 功能:
 *  1,根据标志位，进行秒、分、时、天数等字段的加减法并返回正确的值
 */
int
time_arithmetic_opt(struct tm *timeTm, char item, int num)
{
    int         ret = 0;

    if (!timeTm) {
        return -1;
    }

    switch (item) {
        case 'y':
            timeTm->tm_year += num;
            break;
        case 'm':
            ret = time_arithmetic_month_handle(timeTm, num);
            break;
        case 'd':
            ret = time_arithmetic_common_handle(timeTm, num, SECOND_DAY_SIZE);
            break;
        case 'H':
            ret = time_arithmetic_common_handle(timeTm, num, SECOND_HOUR_SIZE);
            break;
        case 'M':
            ret = time_arithmetic_common_handle(timeTm, num, SECOND_MIN_SIZE);
            break;
        case 'S':
            ret = time_arithmetic_common_handle(timeTm, num, SECOND_SIZE);
            break;
        default:
            printf("Input character is not legal!\n");
            break;
    }

    return ret;
}

/*
 * function:clear stdin
 */
void
clear_iobuff(void)
{
    int     c;
    while ((c=getchar()) != '\n' && c != EOF);
}
