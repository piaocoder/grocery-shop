#!/usr/bin/env python
#coding:utf-8
import time

from basepackage.basekafka import BaseKafkaConsumer
from basepackage.baselog import SignalLogHandle


class TestConsumer(object):
    """TestConsumer"""
    def __init__(self):
        """__init__"""
        self.logObj = SignalLogHandle("/data/logs/test/")
        self.baseKafkaConsumer = BaseKafkaConsumer(
            ['devops-dev1:9090', 'devops-dev1:9091'],
            ['JOB_TEST'], self.logObj)

    def testOneMsgConsumer(self):
        """testOneMsgConsumer"""
        startTime = time.time()
        while True:
            msgs = self.baseKafkaConsumer.get_message()
            if not msgs:
                continue
            break
        endTime = time.time()
        print 'Send a single message for {0} second'.format(
            endTime - startTime)

    def testMultiConsumer(self, num):
        """testMultiConsumer

        :param num:
        """
        index = 1
        startTime = 0
        while True:
            msgInterator = self.baseKafkaConsumer.get_message()
            if not msgInterator:
                # time.sleep(0.5)
                continue

            for msg in msgInterator:
                if index == 1:
                    startTime = time.time()
                index += 1
            if index % 200 == 0:
                print 'Current index:', index
            if index > num:
                break

        endTime = time.time()
        print 'Send {0} messages for {1} second'.format(
            num, endTime - startTime)


if __name__ == '__main__':
    '''main'''
    testObj = TestConsumer()
    # testObj.testOneMsgConsumer()
    testObj.testMultiConsumer(100000)
