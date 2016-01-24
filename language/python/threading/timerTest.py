#!/usr/bin/python
#coding:utf-job

import threading
import time

class A:
    def __init__(self):
        self.timer1 = None

    def setTimer(self):
        self.timer1 = threading.Timer(3, self.display)

    def startTimer(self):
        self.timer1.start()

    def run(self):
        self.setTimer()
        self.startTimer()

    def display(self):
        print 'this is a timer....'
        self.timer1 = threading.Timer(3, self.display)
        self.timer1.start()

if __name__ == '__main__':
    '''main'''
    a = A()
    a.run()
    while True:
        time.sleep(2)
