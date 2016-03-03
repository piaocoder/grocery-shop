#coding:utf-8
'''
    测试脚本所在路径的测试：
        1，getcwd和sys.path、__file__区别
        2，理解工作目录和脚本路径的区别
        3，利用chdir改变当前工作目录
'''
import os
import sys

def test1():
    '''test1'''
    print 'getcwd():', os.getcwd()
    print 'sys.path[0]:', sys.path[0]
    print '__file__:', os.path.realpath(__file__)
    print 'dirname(__file__):', os.path.normpath(os.path.dirname(__file__))
    print

def test3():
    '''test3'''
    print 'getcwd():', os.getcwd()
    os.chdir('/tmp/')
    print 'change directory.............'
    print 'Now, getcwd():', os.getcwd()
    print


if __name__ == '__main__':
    '''main'''
    print '==============================test1==========================='
    test1()
    print '==============================test3==========================='
    test3()
    
