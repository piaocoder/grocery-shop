#!/usr/bin/env python
#coding:utf8
##
# @file python-tags.py
# @brief    考虑到存在多个python版本的问题，因为pyenv或者多版本安装，
#           在打开vim时，对于tags文件的导入可能发生混淆，所以利用
#           该脚本对python_bamboo.vim进行更改操作
# @author unlessbamboo
# @version 1.0
# @date 2016-03-03
import os
import sys
import subprocess


def error_msg(pstr):
    """error_msg:错误信息输出

    :param pstr:
    """
    print "({0}) occur error, msg:{1}".format(__file__, pstr)


g_python_path = """\" Python语言tags 路径设置
\" 根据不同的python版本生成不同的bamboo文件
if has("tags")
    set tags+=tags,{0}{2}
else
    set tags=tags,{1}{3}
endif
"""

g_union_path = """\" C/python语言tags 路径设置
" 根据不同的python版本生成不同的bamboo文件
if has("tags")
    set tags+=tags,/usr/lib/gcc/tags,/usr/include/tags,/usr/local/include/tags
    set tags+=tags,{0}{2}
else
    set tags=tags,/usr/lib/gcc/tags,/usr/include/tags,/usr/local/include/tags
    set tags=tags,{1}{3}
endif

" C语言path 路径设置
set path+=.,/usr/include/,/usr/lib/gcc,/usr/local/include
"""


def get_python_version():
    """get_python_version"""
    # 为何stdout就不行？阻塞输出？
    # out = subprocess.Popen("python --version",
    #           shell=True, stderr=subprocess.PIPE)
    mainVersion = '%d.%d' % (sys.version_info[0:2])
    return mainVersion


def get_python_library_path():
    """get_python_library_path"""
    out = subprocess.Popen("python-config --prefix",
                           shell=True, stdout=subprocess.PIPE)
    outMsg = out.stdout.read().split('\n')[0]
    mainVersion = get_python_version()
    lPath = '{0}/lib/python{1}/'.format(outMsg, mainVersion)
    lPath64 = '{0}/lib64/python{1}/'.format(outMsg, mainVersion)
    return lPath, lPath64


def construct_python_tags():
    """construct_python_tags"""
    global g_python_path
    lPath, lPath64 = get_python_library_path()

    if not os.path.exists(lPath64):
        tagsPath64 = ''
    else:
        tagsPath64 = ',' + lPath64 + 'tags'
    tagsPath = lPath + 'tags'

    msg = g_python_path.format(tagsPath, tagsPath,
                               tagsPath64, tagsPath64)
    with open('./python_bamboo.vim', 'w+') as f:
        f.write(msg)


def construct_union_tags():
    """construct_union_tags"""
    global g_union_path
    lPath, lPath64 = get_python_library_path()

    if not os.path.exists(lPath64):
        tagsPath64 = ''
    else:
        tagsPath64 = ',' + lPath64 + 'tags'
    tagsPath = lPath + 'tags'

    msg = g_union_path.format(tagsPath, tagsPath,
                               tagsPath64, tagsPath64)
    with open('./union_bamboo.vim', 'w+') as f:
        f.write(msg)


if __name__ == '__main__':
    """main"""
    construct_python_tags()
    construct_union_tags()
