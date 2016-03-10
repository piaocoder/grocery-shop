#!/usr/bin/env python
#coding:utf8
##
# @file wrap-iter-test.py
# @brief    对已有的迭代器进行封装（统称为代理），对外表示
#           我就是老大，至于具体的，呵呵
# @author unlessbamboo
# @version 1.0
# @date 2016-03-10


class Node(object):
    """Node"""
    def __init__(self, value):
        """__init__:self._children是被代理人

        :param value:
        """
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({0})'.format(self._value)

    def add_child(self, node):
        """add_child

        :param node:   new value
        """
        self._children.append(node)

    def __iter__(self):
        """__iter__:该方法返回一个实现了__next__的迭代器对象"""
        return iter(self._children)

if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    # Outputs Node(1), Node(2)
    for ch in root:
        print(ch)
