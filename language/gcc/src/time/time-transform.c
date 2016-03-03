#include "time-config.h"

/*
 * 功能：
 *  1，读取键盘输入的时间字符串；
 *  2，比较strptime以及自定义函数的关联性以及正确性,
 *      其中比较的方式:字符串输出,time_t值；
 */
int 
time_transform(void) 
{    
    char            timeStr[128] = {0};
    char            *current = NULL;
    char            item;
    struct tm       tmCurrent;
    time_t          now;
    time_t          timeT;
    int             num; 

    time(&now);
    do {
        memset(&tmCurrent, 0, sizeof(struct tm));
        current = ctime(&now);
        printf("Please input a time, now time is: %s", current);
        scanf("%s", timeStr);
        clear_iobuff();
        //贪婪匹配不懂setbuf(stdin, NULL);//linux--fflush(stdin);//window

        strptime(timeStr, "%Y-%m-%d-%H:%M:%S", &tmCurrent);
        printf("Now, let me look at time of strptime:%s\n",asctime(&tmCurrent));
        printf("year=%d month=%d day=%d hour=%d min=%d second=%d\n"
                "week=%d yday=%d daylight=%d\n\n",
                tmCurrent.tm_year, tmCurrent.tm_mon, tmCurrent.tm_mday,
                tmCurrent.tm_hour, tmCurrent.tm_min, tmCurrent.tm_sec,
                tmCurrent.tm_wday, tmCurrent.tm_yday, tmCurrent.tm_isdst);

        printf("Input what you want to perform arithmetic operations and number:\n");
        scanf("%c %d", &item, &num);
        clear_iobuff();
        if (time_arithmetic_opt(&tmCurrent, item, num) < 0) {
            return -1;
        }
        timeT = mktime(&tmCurrent); 
        printf("Show time after arithmetic:%s\n",ctime(&timeT));
        printf("year=%d month=%d day=%d hour=%d min=%d second=%d\n"
                "week=%d yday=%d daylight=%d\n\n",
                tmCurrent.tm_year, tmCurrent.tm_mon, tmCurrent.tm_mday,
                tmCurrent.tm_hour, tmCurrent.tm_min, tmCurrent.tm_sec,
                tmCurrent.tm_wday, tmCurrent.tm_yday, tmCurrent.tm_isdst);

        do {
            printf("Are you continue this game?(Y/N)");
            scanf("%c", &item);
            clear_iobuff();
            if ( ((item=toupper(item)) == 'N') || item=='Y' ) {
                break;
            }
        } while(TRUE);

        if (item == 'N') {
            break;
        }
    } while(TRUE);

    return 0;
}

/*
 * 1,如果maxsize的长度不能包括一个格式，则仅仅截取部分长度：
 * 例如长度为11,格式为:%d/%b/%Y，则仅仅截取%d/%b部分
 * 2,maxsize=strlen(str) + 1
 */
int
format_time(void)
{
    struct tm       tm;
    time_t          now;
    char            buf[255];

    buf[15] = '\0';
    time(&now);
    tm = *localtime(&now);
    strftime(buf, 13, "%d/%b/:%Y::%H:%M:%S", &tm);
    printf("Buf=%s\n", buf);

    return 0;
}

/*
 * 功能：增加时间并打印出来
 */
int
format_time_add(void)
{
    struct tm       tm;
    time_t          now;
    char            buff[128];

    time(&now);
    now += 60 * 60 * 24 * 3650;
    tm = *gmtime(&now);

    printf("Add time:%s", ctime(&now));
    // Sun, 09-Oct-2016 11:16:02 GMT

    strftime(buff, 128, "%a,%d-%b-%Y %T GMT", &tm);
    printf("Add time:%s\n", buff);

    return 0;
}

int 
main(int argc, char **argv)
{
    //time_transform();
    format_time();
    format_time_add();
    return 0;
}
