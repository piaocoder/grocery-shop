#!/usr/bin/env python
#coding:utf8
##
# @file testtail-epoll.py
# @brief    使用epoll来监听文件
# @author unlessbamboo
# @version 1.0
# @date 2016-02-16
import time
import logging
import select


_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
_LOGGER = logging.getLogger(__name__)


def _configure_logging():
    """_configure_logging"""
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)


def tail(filename):
    '''
    Tail thread which listen to nginx.log
    '''
    done = False
    fd = open(filename, 'r')
    index = 0

    while True:
        readable, writeable, exceptional = select.select([], [fd], [], 0)
        for fileno in writeable:
            if fileno != fd:
                break

            for i in range(len(fd.readlines())):
                index += 1
                if index % 30000 == 0:
                    _LOGGER.info('(Select)Read msg lines '
                                 'arrival a new point, Lines=[%d]',
                                 index)
            if index > 1000000:
                done = True
                break
        if done:
            break


if __name__ == '__main__':
    startTime = time.time()
    _configure_logging()
    filename = '/tmp/ioNotify.tmp'
    tail(filename)
    endTime = time.time()
    print '(Select)Read-Running time:', endTime - startTime
