#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>

typedef struct condition condition;
struct condition {
    char        variables[512];
    char        operator[64];
    char        trfns[256];
    char        expression[256];
};

void testMacro(void)
{
#define LINE        "aaaaa\r\n"

    printf("Macro(\"\\r\\n\") is %lu:\n", sizeof(LINE));
    printf("Macro strlen (\"\\r\\n\") is %lu:\n",strlen(LINE));
}

void testConstString(void)
{
    const char *str = "abcdef";

    printf("abcdef is %lu\n", sizeof(str));
    printf("shit is %lu\n", sizeof("shit"));
}

int main(int argc,char** argv) 
{
    const char      *a = "";
    const char      *cookie = "Set-cookie";
    int              num = atoi(a);

    testMacro();
    testConstString();

    printf("%d\n", num);
    printf("condition--%lu\n", sizeof(condition)*5);
    printf("set-cookie--%lu--%lu\n", sizeof("set-cookie"), sizeof(cookie));

    return 0;
}
