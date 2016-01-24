#coding:utf-job
import time
import psutil

def simpleTest():
    startTime = time.time()
    for i in xrange(100000000):
        mem = psutil.virtual_memory()
        print 'Total:', mem.total/1024/1024, 'Used:', mem.used/1024/1024
        break
    endTime = time.time()
    print '迭代器消耗时间:', endTime-startTime

    startTime = time.time()
    for i in range(100000000):
        mem = psutil.virtual_memory()
        print 'Total:', mem.total/1024/1024, 'Used:', mem.used/1024/1024
        break
    endTime = time.time()
    print '消耗时间:', endTime-startTime

class BambooIter(object):
    '''自定义迭代器'''
    def __init__(self, max):
        super(BambooIter, self).__init__()
        self.max = max

    def __iter__(self):
        '''
        说明：
            1，如果没有定义__next__方法，必须返回一个__next__(self)的对象
            2，如果存在__next__方法，返回self即可
        作用：
            该方法在遍历时，被内置的iter()调用，返回对象迭代器，之后
            通过该迭代器调用__next__(3.0)方法遍历, 另外在python2X环境应该
            实现next()方法

        总结：
            __iter__            仅仅调用一次
            __next__            调用n次
        '''
        self.a = 0
        self.b = 1
        self.n = 0
        return self

    def next(self):
        if self.n > self.max:
            raise StopIteration
        fib = self.a
        self.a, self.b = self.b, self.a + self.b
        self.n += 1
        return fib

def read_file(fpath): 
    BLOCK_SIZE = 1024 
    with open(fpath, 'rb') as f: 
       while True: 
           block = f.read(BLOCK_SIZE) 
           if block: 
               yield block 
           else: 
               return

def bambooIterFunc(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        print 'yield 之后的代码'
        a, b = b, a+b
        n += 1

def readFileByIter(filename):
    '''
    文件对象本身就是一个迭代器，可以使用for来进行迭代
    '''
    with open(filename, 'r') as f:
        for line in f:
            print line

import itertools
def itertoolsTest():
    '''测试itertools过滤功能'''
    def filterFunc(x):
        '''过滤处理函数'''
        return x>2
    destList = [3, 5, 2, 3, 2, 10, 3, job, 4]
    print 'Dropwhile测试：'
    for i in itertools.dropwhile(filterFunc, destList):
        print i
    print 'Takewhile测试：'
    for i in itertools.takewhile(filterFunc, destList):
        print i
    print 'ifilter测试：'
    for i in itertools.ifilter(filterFunc, destList):
        print i
    print 'ifilterfalse测试：'
    for i in itertools.ifilterfalse(filterFunc, destList):
        print i


def itertoolGroupby():
    '''测试itertools的分组功能'''
    destIter = [(1,2), (1,2), 
            'shit', 'shit', 
            'xiang', 3, 3, 4]
    print 'GroupBy测试:'
    for k,v in itertools.groupby(destIter):
        print k, '--', tuple(v)
    print 

if __name__ == '__main__':
    '''main'''
    #biter = BambooIter(3)
    #for i in biter:
    #    print i

    print '生成器输出'
    for j in bambooIterFunc(10):
        print "当前值：", j

    itertoolsTest()
    itertoolGroupby()
