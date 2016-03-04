#!/usr/bin/env python
# coding:utf-8
##
# @file intepreterTest.py
# @brief    调用interpreter测试代码
#           原因：
#               vim在双版本的python下工作不正常，考虑到可能
#                   是解释器的原因，结果，哎
#           PS：其实，一般情况下env python和/usr/bin/python都是
#               同一个解释器吧，多版本的python的路径一般都不是
#               默认路径，无语
# @author unlessbamboo
# @version 0.1
# @date 2016-01-29
import subprocess


def testInterpreter():
    """testInterpreter"""
    subprocess.call(['python', 'env-test.py'])
    subprocess.call(['python', 'bin-test.py'])

if __name__ == '__main__':
    """main"""
    testInterpreter()
