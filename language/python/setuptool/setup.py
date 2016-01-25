#!/usr/bin/python
# coding:utf-8
import re
import sys
import os
import stat
import shutil
from setuptools import setup, find_packages


DATADIR = "/data/test1"
LOGDIR = "/data/logs/test1"
CONFDIR = "/data/conf/test1"


def initConfEnv():
    """Initialize configure and modidy basepackage.ini"""
    # data
    conf = 'conf/basepackage.ini'
    with open(conf, 'r') as f:
        oldStr = f.read()
    with open(conf, 'w') as f:
        f.write(re.sub("\ndata=.*?\n",
                       "\ndata={0}\n".format(DATADIR), oldStr))

    # logs
    conf = 'conf/basepackage.ini'
    with open(conf, 'r') as f:
        oldStr = f.read()
    with open(conf, 'w') as f:
        f.write(re.sub("\nlogs=.*?\n",
                       "\nlogs={0}\n".format(LOGDIR), oldStr))

    # baseconfig
    conf = 'src/basepackage/baseconfig.py'
    with open(conf, 'r') as f:
        oldStr = f.read()
    with open(conf, 'w') as f:
        f.write(re.sub("\nCONF_DIR.*basepackage.ini\"?\n",
                       "\nCONF_DIR = \"{0}/basepackage.ini"
                       "\"\n".format(CONFDIR), oldStr))


def mkdirDir():
    """Test data and log directory and make"""
    # data
    if not os.path.isdir(CONFDIR):
        os.makedirs(CONFDIR)

    # modify file authority
    try:
        os.chmod(CONFDIR, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    except Exception, msg:
        sys.stderr.write('User does not have '
                         'modify permissions, msg:%s\n' % msg)


def copyConf():
    """Copy configure file"""
    # basepackage
    conf = "conf/basepackage.ini"
    if not os.path.exists(conf):
        sys.stderr.write("Note exists configure %s.\n" % conf)
        sys.exit(-1)
    shutil.copy(conf, CONFDIR+"/")

    # kafka
    conf = "conf/kafka.ini"
    if not os.path.exists(conf):
        sys.stderr.write("Note exists configure %s.\n" % conf)
        sys.exit(-1)
    shutil.copy(conf, CONFDIR+"/")


def main():
    """main"""
    try:
        initConfEnv()
        mkdirDir()
        copyConf()
    except Exception, msg:
        sys.stderr.write("Occur error, msg:{0}.\n".format(msg))
        sys.exit(-1)

main()

#
# 调用代码：/usr/local/python/lib/python2.7/distutils/core.py
setup(
    name="basepackage",
    version="0.1",

    # 功能：告知setuptools要处理那些包，例如
    #       [
    #           'basepackage',
    #           'basepackage.test',
    #           'basepackage.s1',
    #       ]
    # 选项：
    #       首参数：一般为空，可以用于指定source directory或者root dir
    #               此时需要packages_dir来合作完成
    #       exclude---排除某些文件
    # 附加说明：
    #     1,简单--如果未做任何嵌入参数：默认为name字段指定的同名目录
    #     2,复杂--指定packages路径，此时需要package_dir配合
    # PS:函数返回一个packages列表，以供setup进行打包-----
    # 返回值：返回['basepackage', 'basepackage.test']，
    #           其中所有目录下必须存在__init__.py文件
    packages=find_packages('src'),
    # packages=find_packages('src'),

    # 功能：
    #       1,告知setuptools根目录，此时必须设置该值
    #       2,此时所有的packages路径应该是：
    #       [
    #           'src/basepackage',
    #           'src/basepackage.test',
    #           'src/basepackage.s1',
    #       ]
    #           当然，find_packages会帮你寻找到所有符合要求的路径
    #       3,如果使用{'basepackage': 'src'}，则默认不进行递归查找，所有的
    #           子目录都必须在packages中指定才可以
    #
    #
    package_dir={'': 'src'},

    # 依赖包
    # install_requires=['logging', 'Fleepy'],

    # 功能：包含指定的数据文件
    # 附加说明：
    #       1，设置了include_package_data，就没有必要设置该项的值(不一定)，
    #           例如：
    #               '': ['*.txt']， 任何包下面的所有.txt文件
    #               'conf': ['conf/*.ini']，conf目录下面的所有ini文件，当然
    #       2，exclude_package_data的反面设置
    #       3，该字典中的值必须是：
    #           packages或者package_dir   --->    相对路径目录的列表
    package_data={
        'basepackage': ['data/*.dat'],
        },

    # 功能：同package_data，告知setuptools打包指定的任何文件
    # 附加说明：
    #       该选项必须和版本控制、MANIFEST.in文件联合使用
    # include_package_data=True,

    # exclude_package_data={},

    author="unlessbamboo",
    author_email="unlessbamboo@shit.com",
    description="This is test1's base packages.",
    license="SHIT",
)
