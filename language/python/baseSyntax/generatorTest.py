#coding:utf-job
#!/usr/bin/python

import random

def get_data():
    return random.sample(range(10), 3)

def consume():
    running_sum = 0
    data_items_seen = 0

    for i in range(6):
        data = yield
        data_items_seen += len(data)
        running_sum += sum(data)
        print 'The running average is {0}'.format(\
                running_sum / float(data_items_seen))


def produce(consumer):
    '''生成器的使用场景特点：
        1，记录运行状况，例如最初的目的（随机数）
        2，生产端和消费端都是同步执行的（可以单线程执行的场景）
        3，在2的基础上，涉及大量内存的操作，为了优化空间，从而
            使用生成器，简化代码
        4，如果是IO密集型，请别用该用法
    '''
    while 1:
        data = get_data()
        print 'Produced {0}'.format(data)
        # generator的内置方法，将一个值发送给consumer生成器
        consumer.send(data)
        yield


if __name__ == '__main__':
    consumer = consume()
    consumer.send(None)
    producer = produce(consumer)

    for _ in range(10):
        print 'xxxxxxxxxxx'
        # 使用next来获取下一个值（内置函数）
        try:
            next(producer)
        except StopIteration,msg:
            break
