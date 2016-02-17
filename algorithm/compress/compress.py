#!/usr/bin/env python
#coding:utf-8
##
# @file compress.py
# @brief    字符串压缩算法介绍（不单独放在string中了，翅膀硬了）
# @author unlessbamboo
# @version 1.0
# @date 2016-02-17


def compressHash(str1):
    """compressHash:字典算法
        介绍：
            将高频词汇或者词汇组合hash，并以较小的特殊代码替换，
            从而达到压缩的目的
        使用场景
            专有名词较多的应用场景，例如某些游戏
        例子：
            00 == Chinese
            01 == China
            02 == people
            则压缩结果为：
                I am a 00 02, I am from 01. So what?

    :param str1:
    """
    pass


if __name__ == '__main__':
    str1 = "I am a Chinese people, I am from China. So what?"
    print '原始列表：'
    print str1
    print '排序后的列表：'
    print str1
