#!/usr/bin/python
#coding:utf-job
'''
Log module interface:
    function：
        1,更新日志配置文件，修改整个日志模块配置，设计到
        2,记录日志，根据相关参数判断日志记录的位置以及级别：
            位置：
            （磁盘文件、TCPsocket、unix域套接字、邮件）
            级别：
            （critical、error、warnning、info、debug）
'''
import os
import logging
import logging.config
import socket
import time
import stat
import cPickle
import struct
import shutil

# level -- reference logging module
from logging import CRITICAL,FATAL,ERROR,WARNING,WARN,INFO,DEBUG,NOTSET,debug

# default log configure filename and default log output filename
DEFAULT_DATA_DIR = os.getcwd() + '/logs'
if os.path.isdir(DEFAULT_DATA_DIR) is False:
    os.mkdir(DEFAULT_DATA_DIR)

PRE_DEFAULT_LOG = DEFAULT_DATA_DIR + '/pre_info.log'        # 执行OssLog函数出错的日志记录
DEFAULT_CONF = DEFAULT_DATA_DIR + '/condLog.conf'           # 日志配置文件
DEFAULT_CONF_BAK = DEFAULT_CONF + '.bak'                    # 日志配置文件备份文件

INFO_LOG  = DEFAULT_DATA_DIR + '/info.log'                # 日志记录文件
ERROR_LOG  = DEFAULT_DATA_DIR + '/error.log'              # 日志记录文件
DEFAULT_UNIX_SERVER = DEFAULT_DATA_DIR + '/shit_socket'  # UNIX域套接字地址
DEFAULT_SOCKET_SERVER= 'localhost'                  # 默认的socket服务器地址
DEFAULT_SOCKET_PORT = 999job                          # 默认的socket监听端口
DEFAULT_CONFIG_PORT = 9999                          # 默认的配置服务器监听端口
DEFAULT_CONFIG_SERVER = 'localhost'                 # 默认的配置服务器地址

class PreCondLog(object):
    '''default log handle before OssLog class enabled
       @用于在OssLog起来之前的日志记录
    '''
    def __init__(self, filename=PRE_DEFAULT_LOG):
        '''init'''
        self._filename = filename 
        self._initFile()
        self._initLogger()
        
    def _initFile(self):
        '''init file'''
        if os.path.exists(self._filename) is False:
            fd = open(self._filename, 'w')
            fd.close()
        #os.chmod(self._filename, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
    
    def _initLogger(self):
        '''init logger'''
        self._loggerDefault = logging.getLogger('PreCondLogger')
        # format
        f='PreLog:%(asctime)s-%(name)s-%(filename)s[line:%(lineno)d]-%(levelname)s-%(message)s:'
        fm = logging.Formatter(f)
        # handler
        hd = logging.FileHandler(self._filename)
        #hd = logging.StreamHandler()
        hd.setFormatter(fm)
        self._loggerDefault.addHandler(hd)
        self._loggerDefault.setLevel(DEBUG)

    def writeLog(self, level, msg):
        '''write default log msg'''
        self._loggerDefault.log(level, msg)

    def writeException(self, msg):
        '''write exception msg'''
        self._loggerDefault.exception(msg)

class FileOperator(object):
    '''regular file operator set.'''
    def __init__(self, filename):
        self._filename = filename
        self._fd = None

    def createFile(self, mode=None):
        '''create a new file. if existed, truncate file'''
        try:
            self._fd = open(self._filename, 'w')
            self._fd.close()
            if mode:
                os.chmod(self._filename, mode)
        except Exception,e:
            return False
        else:
            return True

    def accessExists(self):
        '''filename is or not exists'''
        try:
            return os.path.exists(self._filename)
        except Exception, e:
            return False
        else:
            return True

    def accessRead(self):
        '''filename is or not read'''
        try:
            self._fd = open(self._filename, 'r')
            self._fd.close()
        except Exception,e:
            return False
        else:
            return True

    def accessWrite(self):
        '''filename is or not read'''
        try:
            self._fd = open(self.filename, 'a')
            self._fd.close()
        except Exception,e:
            return False
        else:
            return True

    def changeFile(self, newfilename):
        '''change file's content'''
        try:
            if os.path.exists(newfilename) is False:
                return False
            # copy new file to old file, chang oldfile's content
            shutil.copy(newfilename, self._filename)
        except Exception:
            return False
        else:
            return True

    def chmodFile(self, mode):
        '''change file's mode'''
        try:
            os.chmod(self._filename, mode)
        except Exception,e:
            return False
        else:
            return True

