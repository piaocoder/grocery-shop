#!/usr/bin/python
#coding:utf-8
import os
import sys
import atexit
import time
from signal import (SIGQUIT, SIGHUP)


class MulDaemon(object):
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdin='/dev/null',
                 stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        """Do the UNIX double-fork magic, see Stevens'."Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177).
        """
        # do first fork
        try:
            pid = os.fork()
            sys.exit(0) if pid > 0 else None
        except OSError, e:
            print "Fork process failed: %d(%s)." % (e.errno, e.strerror)
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            sys.exit(0) if pid > 0 else None
        except OSError, e:
            print "Fork process failed: %d(%s)." % (e.errno, e.strerror)
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        #si = file(self.stdin, 'r')
        #so = file(self.stdout, 'a+')
        #se = file(self.stderr, 'a+', 0)
        #os.dup2(si.fileno(), sys.stdin.fileno())
        #os.dup2(so.fileno(), sys.stdout.fileno())
        #os.dup2(se.fileno(), sys.stderr.fileno())

        # registrem destructor function
        atexit.register(self.delpid)
        # write pidfile
        try:
            fd = open(self.pidfile, 'w+')
            fd.write('%s\n' % (str(os.getpid())))
            fd.close()
            os.chmod(self.pidfile, 0777)
        except IOError, msg:
            print "%s:open pidfile failed." % msg
            sys.exit(1)

    def delpid(self):
        '''destructor function'''
        os.remove(self.pidfile)

    def start(self):
        """Start the daemon."""
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist, start failed."
            print message % (self.pidfile)
            sys.exit(1)

        self.daemonize()
        self.run()

    def stop(self):
        """Stop the daemon for SIGQUIT signal."""
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = ("Not found pid at Pidfile %s does not exist."
                       "Manual check process please!")
            print message % self.pidfile
            return

        try:
            while 1:
                os.kill(pid, SIGQUIT)
                time.sleep(1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                message = ("Not found pid=%s at %s."
                           "Manual removal process please.")
                print message % (pid, self.pidfile)
            else:
                print 'Daemon stop:%s' % err
            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)

    def restart(self):
        """Restart the daemon"""
        self.stop()
        self.start()

    def reload(self):
        """reload the daemon"""
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = ("Not found pid at Pidfile %s does not exist."
                       "Manual check process please!")
            print message % self.pidfile
            return

        os.kill(pid, SIGHUP)
        time.sleep(1)
        print 'Reload program successful!'

    def stopforce(self, cmdfile):
        '''Forced to stop process'''
        pid = str(os.getpid())
        commandstr = ("ps -ef|grep python|grep -w '%s'"
                      "|grep -v grep|awk '{print $2}'|"
                      "grep -v %s|xargs kill -9" % (cmdfile, pid))
        if os.system(commandstr) >> 8 is not 0:
            print "Forced to stop all process failed, command:%s" % commandstr

    def usage(self):
        '''user help info'''
        pass

    def run(self):
        """You should override this method when you subclass Daemon.
        It will be called after the process has been
        daemonized by start() or restart()."""
        pass


def start_up(filename, ob, opt, *args):
    '''Start a new program.

    :ob:    objects.
    :args:  other argument
    '''
    if 'start' == opt:
        print "Start aggregate handle."
        ob.start()

    elif 'stop' == opt:
        print "Stop aggregate handle."
        ob.stop()

    elif 'restart' == opt:
        print "Restart aggregate handle."
        ob.restart()

    elif 'reload' == opt:
        print "Reload aggregate handle."
        ob.reload()

    elif 'debug' == opt:
        ob.run()

    elif 'stopforce' == opt:
        ob.stopforce(filename)

    elif 'help' == opt:
        ob.usage()

    else:
        print ("Unknown command, please input \"help\" to"
               "get morn infomation.")
