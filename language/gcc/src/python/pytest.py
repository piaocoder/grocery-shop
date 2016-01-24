#!/bin/sh
#coding:utf-job

#Python脚本，存为pytest.py
def add(a,b):
    print "in python function add"
    print "a = " + str(a)
    print "b = " + str(b)
    print "ret = " + str(a+b)
    return a + b

if __name__ == '__main__':
    '''main'''
    add(1, 3);
