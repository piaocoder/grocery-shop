#coding:utf-job
#/usr/bin/python
import os
import sys
import time
import multiprocessing

search_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, search_path)
from basepackage.baseparse import globalConfigParse
globalConfigParse.setPythonpath()

from basepackage.basemultilog import MultiProcessingLog

def producer1(squeue, d1):
    '''write log'''
    mpl = MultiProcessingLog(squeue)
    msgPre = 'Producer1:Msg'
    index = 1
    while 1:
        msg = ''.join([msgPre, str(index)])
        mpl.send_debug(mpl.ERROR, msg)
        time.sleep(1)
        index += 1
        d1[index] = 'xxxxx'+str(index)

def producer2(squeue):
    '''write log'''
    mpl = MultiProcessingLog(squeue)
    msgPre = '#1,Producer2:%d'
    index = 1
    while 1:
        index +=1
        mpl.send_error(mpl.ERROR, msgPre%(index))
        time.sleep(1)

def producer3():
    print 'xxxxxxxxxxxxx'
    pass

def main():
    '''main handle'''
    shareQueue = multiprocessing.Queue(-1)
    mpl = MultiProcessingLog(shareQueue, "main", module='common')
    mgr = multiprocessing.Manager()
    d1 = mgr.dict()

    p1 = multiprocessing.Process(target=producer1, args=(shareQueue, d1))
    p2 = multiprocessing.Process(target=producer2, args=(shareQueue,))
    p3 = multiprocessing.Process(target=producer3, args=())
    processDict = {
            'producer1':p1,
            'producer2':p2,
            }
    
    #
    # start process
    #
    p1.start()
    p2.start()
    p3.start()

    print '----------------------1'
    print p1.join()
    print '----------------------2'
    print p2.join()
    print '----------------------3'
    print p3.join()

    #
    # consumer
    #
    index = 1
    while 1:
        index +=1
        if index >20 or not mpl.receive():
            break
        print 'Index:', index
        print 'Dict:', d1

    # 
    # stop all process
    #
    while len(processDict): 
        for (name, pro) in processDict.items():
            if pro.is_alive():
                pro.terminate()
            else:
                del processDict[name]
        time.sleep(1)

if __name__ == '__main__':
    main()
