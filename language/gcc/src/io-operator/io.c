#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "io.h"

/*
 * 功能：清除缓存，见apue中说明
 */
void clear_stdbuf()
{
    int         c;

    while((c=getchar()) != '\n');
}

/*
 * 功能：获取str串中在module字符前子串
 */
int
get_specified_sring(const char *src, char *dst, const char *module)
{               
    const char      *temp = src;
                    
    while (*temp != '\0') {
        if (strchr(module, *temp) != NULL) {
            break;      
        }               
        temp++;         
    }
    strncpy(dst, src, temp-src);
    dst[temp-src] = '\0';

    return 0;
}

/*
 * 功能：替换st中的子串orig为repl串
 */
char *replace_one(char *st, char *orig, char *repl) 
{
    static char buffer[4096];
    char        *ch;

    if (!st || !orig || !repl) {
        return NULL;
    }

    if (!(ch = strstr(st, orig))) {
        return st;
    }

    strncpy(buffer, st, ch-st);  
    buffer[ch-st] = 0;
    sprintf(buffer+(ch-st), "%s%s", repl, ch+strlen(orig));

    return buffer;
}

/*
 * 功能：替换st中的所有子串orig为repl串
 */
char *replace_str2(const char *str, const char *old, const char *new)
{
    char                *ret, *r;
    const char          *p, *q;
    size_t              oldlen;
    size_t              count, retlen, newlen;
    int                 samesize;
    int                 l;

    oldlen = strlen(old);
    newlen = strlen(new);
    samesize = (oldlen == newlen);

    if (!samesize) {
        for (count = 0, p = str; (q = strstr(p, old)) != NULL; p = q + oldlen) {
            count++;
        }
        /* This is undefined if p - str > PTRDIFF_MAX */
        retlen = p - str + strlen(p) + count * (newlen - oldlen);
    } else {
        retlen = strlen(str);
    }

    /* malloc memory */
    if (!(ret = malloc(retlen + 1))) {
        return NULL;
    }

    r = ret, p = str;
    while (1) {
        if (!samesize && !count--)
            break;
        if ((q = strstr(p, old)) == NULL)
            break;
        /* This is undefined if q - p > PTRDIFF_MAX */
        l = q - p;
        memcpy(r, p, l);
        r += l;
        memcpy(r, new, newlen);
        r += newlen;
        p = q + oldlen;
    }
    strcpy(r, p);

    return ret;
}

