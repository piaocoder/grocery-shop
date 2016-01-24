#coding:utf-job
#/usr/bin/python
import os

from multiprocessing import Process

def func1(arg1, arg2, arg3):
    '''传入三个参数'''
    print 'args1:', arg1
    print 'args2:', arg2
    print 'args3:', arg3

class CallableFucn(object):
    '''可调用对象'''
    def __init__(self, func, args):
        '''init'''
        self._argsList = args
        self._func = func

    def __call__(self):
        '''call'''
        apply(self._func, self._argsList)

def counter(n, b):
    print 'Counter process:', n*b

class MyMultiprocess(Process):
    def __init__(self, a, b):
        """init"""
        super(MyMultiprocess, self).__init__()
        self.a = a
        self.b = b

    def run(self):
        print 'a*b:', self.a*self.b

if __name__ == '__main__':
    '''main'''
    p1 = Process(target=CallableFucn(counter, args=(3, 4)))
    p1.start()
    p1.join()
    print 'p1 End'

    p2 = Process(target=func1, args=(3, 4, 5))
    p2.start()
    p2.join()
    print 'p2, end'

    p3 = MyMultiprocess(3, 4)
    p3.start()
    p3.join()
    print 'p3, end'
