#!/usr/bin/env python
#coding:utf-8
##
# @file testtaillog-old.py
# @brief    测试旧有的tail读取日志的速度
# @author unlessbamboo
# @version 1.0
# @date 2016-02-16
import os
import logging
import time

_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
_LOGGER = logging.getLogger(__name__)


def _configure_logging():
    """_configure_logging"""
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)


def tailImpl(fd, filename):
    '''tail thread impl'''
    line = fd.readline()
    if not line:
        curPos = fd.tell()
        curFileSize = os.path.getsize(filename)
        if curFileSize < curPos / 100:
            fd.seek(0)
        time.sleep(0.5)
        return False
    else:
        return True


def tail(filename):
    '''
    Tail thread which listen to nginx.log
    '''
    fd = open(filename, 'r')
    # s = os.path.getsize(filename)
    # fd.seek(s)
    index = 0
    while True:
        if tailImpl(fd, filename):
            index += 1
        if index % 30000 == 0:
            _LOGGER.info('(Old)Read msg lines '
                         'arrival a new point, Lines=[%d]',
                         index)
        if index > 1000000:
            break


if __name__ == '__main__':
    startTime = time.time()
    _configure_logging()
    filename = '/tmp/ioNotify.tmp'
    tail(filename)
    endTime = time.time()
    print '(old)Read-Running time:', endTime - startTime
