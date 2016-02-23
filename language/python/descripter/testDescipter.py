#!/usr/bin/env python
# coding:utf-8
##
# @file testDescipter.py
# @brief    测试descipter的某些简单功能
#           1，descripter是属性、实例方法、静态方法、类方法、super的实现机制
# @author unlessbamboo
# @version 0.1
# @date 2016-01-29
import types


class TestDescipter(object):
    """TestDescipter"""
    def __init__(self, name):
        """__init__

        :param name: Object's name
        """
        self.name = name
        self._score = 0

    def testMethod(self):
        """testMethod"""
        print 'testMeothd:{0}'.format(self.name)

    def classMethod(TestDescipter):
        print 'classMethod!'

    ##
    # @brief    property:相当于声明了score属性，另外还有
    #               @property.getter和setter、deleter的声明
    #
    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        """score:使用property修饰

        :param value:
        """
        if not isinstance(value, int):
            raise
        self._score = value

    @score.getter
    def score(self):
        """score:使用property修饰"""
        self._score += 1
        return self._score


def methodTest():
    """methodTest:测试method是如何建立在func的基础之上的。
        前期知识：
            1,类中所有的函数都是non-data descripter，返回bound或者
            unbound方法
            2,方法调用
                aObj.f
                等价于：
                aObj.__dict__['fun1'].__get__(aObj, type(aObj))
                其中__get__方法定义如下：
                class Function:
                    def __get__(self, obj, objtype=None):
                        return types.MethodType(self, obj, objtype)
                其中self表示函数实例，MethodType返回方法类型，例如：
                    <bound method dict.items of {'age': 3}>
            3,func是一个non-data descripter
            4,方法的转换：
                普通方法：f(*args) ---> f(obj, *args)
                静态方法：f(*args) ---> f(*args)
                类方法：f(class, *args) --> f(type(obj), *args)

        检验步骤：
            1，输出方法对象本身，输出type(obj).__dict__['func'].__get__(obj, cls),
                比对结果
            2，输出类方法本身，输出Cls.__dict__['func'].__get__(None, cls),
                比对结果
            3，从而验证property的本质：
                调用方法，本身就是使用__get__调用；
                调用类方法，本身就是使用__get__调用呢，参数不同而已

    """
    test1 = TestDescipter('test1')
    print '对象调用(验证相等)-方法对象打印:{0}\n\t方法类型：{1}'.format(
        test1.testMethod,
        types.MethodType(test1.testMethod, test1, type(test1)))
    print '对象调用__dict__[...]输出:{0}'.format(
        TestDescipter.__dict__['testMethod'].__get__(test1, TestDescipter))
    print '类调用-方法对象打印:{0}'.format(
        TestDescipter.classMethod)
    print '类调用__dict__[...]输出:{0}'.format(
        TestDescipter.__dict__['classMethod'].__get__(None, TestDescipter))
    print '使用@property，逐渐递增score值：\n'
    print 'Score value:{0}, {1}, {2}, {3}'.format(
        test1.score, test1.score, test1.score, test1.score)

if __name__ == '__main__':
    """main"""
    methodTest()
