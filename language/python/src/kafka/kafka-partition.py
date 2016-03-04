#coding:utf-8
'''
    功能：测试在多个分区(partitions)情况下，发送大规模的数据时，是否会自动负载
'''
import sys
import traceback
from kafka import SimpleProducer, KafkaClient

from basepacKage.baselog import globalLog

def exceptionCatch(func,*args,**kw):
    def innerFunc(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception,msg:
            traceList = traceback.extract_tb(sys.exc_traceback)
            for (file,lineno, funcname,text) in traceList:
                globalLog.getError().log(globalLog.ERROR, \
                        "Occur error, func:%s,lineno:%s, msg:%s"%(funcname, lineno, msg))
            sys.exit(-1)
    return innerFunc

@exceptionCatch
def partitionsLoadBalance():
    '''
       发送指定信息到kafka-topic（test），此时为5000次 
    '''
    k1 = KafkaClient('localhost:9092')
    producer = SimpleProducer(k1)
    
    for i in range(200):
        msg = 'This is %dst test'%(i)
        msg1 = ''
        for j in range(2000):
            msg1 = ':'.join([msg1, msg])
        producer.send_messages(b'test', msg1)
    producer.stop()


if __name__ == '__main__':
    '''main'''
    partitionsLoadBalance()
