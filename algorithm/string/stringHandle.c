#include <stdio.h>
#include <stdlib.h>
#include "string.h"
/**
 * @file stringHandle.c
 * @brief   string 操作集锦
 * @author unlessbamboo
 * @version 1.0
 * @date 2016-02-17
 */


/**
 * @brief   stringRepeatNum :统计字符串中所有字符出现的次数
 *      分析：
 *          使用hash表进行（因为首先知道了字符串的取值范围，256字母），
 *          关于hash，在对应章节有相应说明
 *
 * @param   str1
 *
 * @return  
 */
bool stringRepeatNum(char *str1, char *hashList)
{
    int                     i;
    char                    *tmp = NULL;

    if (NULL == hashList) {
        return false;
    }

    // 初始化hash表
    for (i=0; i<256; i++) {
        hashList[i] = 0;
    }

    // 统计
    tmp = str1;
    while (tmp && *tmp != '\0') {
        hashList[*tmp]++;
        tmp++;
    }

    return true;
}


/**
 * @brief   stringExact (提取或者字符串的左右移动)
 *      提取字符串的特定字符，其他字符按照原有顺序拼接，例如：
 *              a*bc*degelge***xx 变为*****abcdegelgexx
 *      分析：
 *          从后面（尾部开始这个思想非常棒啊）扫描，碰到非*字符
 *          移动到末尾，一直不断累加
 *          最后将前面的所有设置为*
 *      算法：
 *          此类解题思路非常有意思，提取的字符是一个通用的、标准化的美女
 *          那么我如何筛选美女呢？类似桶的思想（桶都有了），那么
 *              我仅仅将丑的人依次存放;
 *              最后将美女一股脑儿的随便放置（管你）
 *
 *      PS:
 *          该方法也同时用于字符的删除操作，见下面
 *
 * @param   str1
 *
 * @return  
 */
int stringExact(char *str1)
{
    int             str_len = strlen(str1), i, end;

    end = str_len;

    for (i=str_len-1; i>=0; --i) {
        if (str1[i] != '*') {
            str1[--end] = str1[i];
        }
    }

    // 首部填充
    for (--end; end>=0; --end) {
        str1[end] = '*';
    }

    return true;
}


/**
 * @brief   stringDelete :删除str1中的所有在strdel中的字符
 *      分析：
 *          1，通用方法：
 *              对于strdel中的每一个字符m：
 *                  遍历str1，判断下一个字符是否相同
 *                  如果相同，删除并移动后面的字符
 *              总的时间O(n2*m)
 *          仿照上面stringExact的解题思路:
 *              利用哨兵机制，有点像链表中的双指针（这个在很多地方用处很大）
 *              毕竟人多力量大，双指针标准在处理很多问题是近似于达到
 *              二分效果
 *          2，算法
 *              冲锋部队只管往前移动，删除无用字符，碰到我方"军民"
 *                  "老乡，往后面走，碰到哨兵部队，会安置你的"
 *              后续哨兵部队，只有碰到冲锋部队标识的我方"军民"，接纳
 *              总时间O(n)
 *          3，操作流程
 *              首先统计strdel中的各个字符的hash值，功能：
 *                  保证最低的循环次数；
 *                  一次就可以对所有的m进行查找操作（O(m)）
 *              遍历字符串，对于字符s:
 *                  hash查找，如果为0，表示不需要删除，否则删除
 *              继续
 *
 *          PS:
 *              桶或者hash算法适用于非常多的场景，特别是统计次数场景中
 *              例如：
 *                  返回n个整数中某一个整数出现的次数；
 *                  数组中某一个次数超过k的值等 
 *
 * @param   str1
 * @param   strdel
 *
 * @return  
 */
int stringDelete(char *str1, char *strdel)
{
    unsigned int                  *hashList = NULL;
    char                          *slow, *fast, *tmp;

    hashList = (unsigned int*)malloc(256*sizeof(unsigned int));
    if (NULL == hashList) {
        return false;
    }

    // 初始化hash表
    tmp = strdel;
    while (*tmp != '\0') {
        hashList[*tmp]++;
        tmp++;
    }

    // 删除
    slow = fast = str1;
    while (*fast != '\0') {
        if (0 == hashList[*fast]) {
            *slow++ = *fast;
        }
        fast++;
    }

    // 尾部
    *slow = '\0';
    
    return true;
}


/**
 * @brief   stringReverse ：见stringReverse.py文件
 *
 * @param   str1
 *
 * @return  
 */
int stringReverse(char *str1)
{
    return true;
}



