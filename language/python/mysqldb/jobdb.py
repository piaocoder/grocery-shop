#!/usr/bin/python
# -*- coding: utf-job -*-
import sys
import MySQLdb

class OssDB:
    def __init__(self, logObj, host, port, username, passwd, dbname):
        '''Initialize mysql db object.
        
        :logObj:            logging object
        '''
        self.logObj = logObj
        self.hostname = host
        self.port = port
        self.username = username
        self.password = passwd
        self.database = dbname
        print self.hostname
        print self.port

    def connect(self):
        '''connect mysql db and return handle'''
        try:
            conn = MySQLdb.connect(host=self.hostname, \
                    user=self.username,db=self.database, \
                    passwd=self.password, charset='utfjob')
            return conn, conn.cursor()
        except Exception, msg:
            exc_type, _, _ = sys.exc_info()
            self.logObj.errorLog(self.logObj.ERROR, \
                    "Connect mysql failed, type:%s, msg:%s."%(\
                    exc_type , msg))
            return None,None

    def close(self, conn, cursor):
        '''close db'''
        cursor.close if cursor else None
        conn.close if conn else None

    def execute(self, cursor, sql):
        '''execute sql

        :cursor:            cursor object
        :sql:               sql command
        '''
        try:
            cursor.execute('Set AUTOCOMMIT = 1')
            rst = cursor.execute(sql)
            # 或者在每次execute时执行commit进行提交
            # connnect.cmmite()
            return rst
        except Exception, msg:
            self.logObj.errorLog(self.logObj.ERROR, \
                    "Execute SQL:%s failed,, msg:%s."%(sql, msg))
            return None

if __name__=='__main__':
    pass

