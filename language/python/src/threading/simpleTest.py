#coding:utf-8
import sys
import threading
import signal
import time
import Queue

class A:
    def __init__(self):
        self.flag = False
        self.queue = Queue.Queue()

    def display(self, *args, **kwargs):
        '''print'''
        print args
        for i in range(1000):
            self.queue.put('This is %d test'%(i))
            time.sleep(1)
            if self.flag:
                break

    def handle(self, a, b):
        print 'XXXXXXXXXXXXXXXXXXXXXXXX'
        self.flag = True

    def threadingFunc(self):
        '''
        threading.Thread测试
        '''
        # 创建Thread对象
        thread1 = threading.Thread(target=self.display, 
                name='displayThread', args=[1, 2, 3, 4,], 
                kwargs = {'a':'shit', 'b':'test'})
        # 启动线程
        thread1.start()
        while not self.flag:
            print '==============='
            print self.queue.get()
            time.sleep(1)
        thread1.join()
        time.sleep(3)
        print "xxxxxxxxxx", thread1.isAlive()

if __name__ == '__main__':
    '''main'''
    a = A()
    signal.signal(signal.SIGTERM, a.handle)
    a.threadingFunc()
