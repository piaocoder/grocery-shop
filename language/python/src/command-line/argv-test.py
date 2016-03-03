#!/usr/bin/env python
#coding:utf-8
##
# @file argv-test.py
# @brief
#           最底层的命令行解析，其他模块应该都是对其的封装
# @author unlessbamboo
# @version 1.0
# @date 2016-03-03

import sys


def testSys():
    """testSys"""
    for arg in sys.argv[1:]:
        print (arg)


if __name__ == '__main__':
    testSys()
