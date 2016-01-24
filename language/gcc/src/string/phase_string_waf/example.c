#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define     ENABLE      1
#define     DISABLE     0
#define     BUFLEN      1024

typedef struct condition condition;
struct condition {
    char        variables[512];
    char        operator[32];
    char        trfns[32];
    char        expression[256];
};

const char escapeCharacter[] = {'\'', '(', ')', '\\', '"'};

enum {
    WAF_USER_DEFINED_INIT = -1,
    WAF_USER_DEFINED_VAR,
    WAF_USER_DEFINED_OPT,
    WAF_USER_DEFINED_TRFNS,
    WAF_USER_DEFINED_EXP,
    WAF_USER_DEFINED_MAX,
};
const char* keyCharacter[] = {
    "variables",
    "operator",
    "trfns",
    "expression",
};

/*
 * func:判断转义字符是否为指定的字符
 */
int escape_judge(char ch)
{
    int         i = 0;
    int         len = sizeof(escapeCharacter)/sizeof(escapeCharacter[0]);

    for (i=0; i<len; i++) {
        if (ch == escapeCharacter[i]) {
            return 0;
        }
    }

    return -1;
}
int convert(const char *str) // 常量指针，指向的为main函数里的字符串常量  
{  
    long result=0,f=1;

    while(*str!='\0' && *str>='0' && *str<='9')
    {
        result=result*10 + *str-'0';  //此处务必要将*str的值减去‘0’，因为它是ascii码的值
        str++;
    }

    return ((*str!='\0') ? -1 : result*f);
} 

/*
 * func:判断对应的key值
 */
int key_judge(const char *string) 
{
    int         i = 0;

    if (NULL == string || !strlen(string)) {
        return -1;
    }

    for (i=0; i<WAF_USER_DEFINED_MAX; i++) {   
        if (strcmp(string, keyCharacter[i]) == 0) {
            return i;
        }
    }
    return -1;
}

/*
 * func:判断每个属性值并存储
 */
int value_assign(condition *cond, const char *string, unsigned int flag)
{
    int             len = -1;

    if (NULL == string || !(len=strlen(string)) ) {
        return -3;
    }

    switch (flag) {
        case WAF_USER_DEFINED_VAR:
            if ((len+1) > 512) {
                return -1;
            }
            strcpy(cond->variables, string);
            break;
        case WAF_USER_DEFINED_OPT:
            if ((len+1) > 32) {
                return -1;
            }
            strcpy(cond->operator, string);
            break;
        case WAF_USER_DEFINED_TRFNS:
            if ((len+1) > 32) {
                return -1;
            }
            strcpy(cond->trfns, string);
            break;
        case WAF_USER_DEFINED_EXP:
            if ((len+1) > 256) {
                return -1;
            }
            strcpy(cond->expression, string);
            break;
        default:
            return -4;
    }

    return 0;
}

int phase_string(const char *string, condition *cond, int *conditionIndex)
{
    const char  *p = NULL;
    char        tempBuf[BUFLEN] = {'\0'};        //栈
    int         escapeFlag = DISABLE;
    int         bracketFlag = DISABLE;
    int         doubleQuoteFlag = DISABLE;
    int         spaceFlag = DISABLE;
    int         keyFlag = WAF_USER_DEFINED_INIT;
    int         index = 0, ret = -1, condIndex = -1;

    if (NULL == string || NULL == cond) {
        return -1;
    }

    printf("HANDLE STRING: %s\n", string);
    p = string;
    while (*p != '\0') {
        printf("%c", *p);
        if ('s' == *p) {
            ret = -1;
        }
        if (ENABLE == escapeFlag) {          // deal escape character
            if (escape_judge(*p) < 0) {
                return -2;
            }
            tempBuf[index++] = *p;
            escapeFlag = DISABLE;
            goto next;
        }

        if (' ' == *p) {                    // deal space character
            if (ENABLE == doubleQuoteFlag) {
                tempBuf[index++] = *p;
            } else if (DISABLE == spaceFlag) {
                spaceFlag = ENABLE;
            }
            goto next;
        }

        spaceFlag = DISABLE;
        if ('(' == *p) {
            if (condIndex >= 5) {
                return -1;
            }
            bracketFlag = ENABLE;           // go into a (...)           
            condIndex++;

        } else if (')' == *p) {             // quit a (...)
            // redo initialize.
            memset(tempBuf, 0, BUFLEN);
            index = 0;
            bracketFlag = DISABLE;          
            keyFlag = WAF_USER_DEFINED_INIT;
            doubleQuoteFlag = DISABLE;
            spaceFlag = DISABLE;

        } else if ('"' == *p) {             // go into or quit a "..."
            if (DISABLE == doubleQuoteFlag) {
                doubleQuoteFlag = ENABLE;
            } else {
                if (keyFlag < WAF_USER_DEFINED_VAR || keyFlag > WAF_USER_DEFINED_EXP) {
                    return -1;
                }
                if (value_assign(&cond[condIndex], tempBuf, keyFlag) < 0) {
                    return -1;
                }
                memset(tempBuf, 0, BUFLEN);
                index=0;
                doubleQuoteFlag = DISABLE;
                keyFlag = WAF_USER_DEFINED_INIT;
            }

        } else if (':' == *p) {
            if (WAF_USER_DEFINED_INIT != keyFlag) {
                return -1; 
            } else {
                if ((ret = key_judge(tempBuf)) < 0) {
                    return ret;
                }
                keyFlag = ret;
                memset(tempBuf, 0, BUFLEN);
                index = 0;
            }

        } else if ('\\' == *p) {
            escapeFlag = ENABLE;

        } else {
            tempBuf[index++] = *p;
        }
next:
        p++;
    }//while
    *conditionIndex = condIndex;

    return 0;
}
int 
input_string(char *input)
{
    char        ch = '0';

    while ((ch=getchar()) != '\n') {
        *input++ = ch;
    }
    return 0;
}

int main(int argc, char **argv)
{
    condition           cond[5];
    char                input[1024] = {0};
    int                 ret = -1, i;
    int                 conditionIndex = 0;

    while (1) {
        memset(input, 0, 1024);
        memset(cond, 0, sizeof(condition)*5);

        if (input_string(input) < 0) {
            printf("\nInput failure\n");
            continue;
        }
        //ret = phase_string("(variables:3 expression:\"xxxx   xxx\" operator:4 trfns:job)", 
        ret = phase_string(input, cond, &conditionIndex);   
        if (ret < 0) {
            printf("\nPhase string occur error!\n");
            continue;
        } 

        printf("\nEND:\n");
        for (i=0; i<=conditionIndex; i++) {
            printf("%s %s %s %s\n", cond[i].operator, cond[i].variables, cond[i].trfns, cond[i].expression);
        }
    }

    return 0;
}
