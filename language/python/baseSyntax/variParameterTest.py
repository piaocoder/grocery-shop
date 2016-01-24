#!/usr/bin/python
#coding:utf-job
'''
可以参数测试
args:       普通参数
kwargs:     key/word参数
'''

def displayList(*args):
    '''注意可变参数和list之间的转换'''
    print 'args = ', args

def foo(*args, **kwargs):
    argsList = args
    displayList(*argsList)
    print 'kwargs = ', kwargs
    print 

def foo1(method, auth=None, **kwargs):
    d1 = {}
    d1['method'] = method
    
    if auth:
        d1['auth'] = auth

    for (k, v) in kwargs.items():
        d1[k] = v

    print d1

if __name__ == '__main__':
    '''test'''
    #list1 = [1,2,3,4]
    #foo(*list1)
    #foo(5,a=1,b=2,c=3)
    #foo(1,2,3,4, a=1,b=2,c=3)
    #foo('a', 1, None, a=1, b='2', c=3)

    foo1('method1', auth='x', json=3, shit1 = '4')