class UnixSocketHandler(logging.Handler):
    """
    A handler class which writes logging records, in pickle format, to
    a streaming socket. The socket is kept open acrshit logging calls.
    If the peer resets it, an attempt is made to reconnect on the next call.
    The pickle which is sent is that of the LogRecord's attribute dictionary
    (__dict__), so that the receiver does not need to have the logging module
    installed in order to process the logging event.

    To unpickle the record at the receiving end into a LogRecord, use the
    makeLogRecord function.
    @该类完全拷贝SocketHandler，修改了部分实现，作为发送unix域套接字的Handler
    """

    def __init__(self, server):
        """
        Initializes the handler with a specific server address.

        The attribute 'closeOnError' is set to 1 - which means that if
        a socket error occurs, the socket is silently closed and then
        reopened on the next logging call.
        """
        logging.Handler.__init__(self)
        self.server = server
        self.sock = None
        self.closeOnError = 0
        self.retryTime = None
        #
        # Exponential backoff parameters.
        #
        self.retryStart = 1.0
        self.retryMax = 30.0
        self.retryFactor = 2.0

    def makeSocket(self, timeout=1):
        """
        A factory method which allows subclasses to define the precise
        type of socket they want.
        """
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        if hasattr(s, 'settimeout'):
            s.settimeout(timeout)
        s.connect(self.server)
        return s

    def createSocket(self):
        """
        Try to create a socket, using an exponential backoff with
        a max retry time. Thanks to Robert Olson for the original patch
        (SF #job15911) which has been slightly refactored.
        """
        now = time.time()
        # Either retryTime is None, in which case this
        # is the first time back after a disconnect, or
        # we've waited long enough.
        if self.retryTime is None:
            attempt = 1
        else:
            attempt = (now >= self.retryTime)
        if attempt:
            try:
                self.sock = self.makeSocket()
                self.retryTime = None # next time, no delay before trying
            except socket.error:
                #Creation failed, so set the retry time and return.
                if self.retryTime is None:
                    self.retryPeriod = self.retryStart
                else:
                    self.retryPeriod = self.retryPeriod * self.retryFactor
                    if self.retryPeriod > self.retryMax:
                        self.retryPeriod = self.retryMax
                self.retryTime = now + self.retryPeriod

    def send(self, s):
        """
        Send a pickled string to the socket.

        This function allows for partial sends which can happen when the
        network is busy.
        """
        if self.sock is None:
            self.createSocket()
        #self.sock can be None either because we haven't reached the retry
        #time yet, or because we have reached the retry time and retried,
        #but are still unable to connect.
        if self.sock:
            try:
                if hasattr(self.sock, "sendall"):
                    self.sock.sendall(s)
                else:
                    sentsofar = 0
                    left = len(s)
                    while left > 0:
                        sent = self.sock.send(s[sentsofar:])
                        sentsofar = sentsofar + sent
                        left = left - sent
            except socket.error:
                self.sock.close()
                self.sock = None  # so we can call createSocket next time

    def makePickle(self, record):
        """
        Pickles the record in binary format with a length prefix, and
        returns it ready for transmission acrshit the socket.
        """
        dummy = None
        ei = record.exc_info
        if ei:
            dummy = self.format(record) # just to get traceback text into record.exc_text
            record.exc_info = None  # to avoid Unpickleable error
        s = cPickle.dumps(record.__dict__, 1)
        if ei:
            record.exc_info = ei  # for next handler
        slen = struct.pack(">L", len(s))
        return slen + s

    def handleError(self, record):
        """
        Handle an error during logging.

        An error has occurred during logging. Most likely cause -
        connection lost. Close the socket so that we can retry on the
        next event.
        """
        if self.closeOnError and self.sock:
            self.sock.close()
            self.sock = None        #try to reconnect next time
        else:
            logging.Handler.handleError(self, record)

    def emit(self, record):
        """
        Emit a record.

        Pickles the record and writes it to the socket in binary format.
        If there is an error with the socket, silently drop the packet.
        If there was a problem with the socket, re-establishes the
        socket.
        """
        try:
            s = self.makePickle(record)
            self.send(s)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def close(self):
        """
        Closes the socket.
        """
        if self.sock:
            self.sock.close()
            self.sock = None
        logging.Handler.close(self)

