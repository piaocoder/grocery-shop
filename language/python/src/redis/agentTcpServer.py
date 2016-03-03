#/usr/bin/python
#coding:utf-8
import os
import sys
import redis
import socket
import select
import struct
import atexit
import signal

# set root directory
package_path = os.getcwd() + '/../'
sys.path.append(package_path)

from basepackage.baseConfig import BLACK_FILE,BLACK_PIPE
from basepackage.baselog import globalLog
from agentDaemon import Daemon

class RedisCommnicate():
    '''operator between redis with client'''
    def __init__(self, host='127.0.0.1', port=6379, maxnum = 2000000):
        '''init'''
        try:
            self._client = redis.Redis(host, port, db=0)
            self._pipeline = self._client.pipeline()   # transation
        except Exception:
            globalLog.getError().log(globalLog.ERROR, 'connect redis server failed!')
            sys.exit(-1)
        self._maxnum = maxnum
        # redis key which store black list 
        self._attackKey = 'nginx.blacklist'
    
    def _addRecord(self, searchkey):
        '''add a new connection to redis'''
        # add command to pipe
        if not self._client.get(searchkey):
            self._pipeline.setex(searchkey, 0, 60)
        else:
            self._pipeline.incr(searchkey)
            self._pipeline.get(searchkey)  
        # execute command
        try:
            return int(self._pipeline.execute()[-1])
        except Exception:
            globalLog.getError().log(globalLog.ERROR, \
                    'AgentServer:execute redis command failed.')
            return self._maxnum

    def _writeBlackList(self, attack):
        '''write black list to main redis'''
        self._client.sadd(self._attackKey, attack)

    def addRecord(self, ip):
        '''add a new connection to redis'''
        # set searchkey
        globalLog.getError().log(globalLog.DEBUG, \
                "searchkey:%s"%(ip))
        # get info from redis and store info into redis
        return True if self._addRecord(ip) >= self._maxnum else False

