#!/usr/bin/env python
#coding:utf8
##
# @file argparse-test.py
# @brief    更加格式化，高层的封装策略，模式工厂
# @author unlessbamboo
# @version 1.0
# @date 2016-03-03
import sys
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


def defineActionTest():
    """defineActionTest"""
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

    # ArgumentParser通过parse_args方法，默认参数为sys.argv
    # 检查命令行，将匹配的参数转为相应的类型（例如int），
    # 最后调用对应的action
    rst = parser.parse_args()

    # 输出
    print rst


def descriptionTest():
    """descriptionTest"""
    print "=================={0}=================".format(
        sys._getframe().f_code.co_name)
    parser = argparse.ArgumentParser(description="This is description")
    # 在获取帮助信息后，会自动退出哦，哇哦
    parser.parse_args("-h".split())


def epilogTest():
    """epilogTest"""
    print "=================={0}=================".format(
        sys._getframe().f_code.co_name)
    parser = argparse.ArgumentParser(
        epilog="This is epilog message.",
    )
    parser.parse_args("-h".split())


def parentTest():
    """parentTest"""
    print "=================={0}=================".format(
        sys._getframe().f_code.co_name)
    parent_parser = argparse.ArgumentParser(
        add_help=False,
        epilog="I am a parent.",
        description="So what?",)
    parent_parser.add_argument("--password", type=str)
    parent_parser.add_argument("--user", type=str)

    parser = argparse.ArgumentParser(
        epilog="I am a children.",
        parents=[parent_parser],)
    parser.add_argument("--number", type=int)

    # 可以发现，父类的所有解析器设置在引用方都无效
    # 可以发现2，父类的选项参数在引用方有效，从而达到共享目的
    parser.parse_args("-h".split())


def argumentGroupTest():
    """argumentGroupTest"""
    print "=================={0}=================".format(
        sys._getframe().f_code.co_name)
    parser = argparse.ArgumentParser(
        description="This is argument group test.")

    parser_group1 = parser.add_argument_group("crypt command")
    parser_group1.add_argument("--user", help="username")
    parser_group1.add_argument("--passwd", help="password")

    parser_group2 = parser.add_argument_group("other command")
    parser_group2.add_argument("--age", help="ages")
    parser_group2.add_argument("--number", help="number")

    parser.parse_args("-h".split())


def subprocessTest():
    """subprocessTest"""
    print "=================={0}=================".format(
        sys._getframe().f_code.co_name)
    parser = argparse.ArgumentParser(
        description="This is main parsers")

    subparsers = parser.add_subparsers(help="Sub-command")

    # create first sub parser
    parser_first = subparsers.add_parser('first', help='first help')
    parser_first.add_argument('--name', help='name')
    parser_first.add_argument('--age', help='age')

    # create second sub parser
    parser_second = subparsers.add_parser('second', help='second help')
    parser_second.add_argument('--number', help='number')
    parser_second.add_argument('--weight', help='weight')

    parser.parse_args()


def conflictTest():
    """conflictTest"""
    print "=================={0}=================".format(
        sys._getframe().f_code.co_name)
    parser = argparse.ArgumentParser(
        conflict_handler="resolve",
        description="This is conflict test")

    # 后面的长选项会覆盖前面的长选项
    parser.add_argument("-t", "--test", help="test1")
    parser.add_argument("--test", help="test2")

    parser.parse_args("-h".split())


def prefixCharsTest():
    """prefixCharsTest"""
    print "=================={0}=================".format(
        sys._getframe().f_code.co_name)
    parser = argparse.ArgumentParser(
        prefix_chars="-+",
        description="This is prefix chars test")

    parser.add_argument("++value", dest="boolvalue",
                        action="store_false",
                        default=None)
    parser.add_argument("--value", dest="boolvalue",
                        action="store_true",
                        default=None)

    args = parser.parse_args("++value".split())
    print "++value的输出：", args
    args = parser.parse_args("--value".split())
    print "--value的输出：", args
    print "================end================"


def constTest():
    """constTest"""
    print "=================={0}=================".format(
        sys._getframe().f_code.co_name)
    parser = argparse.ArgumentParser(
        description="This is const test.")

    parser.add_argument("--value", action="store_const", const=42, default=0)

    args = parser.parse_args("".split())
    print "无任何参数时输出为：", args
    args = parser.parse_args("--value".split())
    print "仅为--value时输出为：", args
    print "================end================"


if __name__ == '__main__':
    """main"""
    # simpleTest()
    # descriptionTest()
    # epilogTest()
    # parentTest()
    # conflictTest()
    # prefixCharsTest()
    # constTest()
    # argumentGroupTest()
    subprocessTest()
