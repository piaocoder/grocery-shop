#!/usr/bin/python
# coding:utf-8
import re
import sys
import os
import stat
import shutil
from setuptools import setup, find_packages

DATADIR = "/data/job"
LOGDIR = "/data/logs/job"
CONFDIR = "/data/conf/job"


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
    shutil.copy(conf, CONFDIR + "/")

    # kafka
    conf = "conf/kafka.ini"
    if not os.path.exists(conf):
        sys.stderr.write("Note exists configure %s.\n" % conf)
        sys.exit(-1)
    shutil.copy(conf, CONFDIR + "/")


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
    name="basepackage",
    version="0.1",

    packages=find_packages(),
    # packages=find_packages('src'),
    # package_dir={'':'src'},

    install_requires=['pyinotify'],

    package_data={
        'basepackage': ['conf/*.ini'],
    },

    include_package_data=True,

    # exclude_package_data={},

    author="unlessbamboo",
    author_email="unlessbamboo@gmail.com",
    description="This is job's base packages.",
    license="JOB",
)
