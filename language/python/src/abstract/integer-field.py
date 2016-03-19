#!/usr/bin/env python
#coding:utf8
##
# @file integer-field.py
# @brief
#       1, 测试metaclass，将InterFiled转变为int类型
#       2，参考django中的Models，构造例子
# @author unlessbamboo
# @version 1.0
# @date 2016-03-19
import datetime


class IntegerFiled(object):
    """IntegerFiled"""
    def __init__(self, value, maxLength=4):
        """__init__

        :param value:
        :param maxLength:   整数最大位数
        """
        self.value = value[:maxLength]

    @property
    def value(self):
        """value"""
        return self.value


def with_metaclass(meta, base=object):
    """with_metaclass:对metaclass的封装，
        并返回元类对象，不是实例哦

    :param meta:
    :param base:
    """
    # type的__init__
    return meta("NewMetaBase", (base, ), {})


class ParentBase(type):
    """ParentBase"""
    def __new__(cls, name, base, attrb):
        """__new__

        :param name:
        :param base:
        :param attrb:
        """
        meta = attrb.pop("MetaV", None)
        newClass = super(
            ParentBase, cls).__new__(cls, name, base, attrb)
        # 获取类中的属性并赋值
        newClass.now = getattr(meta, "curTime", None)
        return newClass


class Parent(with_metaclass(ParentBase)):
    """Parent
        相当于：
            NewBase = ParentBase("NewMetaBase", (object,), {})
            class Parent(NewBase):
                pass
        相当于：
            class NewBase(object):
                __metaclass__ = ParentBase

            class Parent(NewBase):
                pass
        具体关于元类的解释见文档说明
    """
    pass

class Child(Parent):
    class MetaV:
        curTime = datetime.datetime.now()


cobj = Child()
print cobj.now
