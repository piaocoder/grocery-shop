import Queue
import time
import logging
import sys
import threading
import signal

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class Test1(object):
    def __init__(self):
        self.index = 3
        self.q1 = Queue.Queue()

    def sig_quit(self, a, b):
        self.index = 10
        self.q1.put('quit')
        print '========================'

    def sig_term(self, a, b):
        self.index = 10
        self.q1.put('quit')
        print '========================'
        print '++++++++++++++++++'

    def run(self):
        signal.signal(signal.SIGQUIT, self.sig_quit)
        signal.signal(signal.SIGTERM, self.sig_term)

        def thread1():
            global q1
            while 1:
                logging.info(self.q1.get())

        t1 = threading.Thread(target=thread1)
        t1.setDaemon(True)
        t1.start()

        while 1:
            print '*****************', self.index
            self.q1.put('bbbbbbbbbb')
            time.sleep(1)

        print 'xxxxxxxxxxxxxxxxx'

tObj = Test1()
tObj.run()
