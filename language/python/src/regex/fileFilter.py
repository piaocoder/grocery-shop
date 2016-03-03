#!/usr/bin/python
#coding:utf-8
'''
    功能：
        扫描指定的日志文件，提取匹配的信息并返回
    设定返回的缓存大小(returnMaxBuf):
        10M
    设定每次读取的字符串缓存大小为(readMaxBuf==returnMaxBuf):
        5M
    读取匹配信息的原则：
        1）仅仅读取系统抛出的异常，格式为：
            *Exception*
                at *.*.*.*
                at *.*.*.*
            Cause by:*Exception*
                at *.*.*.*
            （上面所例举看成一个原子栈信息）
            或者
            *Exception*
                at *.*.*.*
                at *.*.*.*
            *Exception*
                at *.*.*.*
            （后者其实是两个原子栈）
        2）保证读取或者匹配的信息是原子性的，宁可少返回，但保证原子性
        3）如果扫描一个单一的缓存后，获取的匹配信息不足returnMaxBuf，继续扫描
            下一个readMaxBuf，之后如果超额，则存入结果中并立刻更新返回。
        4) 如果单个原子性信息大小大于5M，扩大返回值
    存在的问题：
        如果在当前一段时间内（比如三个单位时间），每个单位时间内（10秒内）生成
        的日志信息过大（比如200M），其中的匹配信息都超过5M，那么可能造成告警
        信息无法及时有效的返回。
    基本流程：
        1打开指定的文件java.log；
        2读取readMaxBuf的信息，匹配并将整数个数的原子栈信息存入到returnBuf中. 
        3判断len(returnBuf)是否近似于returnMaxBuf：
            如果是，返回，结束本次调用；
            如果否，重复步骤2。
'''
import os
import re

from shitlog import CRITICAL,FATAL,ERROR,WARNING,WARN,INFO,DEBUG,NOTSET,debug
from shitlog import OssLog
from shitlog import globalLog

class FileFilter(object):
    '''过滤文件中的类'''
    def __init__(self, filename, maxbuf = 5242880):
        self._maxBuf = maxbuf
        self._filename = filename
        self._fd = None
        self._originstr = None
        self._pos = 0
        # init
        self._init()

    def _init(self):
        '''init'''
        try:
            self._fd = open(self._filename, 'rb')
        except Exception:
            globalLog.writeLog(WARNING, 'Read file %s failed.'%(self._filename))
            self._fd = None

    def _readBufBySize(self):
        '''read 5242880 bytes from file every once'''
        if self._fd is None:
            globalLog.writeLog(WARNING, 'File operator is None, %s existed?'%(self._filename))
            return False
        try:
            self.originstr = self._fd.read(self._maxBuf)
            fx = open('./logs/test', 'ab+')
            fx.write(self.originstr)
            fx.close()
        except Exception:
            globalLog.writeException('Read file %s'%(self._filename))
            return False
        print len(self.originstr), '+++++++++++++++++++++'
        if len(self.originstr) == 0:
            globalLog.writeLog(INFO, 'file\'s length is zero')
            return False

    def endUp(self):
        '''end to read file'''
        self._filename = None
        try:
            self._fd.close()
        except Exception:
            globalLog.writeLog(WARNING, 'close file failed!')
        self._fd = None
        self._pos = 0 
        self._originstr = None

    def filter(self, returnVal=[]):
        '''filter a and return value
        @retvalue格式:
            [
                (2000, '*****'),
                (3000, '*****'),
            ]
            其中每一个元祖表示一个原子栈信息；
            每一个元祖（字符串大小、字符串）;
        @目前的匹配查询正则表达式，主要分为：
            匹配：com.xxx.abException:xxx字段
            (\S*\.)+[a-z0-9A-Z_]*Exception:.*
            匹配：at org.cage.xxx(xxx.java.88)
            ((\n[ \t]*at *(\S*\.)+[a-z0-9A-Z_]*\(.*\))+)
            匹配：Caused by: com.xxx.abdException.xxx字段
            (\ncaused by: (\S*\.)+[a-z0-9A-Z_]*Exception:.*
            # 同上
            (\n[ \t]*at *(\S*\.)+[a-z0-9A-Z_]*\(.*\))+)+
        '''
        regexlist = [
            # pre match
            r'(\S*\.)+[a-z0-9A-Z_]*Exception:.*(\n[ \t]*at *(\S*\.)+[a-z0-9A-Z_]*\(.*\))+',
            # follow match
            r'(\ncaused by: (\S*\.)+[a-z0-9A-Z_]*Exception:.*(\n[ \t]*at *(\S*\.)+[a-z0-9A-Z_]*\(.*\))+)+',
            ]
        # read buf information
        while True:
            if self._readBufBySize() is False:
                return
            # get origin string's length
            buflen = len(self.originstr)
            print 'Test--------------buflen=%d-----------------------'%(buflen)
            for regexstr in regexlist:
                match = re.search(regexstr, self.originstr, re.IGNORECASE)
                if match is None:
                    self._pos = self._pos + buflen
                    continue
                # copy string 
                mstart = match.start()
                mend = match.end()
                print 'Match string is :%s'%(self.originstr[mstart:mend])

if __name__ == '__main__':
    '''main'''
    import pdb
    pdb.set_trace()
    fl = FileFilter('./out.log')
    
    num = 10
    for i in range(num):
        returnVal = []
        fl.filter(returnVal)
        for k in returnVal:
            print '\n=========================================================='
            print k
            
        
