#!/usr/bin/env python
#coding:utf-job

def A():
    try:
        print "xx"
        return
    except:
        print "err"
    else:
        print "---"
    return

if __name__=='__main__':
    A()
