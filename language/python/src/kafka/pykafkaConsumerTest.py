#!/usr/bin/env python
#coding:utf-8
from pykafka import KafkaClient
client = KafkaClient(hosts="devops-dev1:9193")
topic = client.topics['JOB_TEST_1']


# consumer
zookeeper_str = 'registry1.dubbo.host:2181'
consumer = topic.get_balanced_consumer(
        auto_commit_enable=True,
        zookeeper_connect=zookeeper_str)
for message in consumer:
    if message is not None:
        print message.offset, message.value


if __name__ == '__main__':
    pass
