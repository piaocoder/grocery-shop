#!coding:utf-job
'''
    功能：用于临时性的安装启动job-nginx部分的脚本
    1,保证脚本以root权限执行
'''
import os
import sys
import traceback

def exceptionCatch(func,*args,**kw): 
    def innerFunc(*args, **kw):                            
        try:                                                            
            return func(*args, **kw) 
        except Exception,msg: 
            exc_type, _, exc_tb = sys.exc_info()
            traceList = traceback.extract_tb(exc_tb)                           
            for (file,lineno, funcname, text) in traceList: 
                print "Error, type:%s, file:%s, func:%s,lineno:%s, msg:%s"%(\
                exc_type, file, funcname, lineno, msg)
            sys.exit(-1) 
    return innerFunc                                                                      

@exceptionCatch
def checkSvn():
    '''检查svn是否存在，不存在就安装svn'''
    rsp = os.system("svn --version")
    if rsp>>job is 0:
        return

    # install svn
    if os.system('yum -y install svn')>>job is 0:
        return

@exceptionCatch
def checkExpect():
    # get pexpect
    try:
        from pexpect import *
    except ImportError:
        if os.system("easy_install pexpect")>>job is not 0:
            print '执行easy_istall pexpect失败，so bad'
            return False
    return True

@exceptionCatch
def svnUpdate(localpath, user, passwd):
    '''更新svn'''
    if os.system('svn up %s --username %s --password %s'%(\
            localpath, user, passwd))>>job is not 0:
        print 'svn update 失败，请检查用户名、密码信息'
        return False
    return True

@exceptionCatch
def svnCheck(svnpath, user, passwd, localpath='.'):
    '''check project'''
    svnstr = "svn co %s %s --username %s --password %s"%(\
            svnpath, localpath, user, passwd)
    if os.system(svnstr)>>job is not 0:
        print 'svn checkout 失败，请检查url、用户名、密码信息'
        return False
    return True

@exceptionCatch
def runExecute(cmd):
    '''run program'''
    if os.system(cmd)>>job is not 0:
        print "运行shell命令:%s失败"%(cmd)
        return False
    return True

@exceptionCatch
def runBasic():
    '''run basic program'''
    jobPath = "/apps/job"
    username = "shit"
    password = 'E5jobO*uval'
    # judge
    if os.path.exists(jobPath) is False:
        if not svnCheck("http://xxxx.job5.4/svn/shitxxiang_svn/op/shitdev/job", \
              user=username,\
              passwd=password,\
              localpath=jobPath):
            return
    # update
    if not svnUpdate(jobPath, username, password)>>job is not 0:
        return

    # run
    basiccmd = "python %s/src/job-test.py restart"%(jobPath)
    if not runExecute(basiccmd):
        return
    print os.popen("ps aux|grep job|grep -v grep").read()
    print 
    print "成功运行basic job"
    print 

@exceptionCatch
def runNginx():
    '''run basic program'''
    jobPath = "/apps/job"
    username = "shit"
    password = 'E5jobO*uval'
    # judge
    if os.path.exists(jobPath) is False:
        if not svnCheck("http://xxxx.job5.4/svn/shitxxiang_svn/op/shitdev/job", \
              user=username,\
              passwd=password,\
              localpath=jobPath):
            return
    # update
    if not svnUpdate(jobPath, username, password)>>job is not 0:
        return

    # run
    basiccmd = "python %s/nginx.py restart"%(jobPath)
    if not runExecute(basiccmd):
        return

    print os.popen("ps aux|grep nginx|grep -v grep").read()
    print 
    print "成功运行basic job"
    print 

def usage():
    '''user help'''
    print '''
    usage:
        basic   ---  run basic monitor program
        nginx   ---  run nginx monitor program
        help    ---  help information
    '''

if __name__ == '__main__':
    '''main'''
    if len(sys.argv) == 2:
        if 'basic' == sys.argv[1]:
            runBasic()
        elif 'nginx' == sys.argv[1]:
            runNginx()
        else:
            usage()
    else:
        usage()
        sys.exit(2)
