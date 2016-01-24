#/usr/bin/env python
#coding:utf-job
import sys
import time

from kafka import KafkaConsumer
from kafka.common import (
    UnknownTopicOrPartitionError, LeaderNotAvailableError,
    KafkaUnavailableError,
)

def simpleConsumer():
    '''
    @function:测试基本的消费者
    @topic：单一replica，一旦对应的brokers关闭后，排除的异常信息
    @servers:设置多个brokers，但是没有任何用途
    '''
    # To cunsume messages
    try:
        consumer = KafkaConsumer('JOB_TEST_1', \
                bootstrap_servers=['devops-dev1:9193', 'devops-dev1:9194'])
    except KafkaUnavailableError,msg:
        print 'KafkaUnavailableError:',msg
        sys.exit(-1)

    while True:
        try:
            for message in consumer:
                '''
                message value is raw byte string
                @topic:话题名称
                @partition:消息号(每一个消息都是单一的个体)
                @offset:消息在topic-partition中的偏移量
                @value:原始字节(raw bytes)
                '''
                print("TOPIC:%s Partition:%d offset%d key=%s value=%s" % (\
                        message.topic, message.partition,
                        message.offset, message.key,
                        message.value)) 
        except (KafkaUnavailableError,LeaderNotAvailableError), msg:
            print 'Occur KafkaUnavailableError, msg:', msg
            time.sleep(10)
        else:
            break

def simpleConsumer1(topics):
    '''
    @function:测试基本的消费者
    @topic：多个replica，某一个brokers关闭后，是否正常输出
    @servers:设置多个brokers
    @fetch_min_bytes：每一次请求的最小字节
    @group_id：消费者组ID，用于offset的记录
    @auto_commit_enable: 定时记录offset到kafka cluster
    '''
    # To cunsume messages
    try:
        consumer = KafkaConsumer(
                *topics, 
                fetch_min_bytes = 1024, 
                group_id = 'job_consumer_group',
                #auto_offset_reset = 'smallest',
                #auto_commit_enable = True,
                bootstrap_servers=['devops-dev1:9193', 'devops-dev1:9194'])
    except KafkaUnavailableError,msg:
        print 'KafkaUnavailableError:',msg
        sys.exit(-1)

    # get offset
    consumer.set_topic_partitions('JOB_TEST', 'JOB_TEST_1')

    while True:
        try:
            for message in consumer:
                '''
                message value is raw byte string
                @topic:话题名称
                @partition:消息号(每一个消息都是单一的个体)
                @offset:消息在topic-partition中的偏移量
                @value:原始字节(raw bytes)
                '''
                print("TOPIC:%s Partition:%d offset%d key=%s value=%s" % (\
                        message.topic, message.partition,
                        message.offset, message.key,
                        message.value)) 
                consumer.task_done(message)
                consumer.commit()
        except (KafkaUnavailableError,LeaderNotAvailableError), msg:
            print 'Occur KafkaUnavailableError, msg:', msg
            time.sleep(10)
        else:
            consumer.task_done()
            print "Commit:", consumer.commit()
 
def advanceConsumer():
    '''
    multipic topics and auto commit offset
    '''
    consumer = KafkaConsumer('bamboo1', 'bamboo2', 
            bootstrap_servers=['10.1.200.63:9092'], 
            group_id = 'job_consumer_group',
            auto_commit_enable=True,
            auto_commit_interval_ms=30 * 1000, 
            auto_offset_reset='smallest')

    # initialize iteration
    for message in consumer:
        print("TOPIC:%s Partition:%d offset%d key=%s value=%s" % (\
                message.topic, message.partition,
                message.offset, message.key,
                message.value)) 
        consumer.task_done(message)

    consumer.commit()

    # Batch process interface
    while True:
        for m in consumer.fetch_messages():
            print("===Topic:%s Partition:%d offset%d key=%s value=%s" % (\
                    message.topic, message.partition,
                    message.offset, message.key,
                    message.value)) 
            consumer.task_done(m)


if __name__ == '__main__':
    '''main'''
    #simpleConsumer()
    topicList = ['JOB_TEST', 'JOB_TEST_1']
    simpleConsumer1(topicList)
    #advanceConsumer()
