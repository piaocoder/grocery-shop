#!/usr/bin/evn python
#coding:utf-8
##
# @file taillog.py
# @brief    根据pyinotify模块读取日志文件并返回读取的日志文件内容
# @author unlessbamboo
# @version 1.0
# @date 2016-02-14
import sys
import pyinotify


class EventHandler(pyinotify.ProcessEvent):
    def my_init(self, myfd=sys.stdout, callback=None):
        """my_init

        :param myfd:注意，传入myfd仅仅是为了读取数据，和pyinotify监控
                    filename本身没有关系
        :param callback:
        """
        self._myfd = myfd
        self._callback = callback

    def process_IN_MODIFY(self, event):
        self._data = self._myfd.readlines()
        values_len = len(self._data)
        if values_len and self._callback:
            self._callback(self._data)


class TailLogHandler(object):
    def __init__(self, filename, callback):
        """__init__:

        :param filename:monitor filename
        :param callback:callback function
        """
        self.filename = filename
        self.callback = callback
        self.fd = None
        self.wdd = None
        self.wm = pyinotify.WatchManager()
        self.mask = pyinotify.IN_MODIFY
        self.notifier = None
        self.done = False

    def closeFile(self):
        """closeFile"""
        self.fd.close()
        self.fd = None

    def openFile(self):
        """openFile"""
        self.fd = open(self.filename, 'r') if not self.fd else self.fd

    def createNewNotify(self, filename):
        """createNewNotify:create new watch

        :param filename:
        """
        if self.wdd and self.wdd[filename] > 0:
            # self.wm.rm_watch(self.wdd[filename], self.mask, rec=True)
            self.wm.rm_watch(self.wdd[filename], rec=True)

        self.stopNotify()
        self.done = False
        self.openFile()

        self.wdd = self.wm.add_watch(self.filename, self.mask, rec=True)
        my_handler = EventHandler(myfd=self.fd, callback=self.callback)
        self.notifier = pyinotify.Notifier(self.wm, my_handler)

    def stopNotify(self):
        """stopNotify"""
        # if self.wdd and self.wdd[self.filename] > 0:
            # self.wm.rm_watch(self.wdd[self.filename], rec=True)
            # self.wm.rm_watch(self.wdd[self.filename], self.mask, rec=True)

        #if self.notifier:
        #    self.notifier.stop()

        self.done = True

    def run(self):
        """run:loop"""
        self.createNewNotify(self.filename)
        while True:
            self.notifier.process_events()
            if not self.done and self.notifier.check_events():
                self.notifier.read_events()
            elif self.done:
                break
