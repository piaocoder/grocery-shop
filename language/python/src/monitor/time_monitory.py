#!/usr/bin/env python
# coding:utf-8
"""
    时间处理测试函数
"""
import datetime
import timeit
import requests


def with_indexing(tstr):
    """with_indexing:字符串转为datetime对象

    :param tstr:
    """
    return datetime.datetime(*map(
        int, [tstr[:4], tstr[5:7], tstr[8:10],
              tstr[11:13], tstr[14:16], tstr[17:]]))


def with_index_reverse(nowtime):
    """with_index_reverse:datetime转为字符串

    :param nowtime:
    """
    return "%4s/%2s/%2s:%2s:%2s:%2s" % (
        nowtime.year, nowtime.month, nowtime.day,
        nowtime.hour, nowtime.minute, nowtime.second)


import sys
CURRENT_TIME = datetime.datetime.now()


def timeit_test():
    '''使用timeit来测试strptime的时间延迟.'''
    time1 = timeit.timeit(
        'datetime.strptime("2006/01/02:15:04:05", "%Y/%m/%d:%H:%M:%S")',
        'from datetime import datetime', number=1000000)
    print("Strptime:", time1)

    time2 = timeit.timeit(
        'with_indexing("2016/01/02:15:04:05")',
        'from __main__ import with_indexing', number=1000000)
    print('Slice:', time2)

    time3 = timeit.timeit(
        'datetime.strftime(now, "%Y/%m/%d:%H:%M:%S")',
        'from datetime import datetime;from __main__ import now',
        number=5000000)
    print('Strftime:', time3)

    time4 = timeit.timeit(
        'with_index_reverse(now)',
        'from __main__ import with_index_reverse, now',
        number=5000000)
    print('String:', time4)


timeit_test()
