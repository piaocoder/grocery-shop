#coding:utf-8
'''
    assume0：测试在单个分区(partitions)，多replica情况下:
        1,发送大规模的数据时, 是否会自动负载?
        2,如果某一个人为关闭leader，是否会自动负载？

        问题1：
            replica无关负载均衡，仅仅涉及高可用性，即对于数据的复制
        问题2：
            应该关注的测试点，在leader关闭的情况下，如果继续produce是否发生数据丢失，
            即consumer是否有数据输出？
        验证：
            成功解决问题1,2

    assume1：
        是否因为assume0中的测试涉及的IP地址都是localhost，导致没有出现问题？
    操作：
        0，限定zookeeper数量为1
        1，保持当前zookeeper不变，修改每一个broker中的zookeeper.connect值
        2，在10.1.200.124上面新建两个broker
     

    
'''
import sys
import traceback

from kafka import SimpleProducer, KafkaClient
from basepackage.baselog import globalLog

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
def replicaLoadBalance():
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
        producer.send_messages(b'replica-test', msg1)
    producer.stop()

@exceptionCatch
def replicaLoadBalance1():
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
        producer.send_messages(b'replica-test', msg1)
    producer.stop()

if __name__ == '__main__':
    '''main'''
    replicaLoadBalance()
