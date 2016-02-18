#!/usr/bin/env python
#coding:utf-8
##
# @file longestPalindrome.py
# @brief    Find longest palindrome string
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
       分析：
           元操作：判断字符串是否对称，O(n)
           方法1：
               对于任意/所有子字符串，逐个判断是否对称：
                   对于当前字符a和子字符串[a...end]，不断
                   循环，知道找到回文串，比较最大长度--O(n)
               结束，--O(n)
               总的性能消耗：O(n*n*n)
           方法2：
               从里向外判断回文，逐个判断：
                   对于当前字符a，逐层向外，获取最长回文
                   奇数比较(bab)、偶数比较(aa)，--O(n)
               结束，--O(n)
               总的性能消耗：O(n*n)
           方法3：
               manacher算法性能O(n)，以空间换时间


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


def lengthOfLongestSubstring(str1):
    """lengthOfLongestSubstring:
         find the length of the longest substring without repeating characters
        分析：（完全归纳法）
            1，使用hash，对每一个character进行index记录，从而保证
                不存在repeating characters
            2，假设l[i] = s[m...i]，其中m-i没有任何重复元素，最大长度为i-m+1
            3，判断s[i+1]:
                if s[i+1] not in Hashmap:
                    L[i+1] = s[m...i+1]
                else
                    m = max(m, hashmap[s[i+1]])
                    L[i+1] = s[m...i+1]
            4，返回最大的长度

    :param str1:
    """
    start = maxLength = 0
    usedChar = {}

    for i in range(len(str1)):
        if str1[i] in usedChar and start <= usedChar[str1[i]]:
            # 如果在首位和第5位发现a，则start++（在前面一个a的基础上面）
            start = usedChar[str1[i]] + 1
        else:
            maxLength = max(maxLength, i - start + 1)

        usedChar[str1[i]] = i

    return maxLength
