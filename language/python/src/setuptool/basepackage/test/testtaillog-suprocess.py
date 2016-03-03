#!/usr/bin/env python
#coding:utf-8
##
# @file testtaillog-epoll.py
# @brief    使用epoll来监听日志文件（阻塞或者非阻塞）
# @author unlessbamboo
# @version 1.0
# @date 2016-02-16
import time
import logging
import select
import subprocess

_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
_LOGGER = logging.getLogger(__name__)


def _configure_logging():
    """_configure_logging"""
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)


def readLog(filename):
    """readLog:

    :param filename:
    """
    f = subprocess.Popen(['tail', '-F', filename],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = select.epoll()
    p.register(f.stdout)
    index = 0

    while True:
        if p.poll(1):
            index += 1
        if index % 3000000 == 0:
            _LOGGER.info('(subprocess)Read msg lines '
                         'arrival a new point, Lines=[%d]',
                         index)
        if index > 100000000:
            break


if __name__ == '__main__':
    startTime = time.time()
    _configure_logging()
    filename = '/tmp/ioNotify.tmp'
    readLog(filename)
    endTime = time.time()
    print '(Subprocess)Read-Running time:', endTime - startTime
