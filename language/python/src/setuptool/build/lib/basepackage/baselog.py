#!/usr/bin/python
# coding:utf-8
import os
import sys
import string
import traceback
import logging
import logging.handlers
import re
import stat

from datetime import datetime
from logging import (CRITICAL, FATAL, ERROR, WARNING,
                     WARN, INFO, DEBUG, NOTSET)


class _LogConfig(object):
    """base log configure"""
    def __init__(self, rootpath, module):
        self.logdir = rootpath
        self.module = module
        self.confLogLevel = logging.DEBUG
        self.confLogFormat = (' %(levelname)s-%(asctime).19s-%(message)s:')

        self.logbase = self.logdir + '/%s.base.log' % (self.module)
        self.logdebug = self.logdir + '/%s.debug.log' % (self.module)
        self.logerror = self.logdir + '/%s.error.log' % (self.module)
        self._create_file()

    def _create_file(self):
        """Create file for logging."""
        try:
            if os.path.isdir(self.logdir) is False:
                os.makedirs(self.logdir)
            if os.path.exists(self.logbase) is False:
                open(self.logbase, 'w').close()
            if os.path.exists(self.logdebug) is False:
                open(self.logdebug, 'w').close()
            if os.path.exists(self.logerror) is False:
                open(self.logerror, 'w').close()
        except (OSError, IOError, Exception), msg:
            sys.stderr.write('_LogConfig:%s' % msg)
            sys.exit(-1)

    def _mod_authority(self):
        '''Modify file authority'''
        try:
            os.chmod(self.logdir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            os.chmod(self.logbase, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            os.chmod(self.logdebug, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            os.chmod(self.logerror, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        except Exception, msg:
            sys.stderr.write('User does not have '
                             'modify permissions, msg:%s\n' % msg)


class _LogDeal(object):
    """Logging when initialize _LogDeal class."""
    def __init__(self, logConfig):
        """init"""
        self._blcObject = logConfig
        self._filename = self._blcObject.logbase
        self._init_logger()

    def _init_logger(self):
        """init logger"""
        self._loggerBase = logging.getLogger('_LogDeal')
        fm = logging.Formatter(self._blcObject.confLogFormat)
        hd = logging.FileHandler(self._filename)
        hd.setFormatter(fm)
        self._loggerBase.addHandler(hd)
        self._loggerBase.setLevel(DEBUG)

    def log(self, level, msg):
        """write default log msg"""
        self._loggerBase.log(level, msg)

    def write_error(self, msg):
        """write default log msg"""
        self._loggerBase.log(logging.ERROR, msg)

    def write_debug(self, msg):
        """write default log msg"""
        self._loggerBase.log(logging.INFO, msg)


if hasattr(sys, 'frozen'):
    _srcfile = "logging%s__init__%s" % (os.sep, __file__[-4:])
elif string.lower(__file__[-4:]) in ['.pyc', '.pyo']:
    _srcfile = __file__[:-4] + '.py'
else:
    _srcfile = __file__
_srcfile = os.path.normcase(_srcfile)


def currentframe():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception
    except:
        return sys.exc_info()[2].tb_frame.f_back


class _BaseLog(object):
    """Package all logging module handle"""
    CRITICAL = CRITICAL
    FATAL = FATAL
    ERROR = ERROR
    WARNING = WARNING
    WARN = WARN
    INFO = INFO
    DEBUG = DEBUG
    NOTSET = NOTSET

    def __init__(self, rootpath, module):
        """Initialize class.

        :rootpath:  data root path.
        :module:    filename of log.
        """
        self.debugLg = None
        self.errorLg = None
        self._globalBaseLg = _LogDeal(_LogConfig(rootpath, 'common'))
        self.baseLgConfig = _LogConfig(rootpath, module)
        self._create_logger()

    def _create_logger(self):
        """Get logger from logging"""
        self.debugLg = logging.getLogger('infoLogger')
        [self.debugLg.removeHandler(h) for h in self.debugLg.handlers]
        self.debugLg.propagate = 0
        self.debugLg.setLevel(logging.DEBUG)

        self.errorLg = logging.getLogger('errorLogger')
        [self.errorLg.removeHandler(h) for h in self.errorLg.handlers]
        self.errorLg.propagate = 0
        self.errorLg.setLevel(logging.DEBUG)

        fm = logging.Formatter(self.baseLgConfig.confLogFormat)

        lh = logging.handlers.TimedRotatingFileHandler(
            self.baseLgConfig.logdebug, 'midnight')
        lh.setFormatter(fm)
        lh.setLevel(logging.DEBUG)
        self.debugLg.addHandler(lh)

        lh = logging.handlers.TimedRotatingFileHandler(
            self.baseLgConfig.logerror, 'midnight')
        #
        lh.setFormatter(fm)
        lh.setLevel(self.baseLgConfig.confLogLevel)
        self.errorLg.addHandler(lh)

    def removeRedundantLog(self, maxnum=7):
        """Remove randundant log and keep maxnum log.

        :maxnum:   max number of log's file.
        """
        logdir = self.baseLgConfig.logdir
        regexobj = re.compile(r'job\.\w*?\.log\.(\d{4}-\d{2}-\d{2})')
        nowtime = datetime.now()
        for file in os.listdir(logdir):
            matchobj = re.match(regexobj, file)
            if not matchobj:
                continue
            filepath = logdir + "/" + file
            for matchstr in matchobj.groups():
                logtime = datetime.strptime(matchstr, '%Y-%m-%d')
                if (nowtime - logtime).days < maxnum:
                    continue
                self._globalBaseLg.log(ERROR,
                                       "Remove redundant log file:%s" % (
                                           filepath))
                os.remove(filepath)

    def getDebug(self):
        """write log msg to all Logger"""
        return self.debugLg

    def getError(self):
        """write log msg to all Logger"""
        return self.errorLg

    def getbaseLg(self):
        """write base msg to log."""
        return self._globalBaseLg


class SignalLogHandle(_BaseLog):
    """signal-process logging.

    :_BaseLog: super class.
    """
    def __init__(self, rootpath, module='common', name='Signal'):
        """Initialize class.

        :@name: log name
        :rootpath:  data root path
        :module:    filename of log
        """
        super(SignalLogHandle, self).__init__(rootpath, module)
        self.name = '(%s)' % (name)

    def sendDebug(self, level, msg):
        """Send debug log msg into Queue.

        :level: log level.
        :msg:   log message.
        """
        try:
            fn, lno, func = self.findCaller()
            logmsg = ':'.join([fn, str(lno), func,
                               ''.join([self.name, msg])])
            self.debugLg.log(level, logmsg)
        except Exception, msg:
            exc_type, _, exc_tb = sys.exc_info()
            traceList = traceback.extract_tb(exc_tb)
            for (filename, lineno, funcname, text) in traceList:
                self._globalBaseLg.log(self.ERROR,
                                       "Error, type:%s, file:%s, func:%s"
                                       ",lineno:%s, msg:%s." % (
                                           exc_type, filename,
                                           funcname, lineno, msg))

    def sendError(self, level, msg):
        """Send error log msg into Queue.

        :level: log level.
        :msg:   log message.
        """
        try:
            fn, lno, func = self.findCaller()
            logmsg = ':'.join([fn, str(lno), func, ''.join(
                [self.name, msg])])
            self.errorLg.log(level, logmsg)
        except Exception, msg:
            exc_type, _, exc_tb = sys.exc_info()
            traceList = traceback.extract_tb(exc_tb)
            for (filename, lineno, funcname, text) in traceList:
                self._globalBaseLg.log(self.ERROR,
                                       "Error, type:%s, file:%s, func:%s"
                                       ",lineno:%s, msg:%s." % (
                                           exc_type, filename,
                                           funcname, lineno, msg))

    def findCaller(self):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            rv = (filename, f.f_lineno, co.co_name)
            break
        return rv


class MultiLogHandle(_BaseLog):
    """Multi-process logging.

    :_BaseLog: super class.
    """
    def __init__(self, shareQueue, rootpath, name='Multi', module='common'):
        """Initialize class.

        :shareQueue:A Queue for multiple processing.
        :rootpath:  data root path
        :module:    filename of log
        """
        super(MultiLogHandle, self).__init__(rootpath, module)

        self.shareQueue = shareQueue
        self._quitStr = 'quit'
        self._debugLog = 'debug:'
        self._errorLog = 'error:'
        self.name = '(%s)' % (name)
        self._dollarCharacter = '$'
        self._logLoggerDict = {
            self._debugLog: self.debugLg,
            self._errorLog: self.errorLg,
        }

    def sendDebug(self, level, msg):
        """Send debug log msg into Queue.

        :level: log level.
        :msg:   log message.
        """
        fn, lno, func = self.findCaller()
        logmsg = ':'.join([fn, str(lno), func,
                           ''.join([self.name, msg])])
        newMsg = self._dollarCharacter.join(
            [self._debugLog, str(level), logmsg])
        self.shareQueue.put_nowait(newMsg)

    def sendError(self, level, msg):
        """Send error log msg into Queue.

        :level: log level.
        :msg:   log message.
        """
        fn, lno, func = self.findCaller()
        logmsg = ':'.join([fn, str(lno), func, ''.join(
            [self.name, msg])])
        newMsg = self._dollarCharacter.join(
            [self._errorLog, str(level), logmsg])
        self.shareQueue.put_nowait(newMsg)

    def receive(self):
        """Receive log msg from Queue."""
        try:
            data = self.shareQueue.get()
            if data == self._quitStr:
                return False
            lgStr, level, msg = data.split(self._dollarCharacter, 2)
            self._logLoggerDict[lgStr].log(eval(level), msg)
        except Exception, msg:
            exc_type, _, exc_tb = sys.exc_info()
            traceList = traceback.extract_tb(exc_tb)
            for (filename, lineno, funcname, text) in traceList:
                self._globalBaseLg.log(self.ERROR,
                                       "Error, type:%s, file:%s, func:%s"
                                       ",lineno:%s, msg:%s." % (
                                           exc_type, filename,
                                           funcname, lineno, msg))
        return True

    def errorLog(self, msg):
        """write error log."""
        self.errorLg.log(self.ERROR, ''.join([self.name, msg]))

    def debugLog(self, msg):
        """write error log."""
        self.debugLg.log(self.ERROR, ''.join([self.name, msg]))

    def findCaller(self):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            rv = (filename, f.f_lineno, co.co_name)
            break
        return rv

    def stop(self):
        """Stop log handle."""
        self.shareQueue.put_nowait(self._quitStr)

if __name__ == '__main__':
    pass
