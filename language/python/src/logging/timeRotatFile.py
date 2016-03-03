#!/usr/bin/python
#coding:utf-8
import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler

def testRotateSecond():
    '''test TimedRotatingFileHandler
       Impl:
       1，首先创建logfile日志文件
       2，一旦运行时间超过制定的时间，加上后缀文件名
    '''
    logHandler = TimedRotatingFileHandler("logfile", when="M")
    logHandler.suffix = "%Y-%m-%d.%M-%S.log"

    logFormatter = logging.Formatter('%(asctime)s %(message)s')
    logHandler.setFormatter(logFormatter)
    logger = logging.getLogger( 'MyLogger' )
    logger.addHandler( logHandler )
    logger.setLevel( logging.INFO )
    
    for k in range(5):
        logger.info("line %d"%k)
        time.sleep(1)

if __name__ == '__main__':
    '''main'''
    testRotateSecond()
