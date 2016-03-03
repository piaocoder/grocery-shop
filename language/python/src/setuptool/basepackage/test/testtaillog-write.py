#!/usr/bin/env python
#coding:utf-8
import time
import logging

filename = '/tmp/ioNotify.tmp'

_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
_LOGGER = logging.getLogger(__name__)


def _configure_logging():
    """_configure_logging"""
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)


def writeLog(filename):
    """writeLog:write msg to filename

    :param filename:
    """
    index = 0
    with open(filename, 'w+') as f:
        while 1:
            for i in range(10000):
                index += 1
                f.write('The {0} lines.\n'.format(index))
                # f.flush()
            if index % 20000 == 0:
                _LOGGER.info('Write msg and current index[%d]:', index)
            # time.sleep(0.5)
            if index > 1000000:
                break


if __name__ == '__main__':
    startTime = time.time()
    _configure_logging()
    filename = '/tmp/ioNotify.tmp'
    writeLog(filename)
    endTime = time.time()
    print 'Write-Running time:', endTime - startTime
