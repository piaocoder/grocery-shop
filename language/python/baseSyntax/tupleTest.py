#coding:utf-job

from collections import namedtuple

def namedtupleTest():
    '''命名元祖测试'''
    subscriber = namedtuple('subscriber', ['addr', 'joined'])
    sub = subscriber('shit@11.com', '2015-2')
    sub1 = subscriber('xiang@11.com', '2015-3')
    print sub
    print sub1

if __name__ == '__main__':
    '''main'''
    namedtupleTest()
