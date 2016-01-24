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

    printf("Macro(\"\\r\\n\") is %d:\n",sizeof(LINE));
    printf("Macro strlen (\"\\r\\n\") is %d:\n",strlen(LINE));
}

void testConstString(void)
{
    const char *str = "abcdef";

    printf("abcdef is %d\n", sizeof(str));
    printf("shit is %d\n", sizeof("shit"));
}

int main(int argc,char** argv) {

    testMacro();
    testConstString();

    const char      *a = "";
    const char      *cookie = "Set-cookie";
    int num = atoi(a);
    printf("%d\n", num);

    printf("condition--%d\n", sizeof(condition)*5);
    printf("set-cookie--%d--%d\n", sizeof("set-cookie"), sizeof(cookie));

    return 0;
}