class AgentServer(Daemon):
    '''A TCP socket server which commnicate with nginx'''
    def __init__(self, redisServer, redisPort, address='127.0.0.1', port=8008, \
            pid='/data/agentServer/agent.pid'):
        '''init'''
        super(AgentServer, self).__init__(pidfile=pid)
        self._sock = None
        self._packageList = [
                '_handleModuleRedis',           # map REDIS_PACKAGE macro in C
                ]
        self._redisConn = RedisCommnicate(redisServer, redisPort)
        self._address = address
        self._port = port
        self.poller = None
        self.fdToSocket = None
        self._attackPip = None
    
    def _createPipe(self, filename):
        '''Create a pipe'''
        try:
            if os.path.exists(filename) is False:
                os.mkfifo(filename)
            self._attackPip = open(filename, 'w')
            globalLog.getError().log(globalLog.DEBUG, \
                    'Create pipe file successful')
        except (OSError, Exception), msg:
            globalLog.getError().log(globalLog.ERROR, \
                    'Create and Open FIFO failed, %s'%msg)
            sys.exit(-1)

    def _bindSocket(self, ip, port):
        '''bind socket'''
        address = (ip, port)
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._sock.bind(address)
            self._sock.setblocking(0)
            self._sock.listen(10)
        except Exception, msg:
            globalLog.getError().log(globalLog.ERROR, \
                    'AgentServer:bind socket %s failed, %s'%(ip,msg))
            sys.exit(-1)
        globalLog.getError().log(globalLog.DEBUG, 'Bind %s successful.'%ip)

    def _writeReject(self, data):
        '''write attack information into file'''
        # create attackfile
        try:
            if os.path.exists(BLACK_FILE) is False:
                open(BLACK_FILE, 'w').close()
            if os.path.exists(BLACK_PIPE) is False:
                os.mkfifo(BLACK_PIPE)
        except Exception,msg:
            globalLog.getError().log(globalLog.WARNING, \
                    '%s:Handle attack file %s.'%(msg, BLACK_FILE))
            return

        # write info into attack file(pipe and normal file)
        try:
            # Whether existed blacklist ip
            with open(BLACK_FILE, 'r') as reFd:
                strbuf = reFd.read()
                if data in strbuf:
                    return
            # write black into file
            with open(BLACK_FILE, 'a') as inFd:
                inFd.write(data+'\n')
            # write into pipe
            self._attackPip.write(data)
            self._attackPip.flush()
        except Exception, msg:
            globalLog.getError().log(globalLog.WARNING, \
                    'Warning:replace file failed(%s)'%(msg))

    def _handleModuleRedis(self, len, data):
        '''handle redis package'''
        globalLog.getError().log(globalLog.DEBUG, \
                "HandleRedis:blackip:%s"%data)
        #self._redisConn.addRecord(info[0], info[1])
        if self._redisConn.addRecord(data):
            globalLog.getError().log(globalLog.INFO, \
                    "Write blacklist:%s"%data)
            self._writeReject(data)

    def _handleModule(self, type, len, data):
        '''handle tcp socket package
           package format:
           {
                package-Type        00
                package-length      0018
                data(ip/token)      basic package-length's value
           }
        '''
        # call function use attribute
        getattr(self, self._packageList[type])(len, data)

    def _recvPackageFromClient(self, conn):
        '''conmmnicate between server and client'''
        preLength = 8# len(type + data_len)，结构体本身的长度
        #import pdb
        #pdb.set_trace()
        # receive package (hexadecimal number)
        data = conn.recv(preLength)
        if not data:
            globalLog.getError().log(globalLog.DEBUG, \
                    'Received Null string, client close.')
            return False
        elif len(data) != preLength:
            globalLog.getError().log(globalLog.DEBUG, \
                    'Package too small, drop package.')
            return True
        (type, totalLen) = struct.unpack('<ii', data)
        globalLog.getError().log(globalLog.DEBUG, \
                "Package Type:%d, PackageLeng=%d"%(type, totalLen))
        # receive package(content)
        data = conn.recv(totalLen)
        if not data:
            globalLog.getError().log(globalLog.ERROR, \
                    'Received Null string, perhaps client close.')
            return False
        elif len(data) != totalLen:
            globalLog.getError().log(globalLog.DEBUG, \
                    'Package too small, drop package.')
            return True
        # handle
        globalLog.getError().log(globalLog.DEBUG, "Pacakge Content=%s"%data)
        self._handleModule(type, totalLen, data)
        return True

    def _receivePackage(self, poller, conn, fdToSocket, readOnly):
        '''receive package'''
        try:
            if conn is self._sock:
                # add clifd to events 
                globalLog.getError().log(globalLog.DEBUG, 'A new connection come on.') 
                conn, cliAddr = conn.accept()
                conn.setblocking(0)
                fdToSocket[conn.fileno()] = conn
                poller.register(conn, readOnly)
                return True
            else:
                # receive data
                return False if not self._recvPackageFromClient(conn) else True
        except Exception, msg:
            globalLog.getError().log(globalLog.ERROR, msg)
            return False

    def waitConnection(self, poller, readOnly, fdToSocket, timeout):
        ''''''
        # poll timeout
        events = poller.poll(timeout)
        for fd, flag in events:
            # retrieve the actual socket from its file descriptor
            s = fdToSocket[fd]
            # handle inputs
            if (flag & (select.POLLIN | select.POLLPRI)) and \
                    not self._receivePackage(poller, s, fdToSocket, readOnly):
                poller.unregister(s)
                s.close()
                del fdToSocket[fd] 
            elif flag & (select.POLLHUP | select.POLLERR):
                globalLog.getError().log(globalLog.ERROR, 'Client close connection') 
                poller.unregister(s)
                s.close()

    def handle(self):
        '''waitting client connection'''
        # commonly used flag sets
        timeout = 1000
        readOnly = (select.POLLIN | select.POLLPRI|
                select.POLLHUP | select.POLLERR)
        # set up the poller
        self.poller = select.poll()
        self.poller.register(self._sock, readOnly)
        # map file descirptors to socket objects
        self.fdToSocket = {
                self._sock.fileno():self._sock,
                }
        # communicate
        while True:
            try:
                self.waitConnection(self.poller, readOnly, self.fdToSocket, timeout)
            except Exception,msg:
                globalLog.getError().log(globalLog.ERROR, \
                        'Exception in server handle:%s'%msg);

    def doExit(self):
        '''close all'''
        if self._attackPip:
            self._attackPip.close()

    def signalExit(self, a, b):
        '''close all'''
        if self._attackPip:
            print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX----'
            self._attackPip.close()
        print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        sys.exit(-1)
        
    def run(self):
        '''run server as daemon process'''
        # signal handle
        signal.signal(signal.SIGQUIT, self.signalExit)
        signal.signal(signal.SIGTERM, self.signalExit)
        signal.signal(signal.SIGINT,  self.signalExit)
        # bind
        self._createPipe(BLACK_PIPE)
        self._bindSocket(self._address, self._port)
        self.handle()

if __name__ == '__main__':
    '''main'''
    # daemon process
    agentServer = AgentServer('172.16.161.253', 6379, pid='/tmp/agent.pid')
    atexit.register(agentServer.doExit)
    agentServer.run()
    '''
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:  
            agentServer.start()  
        elif 'stop' == sys.argv[1]:  
            agentServer.stop()  
        elif 'restart' == sys.argv[1]:  
            agentServer.restart()  
        else:  
            print "Unknown command"  
            sys.exit(2)  
        sys.exit(0)  
    else:  
        print "usage: %s start|stop|restart" % sys.argv[0]  
        sys.exit(2)  
        '''
