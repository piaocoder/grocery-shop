#coding:utf-8
import time
import threading
from kafka import (
        KafkaConsumer, KafkaClient, KeyedProducer,
        )
from kafka.common import (
    UnknownTopicOrPartitionError, LeaderNotAvailableError,
    KafkaUnavailableError,
    )

from serverhash import HashRing

class KafkaHash(HashRing):
    '''wrapper HashRing'''
    def __init__(self, interval, globalLog, nodes=None):
        '''init'''
        super(KafkaHash, self).__init__(nodes)
        self.serverNodes = nodes
        self.disableNodes = []
        # timer interval
        self.interval = interval
        self.brokerThread = None
        self._brokerFlag = False
        self._globalLog = globalLog

    def addNodes(self, nodes):
        '''add nodes list
           if nodes is signal string, call add_node.
        '''
        for node in nodes:
            self.add_node(node)
            self.serverNodes.append(node)
            self.disableNodes.remove(node)
        # remove dumplicate elements
        self.serverNodes = list(set(self.serverNodes))

    def removeNodes(self, nodes):
        '''delete nodes list'''
        for node in nodes:
            self.remove_node(node)
            self.serverNodes.remove(node)
            self.disableNodes.append(node)
        # remove dumplicate elements
        self.disableNodes = list(set(self.disableNodes))

    def getBrokers(self):
        '''get all enable broker'''
        return self.serverNodes

    def getBroker(self, key):
        '''get enable broker'''
        return self.get_node(key)

    def _brokerResume(self, *args, **kwargs):
        '''
        Timer, function:check disable broker if or not enable
        '''
        while True:
            newEnableNodes = []
            for node in self.disableNodes:
                try:
                    KafkaClient(node)
                except KafkaUnavailableError:
                    continue
                else:
                    self._brokerFlag = True
                    newEnableNodes.append(node)
            # add nodes
            self.addNodes(list(set(newEnableNodes)))
            # sleep
            time.sleep(self.interval)

    def isKafkaNodes(self):
        '''
        Judge disable kafka node's status
        @这里就不关注共享资源锁问题了，没什么大问题
        '''
        self._brokerFlag = False if self._brokerFlag else self._brokerFlag
        return self._brokerFlag

    def startThread(self):
        '''run'''
        # broker resume thread
        self.brokerThread = threading.Thread(target=self._brokerResume)
        self.brokerThread.start()

class BaseKafkaConsumer(object):
    '''kafka consumer
    功能：
        消息消费者实例化该类，通过该类来实现消息的订阅
    细节：
        1）实例化类之后，不再关注各个brokers情况；
        2）消费者将消息拉出并存入队列中
        3）队列处理线程负责处理所有的消息
    '''
    def __init__(self, nodes):
        '''
        @nodes:所有brokers列表，例如[192.168.0.1:9093,]
        '''
        # kafka object
        self._kafkaHash = KafkaHash(1200, nodes)
        self._kafkaHash.startThread()
        self._kafkaConsumer = None
        self._topicDist = {
                'nginx'     :'NGINX_MONITOR',
                'basic'     :'BASIC_MONITOR',
                'java'      :'JAVA_MONITOR',}
        # brokers nodes
        self._brokerNodes = nodes

    def consumerMsg(self, inputQueue):
        '''handle nginx data'''
        self._nginxConsumer = KafkaConsumer(
                self._topicDist['nginx'], self._topicDist['basic'],
                self._topicDist['java'],
                bootstrap_servers=self._brokerNodes)
        # Infinite iteration
        for msg in self._nginxConsumer:
            inputQueue.put(msg)
            self._nginxConsumer.task_done(msg)
        # mark
        self._nginxConsumer.commit()

    def start(self):
        '''start'''
        self._run()

    def _run(self):
        '''start'''
        # get all brokers
        self.servernodes = self.kafkaHash.getBrokers()

        #monitorList:topic 线程列表,['nginx', 'java', 'basic']
        monitorList = [self._nginx, self._java, self._basic]
        for monitor in monitorList:
            threadT = threading.Thread(target=monitor) 
            threadT.daemon = True
            threadT.start()
            self.threadList.append(threadT)

        # waitting thread
        for t in self.threadList:
            t.join()

class KafkaProducer(object):
    '''kafka producer
    功能：
        消息发布者实例化该类，通过该类来实现消息的发布，即
        对KeydProducer类的封装
    细节：
        1）消息发布者实例化类之后，不再关注各个brokers情况；
        2）共有接口：send_message
        3）如果某一个当前broker宕机，类的恢复操作对发布者隐藏
    '''
    def __init__(self, brokers, brokerkey):
        '''init
        @nodes:所有已知的brokers信息，例如：[192.168.101.1:9093,]
        @key:和当前生产者匹配的信息：主机名 + 类型名(nginx,java,...)
        '''
        # broker key
        self._bkey = brokerkey
        # producer key
        self._pIndex = 0
        self._pIndexRange = 10
        self._pkey = [self.bkey + str(i) \
                for i in range(self._pIndexRange)]
        # kafka object
        self._kafkaHash = KafkaHash(3600, brokers)
        self._kafkaHash.startThread()
        self._broker = self.kafkaHash.getBroker(self._bkey) 
        self._kafkaClient = KafkaClient(self._broker)
        self._producer = KeyedProducer(self._kafkaClient)

    def send_message(self, topic, message):
        '''publish message to kafka
        @else：
            在每一次发送消息之后，会验证当前brokers列表是否发生变化
        '''
        try:
            if topic in self._kafkaClient.topics:
                self.producer.send_messages(topic, 
                        self.pkey[self._pIndex], message)
                self._pIndex = (self._pIndex+1)%self._pIndexRange
        except Exception,msg:
            self._globalLog.getError().log(self._globalLog.ERROR, \
                    "Publisher send message failed, msg:%s"%(msg))
            self._removeKafkaNodes()
            self.send_message()
        else:
            if self.kafkaHash.isKafkaNodes():
                self._resetKafkaClient()

    def _resetKafkaClient(self):
        '''reset broker'''
        self._broker = self.kafkaHash.getBroker(self._bkey) 
        self._kafkaClient = KafkaClient(self._broker)
        self._producer = KeyedProducer(self._kafkaClient)

    def _removeKafkaNodes(self):
        '''remove disable broker and reset'''
        self._kafkaHash.removeNodes([self._broker])
        self._resetKafkaClient()

