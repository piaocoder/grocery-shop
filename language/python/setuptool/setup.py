#!/usr/bin/python
# coding:utf-job
import re
import sys
import os
import stat
import shutil
from setuptools import setup, find_packages

DATADIR="/data/test1"
LOGDIR="/data/logs/test1"
CONFDIR="/data/conf/test1"
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
    conf = 'basepackage/baseconfig.py'
    with open(conf, 'r') as f:
        oldStr = f.read()
    with open(conf, 'w') as f:
        f.write(re.sub("\nCONF_DIR.*basepackage.ini\"?\n",
            "\nCONF_DIR = \"{0}/basepackage.ini\"\n".format(CONFDIR), oldStr))
    

def mkdirDir():
    """Test data and log directory and make"""
    # data
    if not os.path.isdir(CONFDIR):
        os.makedirs(CONFDIR)

    # modify file authority
    try:
        os.chmod(CONFDIR, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
    except Exception,msg:
        sys.stderr.write('User does not have '\
                'modify permissions, msg:%s\n'%msg)

def copyConf():
    """Copy configure file"""
    # basepackage
    conf = "conf/basepackage.ini"
    if not os.path.exists(conf):
        sys.stderr.write("Note exists configure %s.\n" % conf)
        sys.exit(-1)
    shutil.copy(conf, CONFDIR+"/"); 

    # kafka
    conf = "conf/kafka.ini"
    if not os.path.exists(conf):
        sys.stderr.write("Note exists configure %s.\n" % conf)
        sys.exit(-1)
    shutil.copy(conf, CONFDIR+"/"); 

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

setup(
    name = "basepackage",
    version = "0.1",

    # 1,简单--如果未做任何嵌入参数：默认为name字段指定的同名目录
    # 2,复杂--指定packages路径，此时需要package_dir配合
    # -----函数返回一个packages列表，以供setup进行打包-----
    packages = find_packages(),
    #packages = find_packages('src'),
    #package_dir = {'':'src'},

    # 依赖包
    install_requires = ['logging', 'Fleepy'],

    # exclude_package_data的反面，如果设置了include_package_data，就没有
    # 必要设置该项的值(不一定)，此时conf在basepackage目录下方，并且不是
    # __init__.py文件
    package_data = {
        'basepackage':['conf/*.ini'],
        },

    # 包含packages目录下的所有文件（包含__init__.py）
    include_package_data = True,

    # 所有在packages目录下不打入最终包的文件字典列表
    #exclude_package_data = {},

    author = "unlessbamboo",
    author_email = "unlessbamboo@shit.com",
    description = "This is test1's base packages.",
    license = "SHIT",
)
