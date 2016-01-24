#!/usr/bin/env python  
# -*- coding:utfjob -*-  
import socket  
  
class NetServer(object):  
    def tcpServer(self):  
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        sock.bind(('', 9527))       # 绑定同一个域名下的所有机器  
        sock.listen(5)  
          
        while True:  
            clientSock, (remoteHost, remotePort) = sock.accept()  
            # 接收客户端的ip, port 
            print("[%s:%s] connect" % (remoteHost, remotePort))      
              
            revcData = clientSock.recv(1024)  
            sendDataLen = clientSock.send("this is send  data from server")  
            print "revcData: ", revcData  
            print "sendDataLen: ", sendDataLen  
              
            clientSock.close()  
              
if __name__ == "__main__":  
    netServer = NetServer()  
    netServer.tcpServer()  
