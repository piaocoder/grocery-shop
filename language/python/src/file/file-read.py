#!/usr/bin/python
#coding:utf-8
import os
import sys
import time
import traceback

sys.path.append(os.getcwd()+"/../")

from basepackage.baselog import globalLog

def exceptionCatch(func,*args,**kw):
    def innerFunc(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception,msg:
            traceList = traceback.extract_tb(sys.exc_traceback)
            for (file,lineno, funcname,text) in traceList:
                globalLog.getError().log(globalLog.ERROR, \
                        "Occur error, func:%s,lineno:%s, msg:%s"%(funcname, lineno, msg))
            return None
    return innerFunc

#@exceptionCatch
def readNotExistFile(filename):
    '''
    Read file from fd, and file was remove at any one time.
    '''
    fd = open(filename, "r")
    fino = os.stat(filename).st_ino
    while True:
        try:
            tempio = os.stat(filename).st_ino
            if fino != tempio:
                print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                fd.close()
                fd = open(filename, 'r')
            print fd.readline()
            time.sleep(5)
        except (IOError,OSError),msg:
            print 'IOerror, msg:%s'%msg
            time.sleep(2)

def readFileByIter(filename):
    '''
    文件对象本身就是一个迭代器，可以使用for来进行迭代
    '''
    with open(filename, 'r') as f:
        for line in f:
            print line

if __name__ == '__main__':
    '''main'''
    #readNotExistFile('./test.log')
    readFileByIter('./boot.log')
