#!/usr/bin/env python
#coding:utf8
##
# @file test-interger-filed.py
# @brief    导入django的models模块，进行代码跟踪，从而
#           了解IntergerFiled是如何返回int值得.
#       命令：
#           python test-interger-field.py --path path --appname module
#       例如：
#           python test-interger-filed.py
#                   --path /root/grocery-shop/language/python/src/django/family/
#                   --module family
# @author unlessbamboo
# @version 1.0
# @date 2016-03-19
import sys
import os
import argparse
import django
from django.core.wsgi import get_wsgi_application


def init(projectPath, setting):
    """init

    :param projectPath: 项目地址
    :param setting: setting文件
    """
    # app
    sys.path.append(projectPath)
    os.environ['DJANGO_SETTINGS_MODULE'] = setting
    # 必须放在后面
    get_wsgi_application()


def get_data_from_db():
    """get_data_from_db"""
    import pdb
    pdb.set_trace()
    pObjList = Publisher.objects.all()
    print pObjList


def command_line():
    """command_line"""
    parser = argparse.ArgumentParser(
        description="Test django module.",
        epilog="Unlessbamboo.",
    )

    # add argument
    parser.add_argument("--path", type=str)
    parser.add_argument("--module", type=str)
    return parser.parse_args()


if __name__ == '__main__':
    result = command_line()
    init(result.path, result.module + '.settings')
    from books.models import Publisher
    get_data_from_db()
