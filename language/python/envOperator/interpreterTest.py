#!/usr/bin/env python
# coding:utf-8
##
# @file intepreterTest.py
# @brief    调用interpreter测试代码
# @author unlessbamboo
# @version 0.1
# @date 2016-01-29
import subprocess


def testInterpreter():
    """testInterpreter"""
    subprocess.call(['python', 'interpreter1.py'])
    subprocess.call(['python', 'interpreter2.py'])

if __name__ == '__main__':
    """main"""
    testInterpreter()
