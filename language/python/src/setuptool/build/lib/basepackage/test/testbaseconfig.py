#!/usr/bin/python
# coding:utf-8

##
# @file testbaseconfig.py
# @brief    test baseconfig.py
# @author unlessbamboo
# @version 0.1
# @date 2016-01-23
import os
import unittest
import Queue

from basepackage.baseconfig import BaseConfig
from basepackage.baselog import MultiLogHandle

class TestBaseConfig(unittest.TestCase):
    """TestBaseConfig:test BaseConfig"""
    def setUp(self):
        """set up"""
        self.baseConfObj = BaseConfig()
        self.logQueue = Queue.Queue(-1)
        processName = 'testBaseConfig'
        rootpath = "/data/logs/test"
        self.globalLog = MultiLogHandle(self.logQueue,
                rootpath, processName, "testBase")

    def testJavaTrace(self):
        """testJavaTrace"""
        self.assertEqual("tracing.log",
                os.path.basename(self.baseConfObj.getJavaTrace()))

    def testPid(self):
        """testPid"""
        self.assertEqual("aggregate.pid",
                os.path.basename(self.baseConfObj.getPidFile("aggregate")))
        self.assertEqual("dubbo.pid",
                os.path.basename(self.baseConfObj.getPidFile("dubbo")))

    def testKafkaConf(self):
        """testKafkaConf"""
        self.assertEqual("kafka.ini",
                os.path.basename(self.baseConfObj.getKafkaConf()))


if __name__ == '__main__':
    unittest.main()
