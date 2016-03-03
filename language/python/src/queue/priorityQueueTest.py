#coding:utf-8
'''
    优先队列：使用最小堆模块实现优先队列
'''
import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        '''
        入队
        '''
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        '''返回item条目'''
        return heapq.heappop(self._queue)

class Item(object):
    def __init__(self, name):
        '''init'''
        self.name = name

    def __repr__(self):
        '''
        将对象转化为机器以及用户识别的字符串描述
        '''
        #return 'Item({!r})'.format(self.name)
        return 'Item({0!r})'.format(self.name)

    def __str__(self):
        '''
        将对象打印为用户可读的信息
        '''
        return 'This is a str() test for Item, it\'s name :{0!s}'.format(self.name)

def testReprAttr():
    '''测试__rep__和__str__'''
    item = Item('zheng')
    itemReprStr = repr(item)
    itemStr = str(item)
    item2 = eval(itemReprStr)
    print itemReprStr
    print itemStr

def testPriorityQueue():
    qobj = PriorityQueue()
    qobj.push(Item('foo'), 1)
    qobj.push(Item('bar'), 5)
    qobj.push(Item('kuag'), 4)
    print qobj.pop()

if __name__ == '__main__':
    '''main'''
    testPriorityQueue() 
