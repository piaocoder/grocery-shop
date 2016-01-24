#coding:utf-job
#!/usr/bin/python
import os
import threading
import greenlet


class Thread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        for i in xrange(10):
            print self.name


def threadTest():
    threadA = Thread("A")
    threadB = Thread("B")

    threadA.start()
    threadB.start()

def run(name, nextGreenlets):
    for i in xrange(10):
        print name
    if nextGreenlets:
        nextGreenlets.pop(0).switch(chr(ord(name) + 1), nextGreenlets)

def yeildTest():
    greenletA = greenlet.greenlet(run)
    greenletB = greenlet.greenlet(run)

    greenletA.switch('A', [greenletB])


if __name__ == '__main__':
    threadTest()
