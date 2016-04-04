#!/usr/bin/env python
# coding:utf8
import socket


g_dstAddress = ('192.168.2.1', 10100)
g_srcAddress = ('192.168.2.11', 10000)


def init_port():
    global g_srcAddress
    socketfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketfd.bind(g_srcAddress)
    return socketfd


def send_package():
    socketfd = init_port()
    if not socketfd:
        print 'Bind tcp client failed.'
        exit(-1)
    socketfd.connect(g_dstAddress)
    for i in xrange(10):
        socketfd.send('This is {0} times test.'.format(i))

    socketfd.close()


if __name__ == '__main__':
    send_package()
