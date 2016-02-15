#!/usr/bin/env python
#coding:utf-8
##
# @file longestPalindrome.py
# @brief    Find longest palindrome string
#       分析：
#           元操作：判断字符串是否对称，O(n)
#           方法1：
#               对于任意/所有子字符串，逐个判断是否对称：
#                   对于当前字符a和子字符串[a...end]，不断
#                   循环，知道找到回文串，比较最大长度--O(n)
#               结束，--O(n)
#               总的性能消耗：O(n*n*n)
#           方法2：
#               从里向外判断回文，逐个判断：
#                   对于当前字符a，逐层向外，获取最长回文
#                   奇数比较(bab)、偶数比较(aa)，--O(n)
#               结束，--O(n)
#               总的性能消耗：O(n*n)
#           方法3：
#               manacher算法性能O(n)，以空间换时间
#
# @author unlessbamboo
# @version 1.0
# @date 2016-02-15


def secondHelper(str1, left, right):
    """secondHelper:Find a palindrome string from one point

    :param str1:source string
    :param left:
    :param right:
    """
    lenStr1 = len(str1)
    while left >= 0 and right <= lenStr1 and str1[left] == str1[right]:
        left -= 1
        right += 1

    return str1[left + 1:right]


def longestPalindromeSecond(str1):
    """longestPalindromeSecond:方法2

    :param str1:Source string
    """
    res = ""

    for i in xrange(len(str1)):
        # odd case
        tmp = secondHelper(str1, i, i)
        if len(tmp) > len(res):
            res = tmp

        # even case
        tmp = secondHelper(str1, i, i + 1)
        if len(tmp) > len(res):
            res = tmp

    return res
