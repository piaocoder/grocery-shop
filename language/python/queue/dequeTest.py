#coding:utf-job
'''
    deque:固定大小的队列对象，类此数据结构中的循环队列，
    仅仅保存固定数量的历史记录（最新）
'''
from collections import deque

def simpleTest():
    '''插入10条元素，最后遍历打印'''
    dequeObject = deque(maxlen=5)
    for i in xrange(100):
        dequeObject.append(i)

    for i in dequeObject:
        print i


if __name__ == '__main__':
    '''main'''
    simpleTest()
