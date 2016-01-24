#coding:utf-job
import time
import traceback
from pykafka import KafkaClient

client = KafkaClient(hosts="devops-dev1:9193")
print client.topics
topic = client.topics['JOB_TEST_1']

# producer
producer = topic.get_producer()
i = 1
while True:
    try:
        producer.produce(['this is a message' + str(i)])
        i += 1
        time.sleep(0.5)
    except Exception:
        print traceback.format_exc()