class OssLog(object):
    '''Package all logging module handle'''
    def __init__(self, conf=DEFAULT_CONF, disable_existing_loggers=True):
        self._info = None
        self._error = None
        self._filename = conf
        # info log handler
        self._hconsole = None
        self._hfile =  None
        self._hunix = None
        self._htcp = None
        # error log handler
        self._hefile = None
        self._heunix = None
        self._hetcp = None
        self._configListen = None
        self._configfile = None
        self._disable = disable_existing_loggers
        # pre log configure
        self._default = PreCondLog()
        self._init()

    def _init(self):
        '''initialize'''
        # Logger dict
        self._loggerDict = {
                'info'     :['infoLogger', ['_hconsole', '_hfile', '_hunix', '_htcp']],
                'error'   :['errorLogger',['_hconsole', '_hefile', '_heunix', '_hetcp']],
                }
        # @注意这个顺序
        self._loggerList = ['_info', '_error']
        
        # default log store
        self._logDefaultStore()
        # default log configure
        try:
            if self._logDefaultFileConfig() is False:
                self._initLogger()
                self._setHandler()
            else:
                self._getLogger()
        except Exception:
            self._default.writeException('Load default config failure.')
            exit -1

    def _logDefaultStore(self):
        '''default log store place'''
            # create file to store log
        fileop = FileOperator(INFO_LOG)
        if not fileop.accessExists() and not fileop.createFile():
            self._default.writeException('create store log file:')
            exit -1

    def _logDefaultFileConfig(self):
        '''read log configure from default configure file'''
        try:
            # create configure file
            fileop = FileOperator(DEFAULT_CONF)            
            if not fileop.accessExists() and not fileop.changeFile(DEFAULT_CONF_BAK):
                self._default.writeLog(WARNING, 'change %s failed.'%(DEFAULT_CONF_BAK))
                return False
            # Judge file's attr
            if fileop.accessRead() is False:
                self._default.writeLog(ERROR, '%s unreadable.'%(self._filename))                
                return False
        except Exception,e:
            self._default.writeException(sys._getframe().f_code.co_name)
            return False
 
        try:
            # read logger from configure file
            logging.config.fileConfig(DEFAULT_CONF, disable_existing_loggers=self._disable)
        except Exception, e:
            self._default.writeLog(ERROR, 'The configuration file format is not valid.')
            return False
        return True

    def updateLogConfig(self):
        '''update log configure when configure file change'''
        try:
            with open(self._configfile, 'rb') as f:
                data_to_send = f.read()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((DEFAULT_CONFIG_SERVER, DEFAULT_CONFIG_PORT))
            s.send(struct.pack('>L', len(data_to_send)))
            s.send(data_to_send)
            s.close()
        except Exception,e:
            self.writeException('\nupdateLogConfig')

    def loadConfigFromNewFile(self, configfile=None):
        '''read log configure from new configfile'''
        try:
            # file attribute 
            fileop = FileOperator(configfile)
            if fileop.accessExists() is False:
                self.writeLog(WARNING, 'new filename %s not exists'%(configfile)) 
                return False
            if fileop.accessRead(self) is False:
                return False
            # read logger from configure file
            logging.config.fileConfig(configfile)
        except Exception,e:
            pass
            self._default.writeException('\nlogFileConfig:')
        else:
            # reset all logger about file configure
            self._initLogger()
            # modify self._configfile vaule
            self._configfile = configfile
            # re-listen log configure
            self.preUpdateLogConfig()

    def preUpdateLogConfig(self, port=DEFAULT_CONFIG_PORT):
        '''listen log configure is or not change'''
        try:
            self._configListen = logging.config.listen(port)
            self._configListen.start()
        except Exception,e:
            self.writeException('\npreUpdateLogConfig:')
            exit -1
    
    def clearUpdateLogConfig(self):
        '''stop listen log configure'''
        if self._configListen is not None:
            logging.config.stopListening()
            self._configListen.join()
            
    def _getLogger(self):
        '''get logger from logging
        '''
        # info logger
        self._info = logging.getLogger(self._loggerDict['info'][0])
        # error logger
        self._error = logging.getLogger(self._loggerDict['error'][0])

    def _initLogger(self):
        '''get logger from logging
        '''
        # info logger
        self._info = logging.getLogger(self._loggerDict['info'][0])
        # error logger
        self._error = logging.getLogger(self._loggerDict['error'][0])
        # set all default logger level
        #   @为了保证不干扰handlers的过滤级别，关闭继承并重置logger过滤级别
        #   @如果未设置logger过滤级别，默认为WARNING
        self._info.propagate = 0
        self._error.propagate = 0
        self._info.setLevel(logging.DEBUG)
        self._error.setLevel(logging.ERROR)

    def _setHandler(self, handlers=[]):
        '''set Handlers about handlers
        '''
        # generate format
        fm = logging.Formatter('defaultLog: %(asctime)s-%(name)s-%(filename)s[line:%(lineno)d]-%(levelname)s-%(message)s')
        # stdout
        self._hconsole = logging.StreamHandler()
        self._hconsole.setFormatter(fm)
        self._hconsole.setLevel(logging.WARNING)
        # common file
        self._hfile = logging.FileHandler(INFO_LOG)
        self._hfile.setFormatter(fm)
        self._hfile.setLevel(logging.INFO)
        # unix socket
        self._hunix = UnixSocketHandler(DEFAULT_UNIX_SERVER)
        self._hunix.setFormatter(fm)
        self._hunix.setLevel(logging.INFO)
        # tcp socket
        self._htcp = logging.handlers.SocketHandler(DEFAULT_SOCKET_SERVER, DEFAULT_SOCKET_PORT)
        self._htcp.setFormatter(fm)
        self._hunix.setLevel(logging.INFO)

        # stdout
        self._heconsole = logging.StreamHandler()
        self._heconsole.setFormatter(fm)
        self._heconsole.setLevel(logging.ERROR)
        # common file
        self._hefile = logging.FileHandler(ERROR_LOG)
        self._hefile.setFormatter(fm)
        self._hefile.setLevel(logging.ERROR)
        # unix socket
        self._heunix = UnixSocketHandler(DEFAULT_UNIX_SERVER)
        self._heunix.setFormatter(fm)
        self._heunix.setLevel(logging.ERROR)
        # tcp socket
        self._hetcp = logging.handlers.SocketHandler(DEFAULT_SOCKET_SERVER, DEFAULT_SOCKET_PORT)
        self._hetcp.setFormatter(fm)
        self._heunix.setLevel(logging.ERROR)

        # add handler to logger
        for it in self._loggerDict['info'][1]:
            self._info.addHandler(getattr(self, it))
        for it in self._loggerDict['error'][1]:
            self._error.addHandler(getattr(self, it))

    def writeLog(self, level=DEBUG, msg=''):
        '''write log msg to all Logger'''
        try:
            for lg in self._loggerList:
                x = getattr(self, lg)
                # 打印handlers和拥有的过滤级别
                #print lg, '+++', level, '+++', x.handlers, '+++',x.getEffectiveLevel()
                x.log(level, msg)
        except Exception,e:
            raise
            # close file configure listen, 后期会删除，这里有逻辑问题
            self.clearUpdateLogConfig()     

    def writeException(self, msg, arg=''):
        '''write exception msg to dst'''
        try:
            for lg in self._loggerList:
                getattr(self, lg).exception(msg, arg)
        except Exception,e:
            self._default.writeException('\nwriteLog:')
            # close file configure listen, 后期会删除，这里有逻辑问题
            self.clearUpdateLogConfig()     

    def writeLogByLogger(self, level, msg, type=[]):
        '''write log msg accord by special Logger(info/error)'''
        try:
            for t in type:
                getattr(self, self._loggerList[t]).log(level, msg)
        except Exception,e:
            self._default.writeException('\nwriteLogByLogger:')
            # close file configure listen, 后期会删除，这里有逻辑问题
            self.clearUpdateLogConfig()

