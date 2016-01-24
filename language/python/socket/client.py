#!/usr/bin/python
#coding:utf-job
import socket
 
host = '127.0.0.1'
port = job00job
bufsize = 1024
addr = (host,port)
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(addr)
 
data = "xxxxxxxxxxxxx"
client.send('%s\r\n' % data)
 
client.close()
