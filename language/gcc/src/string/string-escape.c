/*
 * 功能：字符串转义解析
 *       字符编码输出
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

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
        /* If the old and new strings are different lengths - in other
         * words we have already iterated through with strstr above,
         * and thus we know how many times we need to call it - then we
         * can avoid the final (potentially lengthy) call to strstr,
         * which we already know is going to return NULL, by
         * decrementing and checking count.
         */
        if (!samesize && !count--)
            break;
        /* Otherwise i.e. when the old and new strings are the same
         * length, and we don't know how many times to call strstr,
         * we must check for a NULL return here (we check it in any
         * event, to avoid further conditions, and because there's
         * no harm done with the check even when the old and new
         * strings are different lengths).
         */
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

/** 
 * @brief   判断后面一定长度的字符是否为16进制数
 * 
 * @param   ptr
 * @param   len
 * 
 * @return  -1  --  没有发现
 *          0   --  发现
 */
int
str_escape_isDec(char *ptr, unsigned int len)
{
    char            *temp = ptr;
    char            c = '\0';
    int             flag = -1;

    while ((c = *temp++)!= '\0' && len-->0) {
        if ((c<'0'||c>'9') && (c<'A' || c>'F')&&(c<'a' || c>'f')) {
            flag = -1;
            break;
        }
        flag = 0;
    }

    return flag;
}

/*
 * 功能：将16进制的表示数重新转为字符
 */
int
str_escape_traverse_dec(char *src, char *dst, int *srcLen)
{
    const char      *substr = "\\x";
    int             sublen , declen, totalLen;
    int             stringlen = 0, tmpLen, dstLen = 0;
    char            *curPointer = NULL, *prePointer = NULL;
    char            *dstPointer = NULL;
    unsigned int    c = 0;

    /*substring length and decimal string length*/
    sublen = strlen(substr);
    declen = strlen("EE");
    totalLen = strlen("\\xEE");

    /*initialize*/
    stringlen = *srcLen;
    prePointer = curPointer = src;
    dstPointer = dst;

    /*traverse src*/
    while (stringlen > 0) {
        if ((curPointer = strstr(prePointer, substr)) == NULL) {
            strcpy(dstPointer + dstLen, prePointer);
            tmpLen = strlen(prePointer);
            tmpLen = tmpLen==0?1:tmpLen;//Important
            dstLen += tmpLen;
            stringlen -= tmpLen;
            prePointer += tmpLen;
        } else {
            strncpy(dstPointer + dstLen, prePointer, curPointer-prePointer);
            dstLen += (curPointer-prePointer);
            stringlen -= (curPointer-prePointer);

            if (str_escape_isDec(curPointer+sublen, declen) >= 0) {
                sscanf(curPointer, "\\x%02x", &c);
                memcpy(dstPointer + dstLen, &c, sizeof(char));
                dstLen += sizeof(char);
                stringlen -= totalLen;
                curPointer += totalLen; 
            } else {
                strncpy(dstPointer + dstLen, curPointer, sublen);
                dstLen += sublen;
                stringlen -= sublen;
                curPointer += sublen; 
            }
            prePointer = curPointer;
        }
    }
    // tail operator
    *srcLen = dstLen;
    *(dstPointer+dstLen) = '\0';

    return 0;
}

/*
 * 功能：遍历一个包含转义字符的字符串
 */
int
str_escape_traverse(char *str)
{
    char        c;
    char        *p = str;

    if (!p) {
        return -1;
    }

    while((c=*p++)!='\0') {
        printf("Current character is %c\n", c);
    }
    return 0;
}

/** 
 * @brief   按照module格式进行字节串的输出并转换
 *          对于0-127ASCII字符不做任何处理
 * 
 * @param   str
 * @param   dst
 * @param   module
 * 
 * @return  
 */
int 
str_escape_format_convert(const char *str, char *dst, int *len, 
                                const char *module, int modLen)
{
    int             c = '\0';
    const char      *point = str;
    char            hexBuf[10] = {0};
    int             srcLen = *len, dstLen = 0;

    if (module == NULL) {
        memcpy(dst, str, *len);
        return 0;
    }

    while (srcLen-- > 0) {
        if ((c = *point++) == '\0') {
            *(dst+dstLen) = c;
            dstLen++; 
        } else {
            if (isascii(c)) {
                *(dst+dstLen) = c;
                dstLen++; 
            } else {
                sprintf(hexBuf, module, (unsigned char)c);
                strncpy(dst+dstLen, hexBuf, modLen);
                dstLen += modLen;
            }
        }
    }
    *len = dstLen;

    return 0;
}


/** 
 * @brief   获取一个字节串的长度
 * 
 * @param   str
 * 
 * @return  
 */
int
str_escape_get_len(const char *str, const char *endstr)
{
    const char          *ptr = str, *end;

    while ((end=strstr(ptr, endstr)) == NULL) {
        ptr += (strlen(ptr) + 1);
    }

    return end-str;
}

/** 
 * @brief   显示字节串
 * 
 * @param   str
 * @param   len
 */
void
str_escape_display(const char *str, int len)
{
    const char      *tmpPtr = str;
    unsigned int    tmpLen = 0;

    while (len > 0) {
        tmpLen = strlen(tmpPtr) + 1;
        putchar('\t');
        puts(tmpPtr);
        len -= tmpLen;
        tmpPtr += tmpLen;
    }
}

int 
main(int argc, char **argv)
{
    /*char        *str = "lage\txxx\nyyyyy\fbbbbbbb";*/
    const char    *cstr = "北京市:串结束\0\\x2哇哈哈:串结束\0So stupid,呵呵xxEND";
    char          *buf, *dst;
    int           len = 0, tmpLen = 0; 

    /*printf("===========================================\n");*/
    /*printf("转义字符串遍历:\n");*/
    /*str_escape_traverse(str);*/

    buf = (char*)malloc(512);
    if (buf == NULL) {
        return -1;
    }
    memset(buf, 0, 512);
    dst = (char*)malloc(1024);
    if (buf == NULL) {
        return -1;
    }
    memset(dst, 0, 1024);

    printf("\n===========================================\n");
    printf("整个字节串的长度为:%u\n", (len=str_escape_get_len(cstr, "END"))); 

    printf("多字节编码字符输出显示(module==NULL):\n");
    tmpLen = len;
    str_escape_format_convert(cstr, buf, &tmpLen, NULL, 0);
    str_escape_display(buf, tmpLen);

    printf("\n多字节编码字符输出显示(module==\\x%%02x):\n");
    memset(buf, 0, 512);
    tmpLen = len;
    str_escape_format_convert(cstr, buf, &tmpLen, "\\x%02x", 4);
    str_escape_display(buf, tmpLen);

    printf("\n将多字节编码字符重新以正常形式输出：\n");
    memset(dst, 0, 1024);
    str_escape_traverse_dec(buf, dst, &tmpLen);
    str_escape_display(dst, tmpLen);

    /*
    printf("\n===========================================\n");
    strcpy(buf, "Subject: C=zn, \0ST=\\xE6\\xB2\\xB3\\xE5\\x8C\\x97\\xE7\\x9C\\x81, \0L=\\xE5\\x8C\\x97\\xE4\\xBA\\xAC\\xE5\\xB8\\x82");
    temp[0] = '\0';
    str_escape_traverse_dec(buf, temp, NULL);
    printf("%s\n", temp);
    */

    putc('\n', stdout);
    return 0;
}
