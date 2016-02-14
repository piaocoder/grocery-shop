#!/usr/bin/env python
#coding:utf-8
##
# @file ioNotify.py
# @brief    测试ionotify模块的功能
# @author unlessbamboo
# @version 1.0
# @date 2016-02-14
import os
import sys
import logging
import pyinotify

_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

_LOGGER = logging.getLogger(__name__)


def _configure_logging():
    """_configure_logging"""
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)


f1 = open('/tmp/iotest', 'w')


class EventHandler(pyinotify.ProcessEvent):
    def my_init(self, myfd=sys.stdout):
        self._myfd = myfd
        self._index = 0

    def process_IN_MODIFY(self, event):
        values_len = len(self._myfd.readlines())
        if values_len:
            self._index += values_len
            _LOGGER.info('Path=[%s], Lines=[%d]', event.pathname, self._index)


def _main():
    """_main"""
    filename = '/tmp/ioNotify.tmp'
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            pass

    with open(filename, 'r') as fd:
        wm = pyinotify.WatchManager()
        mask = pyinotify.IN_MODIFY
        wm.add_watch(filename, mask, rec=True)
        my_handler = EventHandler(myfd=fd)
        notifier = pyinotify.Notifier(wm, my_handler)
        notifier.loop()
        f1.close()

if __name__ == '__main__':
    _configure_logging()
    _main()
