/*
 * 功能:测试scanf函数的各个功能
 */
#include "io.h"

/*
 * 功能:测试基本的功能以及转换说明符
 */
void
simple_test()
{
    char        buf[128];
    char        item;
    int         digit;

    printf("测试%%c %%s %%d转换说明符:\n");
    scanf("%c %s %d", &item, buf, &digit);
    printf("你输入的字符为:%c\n"
            "\t字符串:%s\n"
            "\t整数:%d\n",
            item, buf, digit);
}

/*
 * 功能:验证 换行-制表-空格 都属于<空格>的范畴
 * 要求：请自己解释原因
 */
void 
simple_blankspace()
{
    int     i;
    printf("换行-制表-空格都属于《空格》\n");
    printf("请输入一个数字:\n");
    scanf("%d\n", &i);
    printf("i=%d\n", i);
    printf("=============================\n");
}

/*
 * 功能:利用sscanf函数模拟人工输入，验证各个转换说明符的断点
 * 要点1：只有%c不当《空格》为空格。
 * 要点2：注意%s %c之间的空格跳过了多少《空格》
 */
void
breakpoint_test()
{
    char        *str, *strO;
    char        buf[128];
    char        item;
    int         digit;
    
    printf("断点========================\n");
    str = "\n shit\t \nB 345d53 xxgge";
    strO = "\\n shit\\t \nB 345d53 xxgge";
    printf("欲输入的字符串为:%s\n", strO);
    sscanf(str, "%s %c %d", buf, &item, &digit);
    printf("buf=%s item=%c digit=%d\n\n", buf, item, digit);

    buf[0] = '\0';
    item = '\0';
    digit = 0;
    printf("断点========================\n");
    str = "\n B xxxx 1234";
    strO = "\\n B xxxx 1234";
    printf("欲输入的字符串为:%s\n", strO);
    sscanf(str, "%c %s %d", &item, buf, &digit);
    printf("item=%c buf=%s digit=%d\n\n", item, buf, digit);
}

/*
 * 功能：sscanf测试
 * PS：请注意scanf和sscanf的输入来源，一个是buf，一个是stdin，
 *      这个在正则匹配时会有很大的差别，因为stdin是公有的。
 */
