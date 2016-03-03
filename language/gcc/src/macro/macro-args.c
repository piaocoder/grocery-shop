#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

void 
simple_va_fun(int i, ...)
{
   va_list arg_ptr;
   int j=0; 
   
   va_start(arg_ptr, i);
   j=va_arg(arg_ptr, int);
   va_end(arg_ptr);
   printf("%d %d\n", i, j);
   return;
}

void var_second_vsnp(const char *fmt, ...)
{
    va_list     ap;
    char        buf[1024];

    va_start(ap, fmt);
    vsnprintf(buf, 1024, fmt, ap);
    va_end(ap);

    printf("_________________________\n");
    printf("Format=%s\n", fmt);
    printf("_________________________\n");
    printf("Second output:%s\n", buf);
    printf("_________________________\n");
}

void
var_vsnprintf(const char *fmt, ...)
{
    va_list arg_ptr;
    char    buf[1024];

    va_start(arg_ptr, fmt);
    vsnprintf(buf, 1024, fmt, arg_ptr);
    var_second_vsnp(buf);
    va_end(arg_ptr);

    printf("Output:%s\n", buf);
}

void 
error_second_vsnp(const char *fmt, ...)
{
    va_list ap;
    char    buf[1024];

    va_start(ap, fmt);
    vsnprintf(buf, 1024, fmt, ap);
    va_end(ap);
    printf("Error test:%s\n", buf);
}

int 
main(int argc, char **argv)
{
    simple_va_fun(100);
    printf("==============================\n");
    simple_va_fun(100, 200);
    printf("==============================\n");
    simple_va_fun(100, 200, 300);

    //error_second_vsnp("test:%d=3, %s=XXXXX\n");
    error_second_vsnp("test:=3, =XXXXX\n");
    var_vsnprintf("test:%%d=%d, %%s=%s+++\n", 3, "vsnprintf");

    return 0;
}
