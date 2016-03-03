#coding:utf-8
'''
    cgitb模块用于日志信息调试，输出异常上下文所有相关变量的信息
'''
import cgitb
import sys
import traceback

def cgitbTest():
    cgitb.enable(format='text')
    list1 = [1, 2, 3]
    list2 = list1
    return 1/0

if __name__ == '__main__':
    '''main'''
    cgitbTest()
