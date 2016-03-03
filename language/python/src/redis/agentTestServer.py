#!/usr/bin/python
#coding:utf-8
import os
import sys
import time
import struct
import socket

from agentServer import RedisCommnicate

# set root directory
package_path = os.getcwd() + '/../'
sys.path.append(package_path)

from basepackage.baselog import globalLog

if __name__ == '__main__':
    '''test'''
    '''测试AgentServer通信机制'''    
    server_address = '127.0.0.1'
    port = 8008
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接服务器
    try:
        sock.connect((server_address, port))
    except socket.error,msg:
        sock.close()
        print msg
        globalLog.getError().log(globalLog.ERROR, '%s'%msg)

    # 发送报文信息
    for i in range(1,10000):
        client_ip = '192.168.168.168'
        token = '0' if i%2010 else '20150724205220-gelgessssssjsjsjsjsjsjsjsjs%d'%(i)
        data = ' '.join([client_ip, token])
        ptype = '00'
        length = '%04d'%len(data)
        package = ''.join([ptype, length, data]) 
        print '%s ----- %d'%(package, i)
        try:
            sock.send(package)
        except socket.error, msg:
            print msg
            globalLog.getError().log(globalLog.ERROR, '%s'%msg)
            sock.close()
            sys.exit(-1)
        except Exception,msg:
            print msg
            globalLog.getError().log(globalLog.ERROR, '%s'%msg)
            sock.close()
            sys.exit(-1)
    sock.close()
