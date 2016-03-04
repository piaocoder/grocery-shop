#!/usr/bin/env python
#coding:utf-8
import fcntl
import os, time

def normalFile():
    '''Lock a normal file'''
    FILE = "counter.txt"

    if not os.path.exists(FILE):
        # create the counter file if it doesn't exist
        file = open(FILE, "w")
        file.write("0")
        file.close()

    for i in range(20):
        file = open(FILE, "r+")     #由于flock生成的是劝告锁，不能阻止进程对文件的操作，所以这里可以正常打开文件
        #为了避免同时操作文件，需要程序自己来检查该文件是否已经被加锁。这里如果检查到加锁了，进程会被阻塞    
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)   
        print 'acquire lock'
        counter = int(file.readline()) + 1
        file.seek(0)
        file.write(str(counter))
        print os.getpid(), "=>", counter
        time.sleep(2)
        file.close() # unlocks the file
        print 'release lock'

def DirectoryFile():
    '''Lock a normal file'''
    FILE = "testDirectory"

    if not os.path.exists(FILE):
        os.mkdirs(FILE)

    for i in range(20):
        #为了避免同时操作文件，需要程序自己来检查该文件是否已经被加锁。这里如果检查到加锁了，进程会被阻塞    
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)   
        print 'acquire lock'
        counter = int(file.readline()) + 1
        file.seek(0)
        file.write(str(counter))
        print os.getpid(), "=>", counter
        time.sleep(2)
        file.close() # unlocks the file
        print 'release lock'


if __name__ == '__main__':
    '''main'''
    normalFile()
