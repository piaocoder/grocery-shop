#coding:utf-job
from kafka import (KafkaConsumer)
from kafka.common import (ConsumerTimeout, KafkaMessage)

def testRestart():
    '''test restart
    测试某一个group在消费了kafka中的消息并commit之后，是否能重新读取？
            ->事实是不行
    '''
    topicsList = ['JOB_NGINX', 'JOB_BASIC', 'JOB_JMON', 'JOB_TOMCAT']
    brokerList = ['10.10.90.171:9092', '10.10.job2.114:9092', '10.10.94.15:9092']
    groupId = 'job_consumer_group'
    kc = KafkaConsumer(
            *topicsList,
            fetch_min_bytes = 1024, 
            group_id = groupId,
            bootstrap_servers = brokerList,
            consumer_timeout_ms = 10*1000,
            auto_offset_reset='smallest'
            )
    print kc.offsets()
    for partition in [0, 1, 2]:
        consumerMsg = KafkaMessage('JOB_BASIC', \
                partition, 2000, 'shit', 'shit')
        kc.task_done(consumerMsg)
    print kc.offsets()
    kc.set_topic_partitions(
            ('JOB_BASIC', 0, 2000), 
            ('JOB_BASIC', 1, 2000),
            ('JOB_BASIC', 2, 1000))
    import pdb
    pdb.set_trace()
    while 1:
        try:
            for consumer in kc:
                print consumer
                print type(consumer)
                kc.task_done(consumer)
        except ConsumerTimeout:
            kc.commit()
            print 'xxxxxxxxxxxxxxxxx'
            continue

def testOffset():
    '''test kafka offset
    测试某一个group在设置offset是否能指定位置读取，其中没有进行commit提交操作
    '''
    topicsList = ['JOB_NGINX', 'JOB_BASIC', 'JOB_JMON', 'JOB_TOMCAT', 'JOB_KV']
    groupId = 'job_consumer_group'
    brokerList = ['10.10.90.171:9092', '10.10.job2.114:9092', '10.10.94.15:9092']
    kc = KafkaConsumer(
            *topicsList, 
            fetch_min_bytes = 1024, 
            group_id = groupId,
            bootstrap_servers = brokerList,
            consumer_timeout_ms = 10*1000
            )
    #offsetDict = kc.offsets()
    #print 
    #print "commit:", offsetDict['commit']
    #print "task_done:", offsetDict['task_done']
    #print "fetch:", offsetDict['fetch']
    #print '==============================================='
    #while 1:
    #   try:
    #       for consumer in kc.fetch_messages():
    #           print consumer
    #           print type(consumer)
    #   except ConsumerTimeout:
    #       print 'xxxxxxxxxxxxxxxxx'
    #       continue
    print '+++++++++++++++++++++++++++++++'
    kc.set_topic_partitions(*topicsList)
    while 1:
        try:
            for consumer in kc:
                print consumer
                print type(consumer)
        except ConsumerTimeout:
            print 'xxxxxxxxxxxxxxxxx'
            continue
    offsetDict = kc.offsets()
    print 
    print "commit:", offsetDict['commit']
    print "task_done:", offsetDict['task_done']
    print "fetch:", offsetDict['fetch']

if __name__ == '__main__':
    '''main
    '''
    #testOffset()
    testRestart()
    #testSimple()
