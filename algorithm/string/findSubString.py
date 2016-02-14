#!/usr/bin/env python
#coding:utf-8


def lengthOfLongestSubstring(str1):
    """lengthOfLongestSubstring:
         find the length of the longest substring without repeating characters
        分析：
            1，使用hash，对每一个character进行index记录，从而保证
                不存在repeating characters
            2，假设l[i] = s[m...i]，其中m-i没有任何重复元素
            3，判断s[i+1]:
                if s[i+1] not in Hashmap:
                    L[i+1] = s[m...i+1]
                else
                    m = max(m, hashmap[s[i+1]])
                    L[i+1] = s[m...i+1]

    :param str1:
    """
