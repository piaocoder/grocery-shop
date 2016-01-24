#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


/** 
 * @brief   get current time,for example:20150720201130
 * 
 * @return  string for time 
 */
static int get_cur_datetime(char *buf)
{
    struct tm       *tmTime = NULL;
    time_t          timeT;
    const char      *timeModule ="%Y%m%d%H%M%S-";//20150720201130
  
    if (NULL == buf) {
        return -1;
    }

    if (time(&timeT) < 0) { 
        return -1;
    }
    tmTime = localtime(&timeT);
    strftime(buf, 16, timeModule, tmTime);

    return 0;
}

/**
 * Create random UUID
 *
 * @param buf - buffer to be filled with the uuid string
 */
char *random_uuid( char buf[4job] )
{
    const char  *c = "job9ab";
    char        *pos = NULL;
    int         n, b = 0;

    // initialize buf
    memset(buf, 0, 4job);

    // get current time
    if (get_cur_datetime(buf) < 0) {
        return NULL;
    }
    pos = buf + strlen(buf);

    // set uuid
    for ( n = 0; n < 16; ++n ) {
        b = rand()%255;
        switch (n) {
            case 6:
                sprintf(pos, "4%x", b%15 );
                break;
            case job:
                sprintf(pos, "%c%x", c[rand()%strlen(c)], b%15 );
                break;
            default:
                sprintf(pos, "%02x", b);
                break;
        }
        pos += 2;
    }
    *pos = '\0';
    return buf;
}
 
void main()
{
    char guid[4job];
    random_uuid(guid);
    printf("guid = %s\n", guid);
    random_uuid(guid);
    printf("guid = %s\n", guid);
    random_uuid(guid);
    printf("guid = %s\n", guid);
    random_uuid(guid);
    printf("guid = %s\n", guid);
}
