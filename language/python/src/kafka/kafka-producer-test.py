#/usr/bin/env python
#coding:utf-8
import sys
import time
from kafka import SimpleProducer, KafkaClient, KeyedProducer
from kafka.common import (
    UnknownTopicOrPartitionError, LeaderNotAvailableError,
    KafkaUnavailableError, FailedPayloadsError
)

def simpleTest():
    # 使用bamboo:9192kafka服务器进行连接测试
    try:
        kafka = KafkaClient('bamboo:9192')
    except KafkaUnavailableError, msg:
        print "KafkaUnavailableError:", msg
        sys.exit(-1)
    except Exception,msg:
        print "Exception:", msg
        sys.exit(-1)
    producer = SimpleProducer(kafka)
    print kafka.topics

    '''
    Note that the application is responsible 
    for encoding messages to type bytes
    '''
    if 'JOB_TEST_1' in kafka.topics:
        producer.send_messages(b'JOB_TEST_1', b'some message')
        producer.send_messages(b'JOB_TEST_1', 
                b'this method', b'is variadic')
        
        # Send unicode message
        producer.send_messages(b'JOB_TEST_1', 
                u'你怎么样?'.encode('utf-8'))
        producer.stop()

def keyedProducerTest1():
    '''test KeyedProducer
    @topic：多replica情况
    @function:测试KeyedProducer，向指定的broker发布消息，
        并验证develops-dev1:9193关闭之后仍然能够顺利运行
    '''
    import pdb
    pdb.set_trace()
    kafkaClient = KafkaClient('devops-dev1:9193')
    producer = KeyedProducer(kafkaClient)
    message = "This is a test-" 
    index = 0
    while True:
        tmpmsg = message + str(index)
        index += 1
        producer.send_messages(b'JOB_TEST', 'keys', tmpmsg) 
        time.sleep(1)

def keyedProducerTest2():
    '''test KeyedProducer
    @topic：单replica情况(JOB_TEST_1)
    @function:测试KeyedProducer，向指定的broker发布消息，
        并验证develops-dev1:9193关闭之后的异常报错
    '''
    import pdb
    pdb.set_trace()
    kafkaClient = KafkaClient('devops-dev1:9193')
    producer = KeyedProducer(kafkaClient)
    message = "This is a test-" 
    index = 0
    while True:
        tmpmsg = message + str(index)
        producer.send_messages(b'JOB_TEST_1', 'keys', tmpmsg) 
        index += 1
        time.sleep(1)

def waitBrokerRecover(kafkaClient):
    '''wait broker recover'''
    try:
        producer = KeyedProducer(kafkaClient)
    except KafkaUnavailableError:
        time.sleep(10)
    else:
        return producer

def keyedProducerTest3():
    '''test KeyedProducer
    @topic：单replica情况(JOB_TEST_1)
    @function:测试KeyedProducer，向指定的broker发布消息，
        并验证develops-dev1:9193关闭之后的异常的恢复情况
        （等待10秒，不用重新拉起，自动关联）
    '''
    import pdb
    pdb.set_trace()
    kafkaClient = KafkaClient('devops-dev1:9193')
    producer = KeyedProducer(kafkaClient)
    message = "This is a test-" 
    index = 0
    while True:
        try:
            tmpmsg = message + str(index)
            producer.send_messages(b'JOB_TEST_1', 'keys', tmpmsg) 
            index += 1
            time.sleep(1)
        except (FailedPayloadsError,KafkaUnavailableError), msg:
            print 'Occur FailedPayloadsError error, msg:', msg
            time.sleep(10)

if __name__ == '__main__':
    '''main'''
    keyedProducerTest1()
