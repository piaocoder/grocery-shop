#!/usr/bin/env python
#coding:utf8
##
# @file argparse-test.py
# @brief    更加格式化，高层的封装策略，模式工厂
# @author unlessbamboo
# @version 1.0
# @date 2016-03-03
import argparse


class BambooAction(argparse.Action):
    """BambooAction"""
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        """__init__

        :param option_strings: 选项字符串，例如--number，此时没有值哦
        :param dest:    选项值存储的变量名，默认为number
        :param nargs:   对于自定义类，一般不设置多个nargs变量
        :param **kwargs: 选项参数的字典信息（类型，帮助信息，等等）
        """
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(BambooAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """__call__

        :param parser:      ArgumentParser实例
        :param namespace:   类实例，用于保存属性值并返回
        :param values:      命令行参数的值
        :param option_string:   命令行中的选项字符串，注意该值和__init__中
                                的区别
        """
        print "%r %r %r %r" % (namespace, values, option_string, self.dest)
        setattr(namespace, self.dest, values + 1)


def simpleTest():
    """simpleTest"""
    # create argument
    parser = argparse.ArgumentParser(
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Argparse simple test.")

    # add argument infomation
    parser.add_argument(
        "--number",  # 可选参数
        action=BambooAction,
        type=int,
        help="A number for the accumlator")

    parser.add_argument(
        "--valuelist",  # 可选参数
        type=int,
        nargs=3,  # 指定3个
        help="A number list for the accumlator")

    # parser.add_argument(
        # "bamboo",  # 位置参数，必须存在一个整数或者多个
        # action="append",  # 动作，一般是自定义处理回调函数
        # nargs="+",  # 参数个数
        # type=int)

    # ArgumentParser通过parse_args方法，默认参数为sys.argv
    # 检查命令行，将匹配的参数转为相应的类型（例如int），
    # 最后调用对应的action
    rst = parser.parse_args()

    # 输出
    print rst


if __name__ == '__main__':
    """main"""
    simpleTest()
