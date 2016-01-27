#!/usr/bin/python
# coding:utf-8
import re
import sys
import os
import stat
import shutil
try:
    #from setuptools import setup, find_packages
    from setuptools import setup
except ImportError:
    from distutils.core import setup


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
# 调试：设置DISTUTILS_DEBUG环境变量，任何值（除了空）
# 打包的文件涉及：
#           1，packages或者py_modules指定的源码文件
#           2，libraries或者ext_modules指定的C文件
#           3，scripts指定的脚本文件
#           4，test/test*.py文件
#           5，README以及setup.py,setup.cfg文件
#           6，package_data以及data_files指定的文件
#           7，MANIFEST.in文件指定的文件(不是mainfest，而是manifest)
# 参考文档
#       https://pythonhosted.org/setuptools/setuptools.html
#       https://docs.python.org/2/distutils/setupscript.html?highlight=distutils_debug
#
packages = [
    'basepackage',
    'basepackage/test',
]

setup(
    # 功能：包名
    name="basepackage",

    # 功能：包版本
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
    #packages=find_packages('src'),
    #packages=find_packages(),
    packages=packages,

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
    package_dir={'basepackage': 'basepackage'},

    # 依赖包或者更新最新版本的依赖包
    # install_requires=['logging', 'Fleepy'],

    # 安装脚本时需要以来的分发包，用于构建过程
    # setup_requires=['setuptools']

    # 功能：包含指定的数据文件
    # 附加说明：
    #       1，设置了include_package_data，就没有必要设置该项的值(不一定)，
    #           例如：
    #               '': ['*.txt']， 任何包下面的所有.txt文件
    #               'conf': ['conf/*.ini']，conf目录下面的所有ini文件，当然
    #       2，exclude_package_data的反面设置
    #       3，该字典中的值必须是：
    #           packages或者package_dir   --->    相对路径目录的列表
    #package_data={
        #'': ['NOTICE', 'LICENSE'],
        #'basepackage': ['*.dat'],
        #},

    # 功能：将指定的配置文件按照到指定的目录中
    # 附加说明：
    #   1，其他源文件都是相对于编译路径，即：
    #       ./conf/test.ini，其中conf和src是同级目录
    #   2，打包、安装时都会涉及拷贝操作
    data_files=[
        ('/etc/init.d/', ['conf/test.ini'])
    ],

    # 功能：同package_data，告知setuptools打包指定的任何文件
    # 附加说明：
    #       该选项必须和CVS、MANIFEST.in文件联合使用
    #       即该选项为True时，会读取CVS、SVN文件中的文件
    include_package_data=True,
    
    # 功能：
    #       排除指定的文件
    # exclude_package_data={},

    # 功能：动态发现服务和插件、自动生成脚本
    #       1,将python应用变为插件模式，以便其他应用使用
    entry_points = {
            'console_scripts': [
                # /usr/bin下生成插件foo，
                # 该插件将执行basepackage.baselog中的函数
                'foo=basepackage.baselog:bamboo',
                'bar=basepackage.baselog:bamboo',
                ],
            'setuptools.installation': [
                # Eggs execute，使egg可以执行，python basepackage.egg
                'eggsexecute = basepackage.baselog:bamboo',
                ],
            },

    zip_safe=False,

    # 作者信息
    author="unlessbamboo",
    author_email="unlessbamboo@gmail.com",
    # 包维护者信息
    maintainer="unlessbamboo",
    maintainer_email="unlessbamboo@gmail.com",
    # 包的官方网址
    url="http://www.cnblogs.com/unlessbamboo/",

    # 短暂描述
    description="This is test1's base packages.",
    # license
    license="GUN",
)
