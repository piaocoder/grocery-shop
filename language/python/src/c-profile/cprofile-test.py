#!/usr/bin/env python
#coding:utf8
import cProfile


def sum_num(max_num):
    """sum_num:累加

    :param max_num:最大值
    """
    total = 0
    for i in range(max_num):
        total += i
    return total


def test():
    """test"""
    total = 0
    for i in range(40000):
        total += i

    t1 = sum_num(100000)
    print "次数{0}，测试结束.".format(t1)
    t2 = sum_num(400000)
    print "次数{0}，测试结束.".format(t2)

if __name__ == "__main__":
    '''Use cProfile module test program performance.'''
    # 所有的性能统计结果都会记录到result.out中
    cProfile.run('test()', filename="result.out")
