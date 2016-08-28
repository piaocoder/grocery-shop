/**
 * @file typedef.c
 * @brief typedef的用法例子，首先typedef不是一个MACRO
 * @author unlessbamboo@gmail.com
 * @version 1.0
 * @date 2016-08-28
 */

#include <stdio.h>



/**
 * @brief  定义一个DISPLAY类型，指向函数void (*func)(char *);
 *
 * @param 
 *
 * @return 
 */
typedef void (*DISPLAY)(char *);


/**
 * @brief display :打印函数
 *
 * @param msg
 */
void display(char *msg)
{
    printf("Display:%s\n", msg);
}



/**
 * @brief do_special_handle 根据flag和DISPLAY变量，打印不同的值，
 *                      这里用到了typedef和函数指针的用法哦
 *                  1,注意函数指针中实参和形参的用法
 *
 * @param flag  标志变量
 * @param func  函数指针变量
 *
 * @return 
 */
int do_special_handle(int flag, DISPLAY func)
{
    if (flag < 0 ) {
        func("这是一个负数！");
    } else if (flag == 0) {
        func("这是一个非负非正数哦!");
    } else {
        func("这是一个正数！");
    }

    return 0;
}



int main(int argc, char **argv)
{
    // 注意实参传入真正的函数名称
    printf("===================1=================\n");
    do_special_handle(-3, display);

    return 0;
}
