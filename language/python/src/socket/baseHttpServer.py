#!/usr/bin/python
#coding:utf-8
from BaseHTTPServer import BaseHTTPRequestHandler  #BaseHTTPRequestHandler类细分到处理每个协议的方法，这里是‘GET’方法的例子
import urlparse



class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):   #重写这个方法
        #import pdb
        #pdb.set_trace()
        parsed_path = urlparse.urlparse(self.path)
        print "============================================="
        print parsed_path
        print type(parsed_path)
        print parsed_path.query
        print "============================================="
        message_parts = [  #建立一个想要返回的列表
                'CLIENT VALUES:',    #客户端信息
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),  #返回客户端的地址和端口
                'command=%s' % self.command,  #返回操作的命令，这里比然是'get'
                'path=%s' % self.path,  #返回请求的路径
                'real path=%s' % parsed_path.path, #返回通过urlparse格式化的路径
                'query=%s' % parsed_path.query, #返回urlparse格式化的查询语句的键值
                'request_version=%s' % self.request_version, #返回请求的http协议版本号
                '',
                'SERVER VALUES:', #服务器段信息
                'server_version=%s' % self.server_version, #返回服务器端http的信息
                'sys_version=%s' % self.sys_version, #返回服务器端使用的python版本
                'protocol_version=%s' % self.protocol_version,  #返回服务器端使用的http协议版本
                '',
                'HEADERS RECEIVED:',
                ]
        for name, value in sorted(self.headers.items()):  #返回項添加头信息，包含用户的user-agent信息，主机信息等
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        self.send_response(200)  #返回给客户端结果，这里的响应码是200 OK，并包含一些其他信息
        self.end_headers() #结束头信息
        self.wfile.write(message) #返回数据
        return
if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('localhost', 8080), GetHandler)  #在本地8080端口上启用httpserver，使用自定义的GetHandler处理
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()  #保存程序一直运行

