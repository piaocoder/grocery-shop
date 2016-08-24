/*
 * 功能：测试程序的内存布局
 */
#include <stdio.h>
#include <stdlib.h>

int i1 = 10; //静态全局区(data段)
int i2; //静态全局区(bss段)
static int i3 = 30; //静态全局区(data段)
const int i4 = 40;  //代码区!!!


void fun(int i5) //栈区
{
    int i6 = 60; //栈区
    static int i7 = 70; //静态全局区(data段)
    const int i8 = 80; //栈区!!!
    char* str1 = "ABCDE"; //代码区(字符串常量)
    char str2[] = "ABCDE"; //栈区(字符数组)
    int* pi = malloc(sizeof(int)); //堆区

    for (int i=0; i<10; i++) {
        printf("&i5=%p\n", &i5);
        printf("&i6=%p\n", &i6);
        printf("&i7=%p\n", &i7);
        printf("&i8=%p\n", &i8);
        printf("str1=%p\n", str1);
        printf("str2=%p\n", str2);
        printf("pi=%p\n", pi);
    }
    free(pi);
}

int main(void)
{
    printf("&i1=%p\n", &i1);
    printf("&i2=%p\n", &i2);
    printf("&i3=%p\n", &i3);
    printf("&i4=%p\n", &i4);
    fun(50);
    return 0;
}
