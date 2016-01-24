#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <glob.h>
#include <linux/kernel.h>

#define A(s)        #s
#define _A(s)       A(s)
#define ST(a, b)    (a##XX##b) 
#define _ST(a, b)   ST(a, b) 

#define B           (2)
#define INT_MAX     ABC
#define _STR(s)     #s
#define STR(s)      _STR(s)          // 转换宏
#define _CONS(a,b)  int(a##e##b)
#define CONS(a,b)   _CONS(a,b)       // 转换宏

#define myprintf(...) printf("[lch]:File:%s, Line:%d, Function:%s," \
        __VA_ARGS__, __FILE__, __LINE__ ,__FUNCTION__);

int main(int argc, char **argv)
{
    //printf("%s\n", _A(_ST(_A(l),_A(l))) );
    printf("int max: %s\n", STR(INT_MAX)); 

    printf("哇哈哈:%s\n", STR(STR(INT_MAX)) );

    // ASCI标准规定这个是合法的
    printf("aagege""agegege\n");

    myprintf("....");

    return 0;
}
