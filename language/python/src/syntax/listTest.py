#!/usr/bin/evn python
#coding:utf-8
'''
    function:Determine whether the list can store object.
'''
import thread
import time

class A:
    '''class'''
    def __init__(self,desc):
        ''''''
        self.desc = desc

    def display(self):
        ''''''
        print self.desc

class B:
    '''class B'''
    def __init__(self):
        ''''''
        self.objList = {}
        self.lock = thread.allocate_lock()

    def create(self, objList, desc):
        '''create a new Object of A'''
        self.lock.acquire()
        print desc + 'xx'
        a = A(desc)
        objList.append(a)
        self.lock.release()

    def multipleDisplay(self, listDesc):
        ''''''
        for elm in listDesc:
            print elm + 'wawa'
            thread.start_new_thread(self.create, (self.objList, elm))
        time.sleep(2)
        for ele in self.objList:
            ele.display()

if __name__ == '__main__':
    '''main'''
    b = B()
    b.multipleDisplay(['aa', 'bb', 'cc', 'dd', 'ff', 'ee'])

