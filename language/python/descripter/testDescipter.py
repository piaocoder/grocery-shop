#!/usr/bin/env python
# coding:utf-8
##
# @file testDescipter.py
# @brief    测试descipter的某些简单功能
# @author unlessbamboo
# @version 0.1
# @date 2016-01-29


class TestDescipter(object):
    """TestDescipter"""
    def __init__(self, name):
        """__init__

        :param name: Object's name
        """
        self.name = name

    def testMethod(self):
        """testMethod"""
        print 'testMeothd:{0}'.format(self.name)


def methodTest():
    """methodTest:测试method是如何建立在func的基础之上的。
        1，检测method是否是一个函数descipter
        2，
    """
    test1 = TestDescipter('test1')
    print 'Test1 info:{0}'.format(test1.testMethod)
    print 'Test1 info from __dict__[...]:{0}'.format(
        TestDescipter.__dict__['testMethod'])

if __name__ == '__main__':
    """main"""
    methodTest()
