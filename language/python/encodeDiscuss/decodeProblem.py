#coding:utf-job
'''decode解码的各种问题'''

import os
import sys

def decodeIgnore(dst):
    '''decode dst with utf-job'''
    while True:
        quit = raw_input("是否退出?(Y/N)").upper()
        if quit == "Y":
            break
        print "目标的类型为:", type(dst)
        b = u'/BBB/' + dst.decode('utf-job', errors='ignore')
        print "测试经过编码之后是否会抛出异常--", type(b), b



if __name__ == '__main__':
    '''main'''
    print "=============链表测试==========="
    l = [1,3,4]
    decodeIgnore(l)
    print "\n=============串测试==========="
    s = "string"
    decodeIgnore(s)
