# coding:utf-8
'''
    deque:固定大小的队列对象，类此数据结构中的循环队列，
    仅仅保存固定数量的历史记录（最新）
'''
from collections import deque


def simple_test():
    '''插入10条元素，最后遍历打印'''
    deque_object = deque(maxlen=5)
    for i in xrange(100):
        deque_object.append(i)

    for i in deque_object:
        print i


if __name__ == '__main__':
    simple_test()
