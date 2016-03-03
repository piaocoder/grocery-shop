#!/usr/bin/env python
#coding:utf-8
import time
import logging

from basepackage.taillog import TailLogHandler

_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
_LOGGER = logging.getLogger(__name__)


def _configure_logging():
    """_configure_logging"""
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)


class TestTailLogHandler(object):
    def __init__(self, filename):
        """__init__

        :param filename:monitor filename
        """
        self.filename = filename
        self.index = 0

    def readLog(self, values):
        """readLog:handle log file's functions.
            读取日志中的多行字符串数据，遍历即可

        :param values:string list
        """
        for value in values:
            self.index += 1
            if self.index % 30000 == 0:
                _LOGGER.info('Read msg Lines=[%d]', self.index)

        if self.index > 1000000:
            self.tailObj.stopNotify()

    def run(self):
        """run"""
        self.tailObj = TailLogHandler(self.filename, self.readLog)
        self.tailObj.run()


if __name__ == '__main__':
    startTime = time.time()

    _configure_logging()
    testObj = TestTailLogHandler('/tmp/ioNotify.tmp')
    testObj.run()

    endTime = time.time()
    print '(pyinotify)Read-Running time:', endTime - startTime
