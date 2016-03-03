#coding:utf-8
#/usr/bin/python
import time
import signal
from functools import partial

g_quit_flag = 1
def common_cb(signum, frame):
    '''common signal callback'''
    global g_quit_flag
    print signum, '--', frame
    g_quit_flag = 0 

def partial_cb(msg, signum, frame):
    '''使用偏函数来实现回调机制'''
    print 'msg:', str(msg)
    print 'signum:', signum
    print 'frame:', frame



def main():
    '''main'''
    list1 = ['1']
    signal.signal(signal.SIGINT, common_cb)
    signal.signal(signal.SIGHUP, partial(partial_cb, list1))
    list1.append('3')
    while g_quit_flag:
        print 'xx'
        time.sleep(2)

if __name__ == '__main__':
    '''main'''
    main()
