#coding:utf-8
'''
    简单的测试:run()和start()函数是如何构造的？
'''

class StartTest(object):
    def __init__(self):
        '''test run and start'''
        self.testVar = ''

    def display(self):
        '''判断self.testVar是否发生变化'''
        print self.testVar

    def run(self):
        '''run'''
        self.testVar = 'xxxxxxxxxxxxxxxxxxx'

if __name__ == '__main__':
    '''main'''
    startTest = StartTest()
    startTest.start()
    startTest.display()
