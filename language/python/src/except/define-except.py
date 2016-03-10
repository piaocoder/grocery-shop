#!/usr/bin/env python
#coding:utf8
##
# @file define-except.py
# @brief    自定义异常
#           通用做法：
#               1，定义基类
#               2，各个不同功能类抛出不同异常
# @author unlessbamboo
# @version 1.0
# @date 2016-03-10


class BaseError(Exception):
    """BaseError"""
    pass


class InputError(BaseError):
    """InputError"""
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    def __str__(self):
        """__str__"""
        return repr("Expression:{0}, message:{1}".format(
            self.expression, self.message))


if __name__ == '__main__':
    try:
        raise InputError('mylove', 'not found this file.')
    except Exception, msg:
        print msg
