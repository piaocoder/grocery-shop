#coding:utf-8
import sys
import time
from kafka import (
    KafkaConsumer, KafkaClient, KeyedProducer, )
from kafka.common import (
    LeaderNotAvailableError, ConsumerTimeout,
    KafkaUnavailableError, FailedPayloadsError, )


class BaseKafkaConsumer(object):
    '''kafka consumer
    $problems:not exists
    '''
    def __init__(self, brokers, topics, globalLog):
        '''Initialize.

        :brokers:   brokers list, for example:[192.168.0.1:9093,]
        :topics:    topics list
        '''
        self._kafkaConsumer = None
        self._brokers = brokers
        self._topics = topics
        self._stop = False
        self._commit = False
        self._globalLog = globalLog
        self._groupId = 'job_consumer_group'
        self.init_kafka()

    def init_kafka(self):
        '''Initialize kafka objects.'''
        try:
            self._kafkaConsumer = KafkaConsumer(
                *self._topics,
                fetch_min_bytes=1024,
                group_id=self._groupId,
                bootstrap_servers=self._brokers,
                consumer_timeout_ms=10 * 1000
            )
        except KafkaUnavailableError:
            self._globalLog.sendError(
                self._globalLog.ERROR,
                "Consumer, all brokers:{0} close, "
                "please checkout.".format(self._brokers))

    def get_message(self):
        '''Get msg from kafka.'''
        try:
            return self._kafkaConsumer.fetch_messages()
        except (KafkaUnavailableError, LeaderNotAvailableError), msg:
            self._globalLog.sendError(
                self._globalLog.ERROR,
                "All brokers are unavailabled when get"
                "msg from kafka, msg:{0}".format(msg))
            self.init_kafka()
        except (ConsumerTimeout):
            self._globalLog.sendError(
                self._globalLog.ERROR,
                "Timeout when get msg from kafka.")
            return None
        except (AttributeError):
            self._globalLog.sendError(
                self._globalLog.ERROR,
                "Brokers disable when get msg from kafka, waitting!!")
            time.sleep(2)
            return None

    def stop_consumer(self):
        '''stop consumer msg'''
        self._stop = True

    def commit(self):
        '''commit'''
        self._kafkaConsumer.commit()

    def task_done(self, message):
        '''task_done'''
        self._kafkaConsumer.task_done(message)


class BaseKafkaProducer(object):
    '''kafka producer
    功能：
        消息发布者实例化该类，通过该类来实现消息的发布，即
        对KeydProducer类的封装
    '''
    def __init__(self, brokers, topic, globalLog):
        '''init
        @brokers:所有已知的brokers信息，例如：[192.168.101.1:9093,]
        '''
        # producer key
        self._pIndex = 0
        self._pIndexRange = 10
        # kafka object
        self._brokers = brokers
        self._kafkaClient = None
        self._producer = None
        self._topic = topic
        self._globalLog = globalLog
        self.init_kafka()

    def init_kafka(self):
        '''init brokers'''
        # create kafka client object
        for broker in self._brokers:
            try:
                self._kafkaClient = KafkaClient(broker)
            except (FailedPayloadsError, KafkaUnavailableError), msg:
                self._globalLog.sendError(
                    self._globalLog.ERROR,
                    "Brokers:{0}, broker:{1}, may be close, "
                    "please checkout, msg:{2}".format(
                        self._brokers, broker, msg))
                self._kafkaClient = None
            else:
                break
        if not self._kafkaClient:
            self._globalLog.sendError(
                self._globalLog.ERROR,
                "All brokers are unavailable, please checkout")
        else:
            # create producer object
            self._producer = KeyedProducer(self._kafkaClient)

    def send_message(self, keys, values):
        '''
        publish message to kafka
        @keys:hostname:timestamp
        @values:may be a dist or list
        @发布消息接口说明:
            keys格式    :主机名:时间戳，即hbase中的key键
            values      :已经构造好，准备发送到Hbase的字典数据，例如：
                {
                u'Row': [
                    {
                        u'key':'lg-main-nginx-bjc-001:201508221710',
                        u'Cell':[
                            {
                                u'column':'cpu.1',
                                u'timestamp':333333,
                                u'$':'2.333334',
                            },
                            {
                                u'column':'cpu.2',
                                u'timestamp':33333,
                                u'$':'3.333333',
                            },
                            ...
                        ],
                    },
                ]
                }
          详细例子，请见test/jobConsumerTest.py(由job.py修改而成):
            1)初始化BaseKafkaProducer对象（60行）
            2)设置当前producer的topics主题名(61行)
            3)发布消息，239行
           简单例子，请见producerTest.py文件
        '''
        # send message
        try:
            if self._topic in self._kafkaClient.topics and self._producer:
                self._producer.send_messages(self._topic, keys, values)
        except (FailedPayloadsError, KafkaUnavailableError), msg:
            self._globalLog.sendError(
                self._globalLog.ERROR,
                "Topic:{0} not found in {1}, "
                "msg:{2},all brokes are close?".format(
                    self._topic, str(self._kafkaClient.topics), msg))
            self.init_kafka()
        except Exception, msg:
            exc_type, _, exc_tb = sys.exc_info()
            self._globalLog.sendError(
                self._globalLog.ERROR,
                "Send msg to kafka failed. Exception type"
                ":{0}, msg:{1}".format(exc_type, msg))
            self.init_kafka()


if __name__ == '__main__':
    '''main'''
    baseKafkaProducer = BaseKafkaProducer(
        ['devops-dev1:9193', 'devops-dev1:9194'],
        'JOB_TEST')
    topicsList = ['JOB_TEST', 'JOB_TEST_1']
    baseKafkaConsumer = BaseKafkaConsumer(
        ['devops-dev1:9193', 'devops-dev1:9194'],
        *topicsList)
