#!/usr/bin/python
#coding:utf-8
import os
import shutil
import re
import traceback
import sys
import subprocess


def exceptionCatch(func, *args, **kw):
    """异常处理"""
    def innerFunc(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception, msg:
            exc_type, _, exc_tb = sys.exc_info()
            traceList = traceback.extract_tb(exc_tb)
            for (filename, lineno, funcname, text) in traceList:
                print "Error, type:%s, file:%s, func:%s" \
                    ",lineno:%s, msg:%s, args:%s, kwargs:%s" % (
                        exc_type, filename, funcname,
                        lineno, msg, args, kw)
    return innerFunc


def create_build_directory():
    """create build directory

        创建build目录以及其他目录，用于存放编译后的可执行文件、配置文件
        等等
    """
    buildDir = ['build', 'build/conf', 'build/bin',
                'build/libs', 'build/include']
    for path in buildDir:
        if not os.path.isdir(path):
            os.makedirs(path)


def update_run_ldconf(installDir):
    """update and run ldconfig

        添加/apps/gcc/libs/lib到ldconfig中
    """
    boLdConf = "/etc/ld.so.conf.d/gcc-x86_64.conf"
    boValue = installDir + "/libs/lib"
    if not os.path.isfile(boLdConf):
        open(boLdConf, "w").close()
    with open(boLdConf, "w") as f:
        f.write(boValue)

    #run ldconf
    rst = subprocess.check_call(['ldconfig'])
    if rst:
        print "Call ldconfig failed:{0}.".format(
            subprocess.CalledProcessError)


def update_run_conf(logDir, installDir):
    """Update configure

       运行时配置文件修改：
            将日志配置文件，gcc运行配置文件中的路径更改
    """
    srcLogConf = "conf/gcc-zlog.conf"
    newLogConf = "build/conf/gcc-zlog.conf"
    srcRunConf = "conf/gcc.ini"
    newRunConf = "build/conf/gcc.ini"
    confDir = installDir + "/conf"

    # mkdir
    if not os.path.exists(logDir):
        os.makedirs(logDir)
    if not os.path.exists(confDir):
        os.makedirs(confDir)

    # copy
    shutil.copy(srcLogConf, newLogConf)
    shutil.copy(srcRunConf, newRunConf)

    # sub gcc-zlog.conf
    with open(newLogConf, "r") as f:
        oldStr = f.read()
    with open(newLogConf, "w") as f:
        f.write(re.sub("/data/logs/gcc/", logDir + "/", oldStr))

    # ini
    with open(newRunConf, "r") as f:
        oldStr = f.read()
    with open(newRunConf, "w") as f:
        f.write(re.sub("\nconfdir=.*?\n",
                       "\nconfdir={0}\n".format(confDir), oldStr))


def update_compile_include(installDir):
    """update common.h

        更改common.h文件中的宏，该宏记录了gcc.ini的位置
        @@:
            #define LOG_CONF_PATH  "/apps/gcc/conf/gcc.ini"
    """
    newConf = '"' + installDir + '/conf/gcc.ini' + '"'
    comm = './include/common.h'
    with open(comm, 'r') as f:
        oldStr = f.read()

    with open(comm, 'w') as f:
        f.write(re.sub("\n#define LOG_CONF_PATH .*?\n",
                       "\n#define LOG_CONF_PATH{0:>52}\n".format(
                           newConf), oldStr))


def update_compile_makefile(installDir):
    """update makefile

       编译时配置文件修改：
            更改makefile，保证编译安装的顺利执行
    """
    mk = './Makefile'
    with open(mk, "r") as f:
        oldStr = f.read()
    with open(mk, "w") as f:
        f.write(re.sub("\nINSTALLDIR=.*\n",
                "\nINSTALLDIR={0}\n".format(installDir), oldStr))


@exceptionCatch
def main(logDir, installDir):
    """main"""
    create_build_directory()

    update_compile_makefile(installDir)
    update_compile_include(installDir)

    update_run_ldconf(installDir)
    update_run_conf(logDir, installDir)

if __name__ == '__main__':
    """main"""
    main('/data/logs/gcc', '/apps/gcc')
    print "Compile prepare complete!"
