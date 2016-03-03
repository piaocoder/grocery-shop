#!/usr/bin/env python
#coding:utf-8
import time
import base64
import datetime

from basepackage.basekafka import BaseKafkaProducer
from basepackage.baselog import SignalLogHandle


class TestProducer(object):
    """TestProducer"""
    def __init__(self):
        """__init__"""
        self.message = 'This is a test case, index is '
        self.logObj = SignalLogHandle("/data/logs/test/")
        self.baseKafkaProducer = BaseKafkaProducer(
            ['devops-dev1:9090', 'devops-dev1:9091'],
            'JOB_TEST', self.logObj)

    def testOneMsgProducer(self):
        """testOneMsgProducer:
            测试单条数据发送是否成功，如果成功记录发送时间，
            用于后期的延迟判断
        """
        msg = self.message + 'single(0).'
        startTime = time.time()
        self.baseKafkaProducer.send_message("keys", msg)
        endTime = time.time()
        print 'Send a single message for {0} second'.format(
            endTime - startTime)

    def testMultiReplicaProducer(self, num):
        """testMultiReplicaProducer：发送多条数据并记录时间延迟

        :param num: 发送的消息条数
        """
        message = 'This is a test case, index is multiple({0})'
        index = 0
        startTime = time.time()
        while True:
            msg = message.format(index)
            index += 1
            self.baseKafkaProducer.send_message("keys", msg)
            if index % 200 == 0:
                print 'Current index:', index
            if index > num:
                break
        endTime = time.time()
        print 'Send {0} messages for {1} second'.format(
            num, endTime - startTime)

    def basicConstructor(self, data):
        """basicConstructor

        :param data:
        """
        if not isinstance(data, dict):
            return

        jsonrows = {
            "Row": [
                {},
            ],
        }
        rows = jsonrows['Row']
        rowkey = base64.b64encode(
            self.hostname + ":" +
            datetime.now().strftime('%Y%m%d%H%M'))
        cell = []
        for key in data.keys():
            for kkey in data[key].keys():
                cell.append({
                    "column":   base64.b64encode(key + ":" + kkey),
                    "$":        base64.b64encode(data[key][kkey])})
        od = dict([("key", rowkey), ("Cell", cell)])
        rows.append(od)
        return rowkey, jsonrows


if __name__ == '__main__':
    '''main'''
    testObj = TestProducer()
    #testObj.testOneMsgProducer()
    testObj.testMultiReplicaProducer(100000)
