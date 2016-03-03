#!/usr/bin/python
#coding:utf-8
import os
import sys
import MySQLdb

# set root directory
package_path = os.getcwd() + '/../'
sys.path.append(package_path)

from basepackage.baselog import globalLog

class MysqldbHandle(object):
    '''test MySQLdb'''
    def __init__(self, address, user, passwd, db):
        self._address = address
        self._user = user
        self._passwd = passwd
        self._dbname = db
        self._db = None
        self._cursor = None

    def connectDb(self):
        '''connect DB'''
        try:
            self._db = MySQLdb.connect(self._address, self._user, self._passwd, self._db)
            self._cursor = self._db.cursor()
        except Exception,msg:
            globalLog.getError().log(globalLog.ERROR, \
                    'Connect SqlDB failed, msg:%s'%(msg))
            return

    def executeSql(self, sql, isReturn=False):
        '''execute sql command'''
        try:
            self.execute(sql)
            self._db.commit()
            if not isReturn:
                return
            results = self._cursor.fetchall()
            for row in results:
                globalLog.getError.log(globalLog.ERROR, \
                        'row0=%s'%(row[0]))
        except Exception,msg:
            self._db.rollbak()
            globalLog.getError().log(globalLog.ERROR, \
                    'Execute sql failed, sql=%s, msg:%s'%(sql, msg))

if __name__ == '__main__':
    '''main'''
    pass
