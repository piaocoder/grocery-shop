#!/usr/bin/python
#coding:utf-job
import sys
import traceback
import logging

def exceptionCatch(func,*args,**kw):
    '''
        exc_type是抛出的异常类型
        exc_value是异常值信息
        exc_tb是一个traceback对象，替换以前的sys.exc_traceback值
    '''
    def innerFunc(*args,**kw):        
        try:
            return func(*args,**kw)
        except Exception,msg:
            # 获取栈信息
            exc_type, exc_value, exc_tb = sys.exc_info()
            logging.error("参数：{0}-{1}".format(args, kw))
            logging.error("异常类型:%s"%sys.exc_type)
            logging.error("异常值:%s"%sys.exc_value)
            traceList = traceback.extract_tb(exc_tb)
            for file,lineno,function,text in traceList:
                logInfo = "%s\t%s\t%s\t%s\t%s"%(
                            file,lineno,function,
                            text, msg)
                logging.error(logInfo)
            return "error"
    return innerFunc


class TestExceptCatch(object):
    def __init__(self):
        self.mystring = 'This is test for except Catch'

    @exceptionCatch
    def raiseExcept(self, msg, name='bifeng', age='26'):
        '''raise except'''
        raise Exception('哇哈哈')

if __name__ == '__main__':
    '''main'''
    import os
    print __file__
    print os.path.splitext(os.path.basename(__file__))
    testObject = TestExceptCatch()
    testObject.raiseExcept('Perfect')