void sscanf_test(void)
{
    int         ret;
    char        *string = NULL;
    int         digit;
    char        buf1[255];
    char        buf2[255];
    char        buf3[255];
    char        buf4[255];


    /*1.最简单的用法*/
    printf("======================================\n");
    string = "UESTC EE 4200802";
    ret = sscanf(string, "%s %s %d", buf1, buf2, &digit);
    printf("1.string=%s\n", string);
    printf("1.ret=%d, buf1=%s, buf2=%s, digit=%d\n\n", ret, buf1, buf2, digit);
    /***********************************************
    1.string=UESTC EE 4200802
    1.ret=3, buf1=UESTC, buf2=EE, digit=4200802
    ***************************************************/


    /*2.取指定长度的字符串*/
    printf("======================================\n");
    string = "123456789";
    sscanf(string, "%5s", buf1);
    printf("2.string=%s\n", string);
    printf("2.buf1=%s\n\n", buf1);
    /****************************************
    2.string=123456789
    2.buf1=12345
    ***************************************/

    /*3.取到指定字符为止的字符串*/
    printf("======================================\n");
    string = "123/456";
    sscanf(string, "%[^/]", buf1);
    printf("3.string=%s\n", string);
    printf("3.buf1=%s\n\n", buf1);
    /********************************************
    3.string=123/456
    3.buf1=123
    ********************************************/

    /*4.取到指定字符集为止的字符串*/
    printf("======================================\n");
    string = "123abcABC";
    sscanf(string, "%[^A-Z]", buf1);
    printf("4.string=%s\n", string);
    printf("4.buf1=%s\n\n", buf1);
    /***********************************
    4.string=123abcABC
    4.buf1=123abc
    ************************************/

    /*5.取仅包含指定字符集的字符串，如果不合法，出错*/
    printf("======================================\n");
    string = "0123abcABC";
    sscanf(string, "%[0-9]%[a-z]%[A-Z]", buf1, buf2, buf3);
    printf("5.string=%s\n", string);
    printf("5.buf1=%s, buf2=%s, buf3=%s\n\n", buf1, buf2, buf3);
    /*******************************************
    5.string=0123abcABC
    5.buf1=0123, buf2=abc, buf3=ABC
    如果不合法：
        5.string=0123#abcABC
        5.buf1=0123, buf2=EE, buf3=
    *******************************************/

    /*6.获取指定字符中间的字符串，其中*表示跳过*/
    printf("======================================\n");
    string = "ios<Android>wp7";
    sscanf(string, "%*[^<]<%[^>]", buf1);
    printf("6.string=%s\n", string);
    printf("6.buf1=%s\n\n", buf1);
    /*************************************
    6.string=ios<Android>wp7
    6.buf1=Android
        其中%*[^<]表示跳过"<"之前的所有字符
    ***************************************/

    /*7.指定要跳过的字符串*/
    printf("======================================\n");
    string = "iosVSandroid";
    sscanf(string, "%[a-z]VS%[a-z]", buf1, buf2);
    printf("7.string=%s\n", string);
    printf("7.buf1=%s, buf2=%s\n\n", buf1, buf2);
    /*******************************
    7.string=iosVSandroid
    7.buf1=ios, buf2=android
    ************************************/

    /*8.分割以某字符隔开的字符串*/
    printf("======================================\n");
    string = "android-iphone-wp7";
    /************************************************
    **字符串取道'-'为止,后面还需要跟着分隔符'-',
    **起到过滤作用,有点类似于第7点
    *************************************************/
    sscanf(string, "%[^-]-%[^-]-%[^-]", buf1, buf2, buf3);
    printf("8.string=%s\n", string);
    printf("8.buf1=%s, buf2=%s, buf3=%s\n\n", buf1, buf2, buf3);
    /***********************************************
    8.string=android-iphone-wp7
    8.buf1=android, buf2=iphone, buf3=wp7
    **************************************************/

    /*9.提取邮箱地址*/
    printf("======================================\n");
    string = "Email:shihui512@139.com";
    sscanf(string, "%[^:]:%[^@]@%[^.].%s", buf1, buf2, buf3, buf4);
    printf("9.string=%s\n", string);
    printf("9.buf1=%s, buf2=%s, buf3=%s, buf4=%s\n\n", buf1, buf2, buf3, buf4);
    /**************************************
    9.string=Email:shihui512@139.com
    9.buf1=Email, buf2=shihui512, buf3=139, buf4=com
    *************************************/

    /*10.获取有空格的字符串*/
    printf("======================================\n");
    string = "black space (~_~)\nxxx";
    sscanf(string, "%[^\n]", buf1);
    printf("10.string=%s\n", string);
    printf("10.buf1=%s\n\n", buf1);
    /**************************************
    10.string="black space (~_~)\nxxx"
    10.buf1=black space (~_~)
    *************************************/

    /* 11. 获取键值对中的键值 */
    printf("======================================\n");
    string = "mylove = pan";
    sscanf(string, "%[^=|^ |^\t]", buf1);
    printf("11.string=%s\n", string);
    printf("11.buf1=%s\n\n", buf1);

    /* 12. 获取键值对中的键值，并非sscanf函数 */
    printf("======================================\n");
    string = "mylove = pan";
    get_specified_sring(string, buf1, "= \t");
    printf("11.string=%s\n", string);
    printf("11.buf1=%s\n\n", buf1);

    /* 13. 将\xE5的16进制表示的数转化为真正的16进制数 */
    printf("======================================\n");
    string = "\\xE5\\x8C\\x97\\xE4\\xBA\\xAC\\xE5\\xB8\\x82";
    sscanf(string, "\\x%[0-9|A-F]", buf1);
    printf("13.string=%s\n", string);
    printf("13.buf1=\\x%s\n\n", buf1);
}

int 
main(int argc, char **argv)
{
    //simple_test();
    breakpoint_test();
    simple_blankspace();
    sscanf_test();

    return 0;
}
