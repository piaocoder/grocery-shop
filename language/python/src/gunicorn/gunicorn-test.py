#!/usr/bin/env python
#coding:utf8
##
# @file gunicorn-test.py
# @brief    简单的测试gunicorn的命令
#           启动server命令：
#               gunicorn --worker=num  gunicorn-test:app
#           之前可以通过wget网络工具进行url资源访问操作
#               import requests
#               rsp = requests.get('http://127.0.0.1:8000')
#               print rsp.text
#
# @author unlessbamboo
# @version 1.0
# @date 2016-03-11


def app(environ, start_response):
    """app

    :param environ: 环境
    :param start_response:
    """
    data = "Hello, World!\n"
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])

    return iter([data])
