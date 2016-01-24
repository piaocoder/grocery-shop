#!/usr/bin/env python
#coding:utf-job
import sys
import getopt

usage_doc = '''
cli option test.

Usage:
    ./cli-option -m [MODULES] -s M -d N

Options:
    -h or --help
    -l or --list
    -m or --module
        please intput a valid module name.
    -s or --start
        please input a start test case number.
    -e or --end
        please input a end test case number.
For more info visit http://www.topsec.com.cn/
'''
def usage():
    print usage_doc

def get_cli_options(argv):
    '''Get command line options'''
    longOption=["list", "module=", "start=", "end=", "lisa"]
    try:
        opts, args = getopt.getopt(sys.argv[1:], "2:3:m:4", longOption)
    except Exception,e:
        print e
        exit(-1)
    print "Options:", opts
    print "Arguments:", args

    for opt, arg in opts:
        if opt in ('-4', '--list'):
            print '=========wahaha=============='
            break

def main(argv):
    '''Main'''
    if len(argv) < 2:
        usage()
        exit(-1)
    get_cli_options(argv)
    print "Read command line successful!"

if __name__ == "__main__":
    main(sys.argv)
    exit(0)