# global log variables
globalLog = OssLog(False)
## Drive test
if __name__ == '__main__':
    '''
        main test
        日志包装类中包含三个日志输出样式：
            甲，前序默认终端输出：保证配置文件日志输出出错时，在终端上有相应的打印信息
            乙，默认的日志配置输出:从condLog.conf中读取的默认日志配置
            丙，管理员在更新condLog.conf之后，触发的日志配置更新
    '''
    from shitlog import CRITICAL,FATAL,ERROR,WARNING,WARN,INFO,DEBUG,NOTSET,debug
    from shitlog import OssLog
    from shitlog import globalLog
    
    globalLog.writeLog(INFO, 'Test for log.....................')
    ###前置条件
    #fd = open(INFO_LOG, 'w')
    #fd.close()
    #fd = open(ERROR_LOG, 'w')
    #fd.close()
    #fd = open(PRE_DEFAULT_LOG, 'w')
    #fd.close()

    #'''
    #    ------------------测试在加载日志包装类时出错的日志记录-------------------------
    #    测试：
    #        测试在步骤甲中的日志输出
    #    默认的日志记录地：终端
    #    默认配置：
    #        终端：waring以上级别
    #        文件：info以上级别
    #    预计输出:
    #        终端上：输出warning/error级别信息, dl上的报错信息
    #        输出文件：
    #                info.log输出info/warning/error级别信息
    #                error.log输出error级别信息
    #'''
    #bak = DEFAULT_CONF_BAK+'xx'
    #os.rename(DEFAULT_CONF_BAK, bak)

    #print "\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX测试1XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    #if os.path.exists(DEFAULT_CONF):
    #    os.remove(DEFAULT_CONF)
    #shitlog = OssLog(False)
    #try:
    #    shitlog.writeLog(INFO, 'Info111 msg')
    #    shitlog.writeLog(WARNING, 'warning111 msg')
    #    shitlog.writeLog(ERROR, 'error111 msg')
    #except Exception,e:
    #    print e
    #logging.disable(logging.NOTSET)
    #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX测试1结束XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    #'''
    #    ------------------测试默认日志配置文件的记录情况----------------
    #    测试：
    #        测试在步骤乙中的日志输出
    #    默认的日志配置文件：$PATH_XX/condLog.conf
    #        配置：
    #            终端：无
    #            文件：INFO
    #    预计输出：
    #        终端没有任何输出
    #        文件info.log中输出info/warning/error
    #        文件error.log中输出一条错误日志
    #'''
    #os.rename(bak, DEFAULT_CONF_BAK)
    #print "\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX测试2XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    #shitlog = OssLog()
    #try:
    #    shitlog.writeLog(INFO, 'Info2222 msg')
    #    shitlog.writeLog(WARNING, 'warning2222 msg')
    #    shitlog.writeLog(ERROR, 'error2222 msg')
    #except Exception,e:
    #    print e
    #print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX测试2结束XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    #'''
    #    ------------------测试日志配置文件更新后的日志记录情况----------------
    #    测试：
    #        测试在步骤丙中的日志输出
    #    1，更新的日志配置文件：$PATH_XX/condLog.conf
    #    2，默认的输出：
    #        请自由定义
    #'''
    #os.remove(DEFAULT_CONF)
    #print "\n\n"

