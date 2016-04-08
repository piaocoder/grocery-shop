/**
 * @file getopt-test.c
 * @brief   getopt相关函数的测试用例
 * @author unlessbamboo
 * @version 1.0
 * @date 2016-04-07
 */
#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>

/*
 * 长选项
 *  name选项名
 *  has_arg，(no_argument, required_arugment, optional_argument
 *  flags,  NULL——返回val值，非NULL——填充val，此时getopt_long返回0
 *  val，长选项对应的短选项名称，作为opt的返回值
 */
struct option longopts[] = {
    {"config", required_argument, NULL, 0},
    {"name", required_argument, NULL, 'n'},
    {NULL, 0, NULL, 0},
};
const char *shortopts = "n:";

/**
 * @file getopt-test.c
 * @brief   测试getopt_long函数
 * @author unlessbamboo
 * @version 1.0
 * @date 2016-04-07
 */
int test_getopt_long(int argc, char **argv)
{
    int             opt = 0, longindex;

    opterr = 0;
    while ((opt = getopt_long(argc, argv, shortopts, 
                    longopts, &longindex)) != EOF) {
        switch (opt) {
            case 'n':
                printf("短选项，参数值%s\n", optarg);
                break;
            case 0:
                printf("长选项,index:%d, 参数值:%s\n", longindex, optarg);
                break;
            default:
                printf("无效的参数:opt:%c.\n", opt);
                break;
        }
    }

    return 0;
}


int main(int argc, char **argv)
{
    printf("Begin test getopt.\n");
    printf("getopt_long输出：\n");
    test_getopt_long(argc, argv);

    return 0;
}
