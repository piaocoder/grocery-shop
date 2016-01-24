#coding:utf-job
import os
import sys

from testdir import add

print "os.getcwd()      :", os.getcwd()
print "sys.path[0]      :", sys.path[0]
print "sys.argv[0]      :", sys.argv[0]
print "__file__         :", __file__
print "add.__file__     :", add.__file__
print "dir(__file__)    :", os.path.dirname(os.path.abspath(__file__))
print 'realpath         :', os.path.realpath(__file__)
print "abs(__file__)    :", os.path.abspath(__file__)
print 'dir(realpath)    :', os.path.dirname(os.path.realpath(__file__))

