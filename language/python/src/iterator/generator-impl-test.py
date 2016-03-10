#!/usr/bin/env python
#coding:utf8
##
# @file generator-impl-test.py
# @brief    实现一个自定义的迭代方式，而不是通过__iter__和
#           __next__来进行构造
#       注意：
#           使用yields语法时，返回的并不是一个iterator对象，
#           不能使用next(obj)语法；
#           如果要使用，需要使用iter进行封装：
#               iobj = iter(obj)
#               next(iobj)
# @author unlessbamboo
# @version 1.0
# @date 2016-03-10


def frange(start, stop, increment):
    """frange：
        利用生成器来实现迭代模式，可以具体比较迭代器的底层
        实现构造代码，见iter-protocol-test.py文件

    :param start:
    :param stop:
    :param increment:
    """
    x = start
    while x < stop:
        yield x
        x += increment

if __name__ == '__main__':
    """main"""
    for num in frange(0, 4, 0.3):
        print num
