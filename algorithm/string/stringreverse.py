#!/usr/bin/env python
#coding:utf-8
##
# @file stringOperator.py
# @brief    字符串各种操作集合（python语言）
# @author unlessbamboo
# @version 1.0
# @date 2016-02-17
import array


def reverseString(str1):
    """reverseString
       分析：
           1，标准库：s1[::-1]
           2，字符缓存：
               使用额外的字符串空间存储，遍历即可
           3，字符串交换
               交换i 和 n-i字符，不过必须提前知道串长度
               其中交换使用：
                   a = a ^ b
                   b = b ^ a
                   a = a ^ b
           4，递归操作
                使用原语力量，递归的进行字符组合反转操作，
                每次仅仅更换两个组合，分治递归，最后成功反转
                    [0..i]和[i+1..n]
                    =======
                    [i+1..j]和[j+1..n]反转，其他
                    =======
                    [j+1..k]和[k+1..n]反转..
                例子：
                    1 2 3 4 5 6 7 8
                    ---------------
                    5 6 7 8 | 1 2 3 4
                    -----------------
                    7 8 | 5 6 | ...
                    -----------------
                    8|7|...
                    -----------------
                    8 7 6 5 4 3 2 1
           5，utf8交换
               需要判断首字节0xF/0xE/0xC,0xD，有选择的移动字节

    :param str1:
    """
    array1 = array.array('B', str1)
    str_len = len(array1)

    for i in range(str_len / 2 - 1):
        array1[i], array1[str_len - i - 1] = array1[str_len - i - 1], array1[i]

    return array1.tostring()


def reverseUtf8(str1):
    """reverseUtf8:reverse utf8 string

    :param str1:
    """
    str1 = reverseString(str1)

    array1 = array.array('B', str1)
    str_len = len(array1)
    start = 0
    end = str_len - 1

    while start < end:
        tmp_ch = (array1[end] & 0xF0) >> 4
        if tmp_ch == 0xF:
            # 四字节，交换
            array1[end], array1[end - 3] = array1[end - 3], array1[end]
            array1[end - 1], array1[end - 2] = array1[end - 2], array1[end - 1]
            end -= 4
        elif tmp_ch == 0xE:
            # 三字节
            array1[end], array1[end - 2] = array1[end - 2], array1[end]
            end -= 3
        elif tmp_ch == 0xC or tmp_ch == 0xD:
            array1[end], array1[end - 1] = array1[end - 1], array1[end]
            end -= 2
        else:
            end -= 1

    return array1.tostring()


if __name__ == '__main__':
    str1 = "string-狂想写作本"
    str1 = "狂想写作本"
    print '原始列表：'
    print str1
    str1 = reverseUtf8(str1)
    print '排序后的列表：'
    print str1
    pass
