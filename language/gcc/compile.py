#!/usr/bin/env python
# coding:utf-8
"""
    设置基础环境
"""
import os
import shutil
import re
import traceback
import sys
import subprocess


def exception_catch(func, *args, **kw):
    """异常处理"""
    def inner_func(*args, **kw):
        """处理"""
        try:
            return func(*args, **kw)
        except BaseException, msg:
            exc_type, _, exc_tb = sys.exc_info()
            trace_list = traceback.extract_tb(exc_tb)
            for (filename, lineno, funcname, _) in trace_list:
                print "Error, type:%s, file:%s, func:%s" \
                    ",lineno:%s, msg:%s, args:%s, kwargs:%s" % (
                        exc_type, filename, funcname,
                        lineno, msg, args, kw)
    return inner_func


def create_build_directory():
    """create build directory

        创建build目录以及其他目录，用于存放编译后的可执行文件、配置文件
        等等
    """
    build_dir = ['build', 'build/conf', 'build/bin', 'build/libs', 
                 'build/include']
    for path in build_dir:
        if not os.path.isdir(path):
            os.makedirs(path)


def update_run_ldconf(install_dir):
    """update and run ldconfig

        添加/apps/gcc/libs/lib到ldconfig中
    """
    bold_conf = "/etc/ld.so.conf.d/gcc-x86_64.conf"
    bo_value = install_dir + "/libs/lib"
    if not os.path.isfile(bold_conf):
        open(bold_conf, "w").close()
    with open(bold_conf, "w") as fobj:
        fobj.write(bo_value)

    # run ldconf
    rst = subprocess.check_call(['ldconfig'])
    if rst:
        print "Call ldconfig failed:{0}.".format(
            subprocess.CalledProcessError)


def update_run_conf(log_dir, install_dir):
    """Update configure

       运行时配置文件修改：
            将日志配置文件，gcc运行配置文件中的路径更改
    """
    src_log_conf = "conf/gcc-zlog.ini"
    new_log_conf = "build/conf/gcc-zlog.ini"
    src_run_conf = "conf/gcc.ini"
    new_run_conf = "build/conf/gcc.ini"
    conf_dir = install_dir + "/conf"

    # mkdir
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if not os.path.exists(conf_dir):
        os.makedirs(conf_dir)

    # copy
    shutil.copy(src_log_conf, new_log_conf)
    shutil.copy(src_run_conf, new_run_conf)

    # sub gcc-zlog.conf
    with open(new_log_conf, "r") as fobj:
        old_str = fobj.read()
    with open(new_log_conf, "w") as fobj:
        fobj.write(re.sub("/data/log/gcc/", log_dir + "/", old_str))

    # ini
    with open(new_run_conf, "r") as fobj:
        old_str = fobj.read()
    with open(new_run_conf, "w") as fobj:
        fobj.write(re.sub("\nconf_dir=.*?\n",
                          "\nconf_dir={0}\n".format(conf_dir), old_str))


def update_compile_include(install_dir):
    """update common.h

        更改common.h文件中的宏，该宏记录了gcc.ini的位置
        @@:
            #define LOG_CONF_PATH  "/apps/gcc/conf/gcc.ini"
    """
    new_conf = '"' + install_dir + '/conf/gcc.ini' + '"'
    comm = './include/common.h'
    with open(comm, 'r') as fobj:
        old_str = fobj.read()

    with open(comm, 'w') as fobj:
        fobj.write(re.sub("\n#define LOG_CONF_PATH .*?\n",
                          "\n#define LOG_CONF_PATH{0:>52}\n".format(
                              new_conf), old_str))


def update_compile_makefile(install_dir):
    """update makefile

       编译时配置文件修改：
            更改makefile，保证编译安装的顺利执行
    """
    mk1 = './Makefile'
    with open(mk1, "r") as fobj:
        old_str = fobj.read()
    with open(mk1, "w") as fobj:
        fobj.write(re.sub("\ninstall_dir=.*\n",
                          "\ninstall_dir={0}\n".format(install_dir), 
                          old_str))


@exception_catch
def main(log_dir, install_dir):
    """main"""
    create_build_directory()

    update_compile_makefile(install_dir)
    update_compile_include(install_dir)

    update_run_ldconf(install_dir)
    update_run_conf(log_dir, install_dir)


if __name__ == '__main__':
    main('/data/log/gcc', '/apps/gcc')
    print "Compile prepare complete!"
