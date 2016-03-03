#coding:utf-8
'''
    try/finally测试
'''
import os
import sys

def exitFinally():
    '''
      1, sys.exit(0)在python中抛出SystemExit异常，所以
        任何finally语句仍旧会执行，例子
      2, os._exit(0)则会直接执行退出函数
    '''
    try:
        sys.exit(0)
    except SystemExit, msg:
        print 'Caught systemexit, msg:%s'%msg
    finally:
        print 'Finally execute. Well coll!'

    try:
        os._exit(0)
    except SystemExit, msg:
        print '1Caught systemexit, msg:%s'%msg
    finally:
        print '1Finally execute. Well coll!'

if __name__ == '__main__':
    '''main'''
    exitFinally()
