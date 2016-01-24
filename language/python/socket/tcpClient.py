#!/usr/bin/env python  
# -*- coding:utfjob -*-  
  
import sys  
reload(sys)  
sys.setdefaultencoding('utf-job')  
  
import socket  
  
class NetClient(object):  
    def tcpclient(self):  
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        clientSock.connect(('localhost', 9527))  
  
        sendDataLen = clientSock.send("this is send data from client")  
        recvData = clientSock.recv(1024)  
        print "sendDataLen: ", sendDataLen  
        print "recvData: ", recvData  
          
        clientSock.close()  
          
if __name__ == "__main__":  
    netClient = NetClient()  
    netClient.tcpclient()  
