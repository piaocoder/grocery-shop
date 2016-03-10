#!/usr/bin/env python
#coding:utf8
##
# @file nextTest.py
# @brief    手动精确的控制迭代器的返回值，额外封装
# @author unlessbamboo
# @version 1.0
# @date 2016-03-10


def manualIter(filename):
    """manualIter

    :param filename:
    :NOTE: 文件对象本身就已经是一个可迭代对象了
    """
    with open(filename) as f:
        try:
            while 1:
                line = next(f)
                print line,
        except StopIteration:
            pass

if __name__ == '__main__':
    """main"""
    manualIter('/etc/passwd')
