#!/usr/bin/env python
#coding:utf8
##
# @file iter-reverse-test.py
# @brief    反向迭代操作，必须一开始就知道迭代的数量哦
# @author unlessbamboo
# @version 1.0
# @date 2016-03-10


class Countdown(object):
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        """__iter__：利用生成器来进行迭代操作，无需返回自身了"""
        n = self.start
        while n > 0:
            yield n
            n -= 1

    def __reversed__(self):
        """__reversed__：和__iter__就是一个两极啊"""
        n = 1
        while n <= self.start:
            yield n
            n += 1

if __name__ == '__main__':
    for rr in reversed(Countdown(30)):
        print(rr)
    for rr in Countdown(30):
        print(rr)

    cObj = Countdown(30)
    next(cObj)
