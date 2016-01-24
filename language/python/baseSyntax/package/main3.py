#!/usr/bin/python
#coding:utf-job
'''
    尝试以python -m module来执行python模块，并非以脚本形式执行，之后分别打印输出
'''
from sub_package import string

if __name__ == '__main__' and __package__ is None:
    print '以python module.py形式执行程序'
    print '__name__:', __name__
    print '__package__:', __package__
else:
    print '以python -m module形式执行程序'
    print '__name__:', __name__
    print '__package__:', __package__
