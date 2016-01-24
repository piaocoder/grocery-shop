#!/usr/bin/env python

def test1():
    import repeImport
    print 'Test1++++++++++++++++++++++++++++++'

if __name__ == '__main__':
    """main"""
    print 'Main==========================='
    import time
    time.sleep(3)
    test1()
