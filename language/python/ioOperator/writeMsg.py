#!/usr/bin/env python
#coding:utf-8
import time

filename = '/tmp/ioNotify.tmp'
index = 0
with open(filename, 'w+') as f:
    while 1:
        for i in range(80000):
            index += 1
            f.write('The {0} lines.\n'.format(index))
            f.flush()
        time.sleep(0.5)
        if i > 1000000000:
            break
