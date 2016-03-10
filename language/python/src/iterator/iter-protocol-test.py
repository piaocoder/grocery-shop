#!/usr/bin/env python
#coding:utf8
##
# @file iter-protocol-test.py
# @brief    实现了迭代器协议，真正实现底层操作，对比生成器方法
#           该方式非常麻烦和复杂
#       1，步骤：
#           1）定义__iter__方法，返回本身（即返回一个定义了next方法的对象）
#           2）定义__next__方法或者next方法，返回下一个
# @author unlessbamboo
# @version 1.0
# @date 2016-03-10


class Count(object):
    """Count:从1数到10"""
    def __init__(self, max):
        """__init__

        :param max: 最大数
        """
        # super(Count, self).__init__()
        self.max = max

    def __iter__(self):
        """__iter__"""
        # 每次迭代开始时进行相关变量的初始化操作
        self.start = 0
        # 返回自身，从这里就可以看出迭代器自身为何
        # 节省内存消耗，仅仅返回一个对象，使用“懒惰属性”
        # 用的时候采取拿数据，不用就一直开着指针
        return self

    def next(self):
        """__next__

        @Note:在python3中，使用__next__替换next方法
        """
        if self.start >= self.max:
            raise StopIteration

        value = self.start
        self.start += 1
        return value

if __name__ == '__main__':
    """main"""
    cObj = Count(100)
    for num in cObj:
        print num
