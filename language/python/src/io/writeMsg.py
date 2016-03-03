#!/usr/bin/env python
##
# @file writeMsg.py
# @brief    将数据写入指定文件，meta必须为一行，用于测试pyinotify模块
# @author unlessbamboo
# @version 1.0
# @date 2016-02-14

#coding:utf-8
import time

filename = '/tmp/ioNotify.tmp'
index = 0
with open(filename, 'w+') as f:
    while 1:
        for i in range(800):
            index += 1
            f.write('The {0} lines.\n'.format(index))
            f.flush()
        time.sleep(0.5)
        if i > 100000:
            break
