#coding:utf-job
'''
    全局异常捕捉器
'''
import sys
import traceback

def foo(exctype, value, tb):
    print 'My Error Information'
    print 'Type:', exctype
    print 'Value:', value
    print 'Traceback:', tb

def testExcept():
    return 1/0

if __name__ == '__main__':
    '''main'''
    # 对全局异常捕捉函数的override
    sys.excepthook = foo
    testExcept()

