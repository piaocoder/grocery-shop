#!/usr/bin/python
# coding:utf-8

##
# @file testmullog.py
# @brief    test multiple log
# @author unlessbamboo
# @version 0.1
# @date 2016-01-23
import time
import multiprocessing

from basepackage.baselog import MultiLogHandle


def writeDebugProcess(logQueue, rootpath):
    """writeDebugProcess:Write debug msg process.

    :param logQueue:share queue
    """
    logObj = MultiLogHandle(logQueue, rootpath, "Debug-process")
    for i in range(10):
        msg = "Debug msg number({0}).".format(i)
        logObj.sendDebug(logObj.ERROR, msg)
        logObj.sendDebug(logObj.WARN, msg)
        logObj.sendDebug(logObj.INFO, msg)

    time.sleep(2)
    logObj.stop()


def writeErrorProcess(logQueue, rootpath):
    """writeErrorProcess:Write error msg process.

    :param logQueue:share queue
    """
    logObj = MultiLogHandle(logQueue, rootpath, "Error-process")
    for i in range(10):
        msg = "Error msg number({0}).".format(i)
        logObj.sendError(logObj.ERROR, msg)
        logObj.sendError(logObj.WARN, msg)
        logObj.sendError(logObj.INFO, msg)
    time.sleep(2)
    logObj.stop()


def mainProcess(rootpath):
    """mainProcess:main process"""
    logQueue = multiprocessing.Queue(-1)
    logObj = MultiLogHandle(logQueue, rootpath, "MainControl")

    debugProcess = multiprocessing.Process(target=writeDebugProcess,
            args=[logQueue, rootpath])
    errorProcess = multiprocessing.Process(target=writeErrorProcess,
            args=[logQueue, rootpath])
    debugProcess.start()
    errorProcess.start()

    while 1:
        try:
            if not logObj.receive():
                break
        except Exception, msg:
            print "Main control occur error, msg:{0}.".format(msg)
            break

    print "Main process quit."


if __name__ == '__main__':
    """main"""
    mainProcess("/data/logs/job")
