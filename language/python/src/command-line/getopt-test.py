#!/usr/bin/env python
#coding:utf-8
import sys
import getopt


def usage():
    """usage"""
    usage_doc = """cli option test.
    Usage:
        ./cli-option -m [MODULES] -s M -d N

    Options:
        -h or --help
        -l or --list
        -m or --module
            please intput a valid module name.
        -s or --start
            please input a start test case number.
        -e or --end
            please input a end test case number.

    For more info visit http://www.unlessbamboo.com.cn/"""
    print usage_doc


def getCliOptions(argv):
    """getCliOptions:get command options

    :param argv:
    """
    # 尽量不要使用相同开头字母的短选项
    short_opt = "m:s:e"
    long_opt = ["list", "module=", "start=", "end=", "lisa"]
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opt, long_opt)
    except getopt.GetoptError, msg:
        print "Occur error, msg:{0}".format(msg)
        usage()
        sys.exit(1)

    # 仅仅进行必选项的检查（有就检查，没有就忽略）
    print "选项序列:", opts
    for opt, arg in opts:
        print "\t选项：{0}, 值:{1}".format(opt, arg)

    print "无关参数序列:", args


if __name__ == "__main__":
    """main"""
    getCliOptions(sys.argv)
