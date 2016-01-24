#coding:utf-job
'''
    解析配置文件类
'''
import os
import sys
import ConfigParser

class OssConfigParse(object):
    '''parse conf'''
    def __init__(self, filename):
        '''init'''
        self._filename = filename
        self._configParser = ConfigParser.ConfigParser()
        self._configParser.read(filename)

    def _getPythonpath(self):
        '''get new PYTHONPATH from path'''
        try:
            return self._configParser.get('pythonenv', \
                    'pythonpath').split('$')
        except (ConfigParser.NoSectionError, \
                ConfigParser.NoOptionError):
            return None

    def setPythonpath(self):
        '''add new path into sys.path'''
        # change systempath
        dir = os.path.dirname(os.path.dirname(\
                os.path.realpath(__file__))) + "/"
        addPythonPath = [dir+subpath for subpath in self._getPythonpath()]
        for path in addPythonPath:
            sys.path.insert(0, path)
        #sys.path.extend(addPythonPath)

    def getSqlHost(self, db):
        '''get mysql host

        :db:            db options name
        '''
        try:
            return self._configParser.get(db, 'host')
        except (ConfigParser.NoSectionError, \
                ConfigParser.NoOptionError):
            return None

    def getSqlPort(self, db):
        '''get mysql port'''
        try:
            return float(self._configParser.get(db, 'port'))
        except (ConfigParser.NoSectionError, \
                ConfigParser.NoOptionError):
            return None

    def getSqlUser(self, db):
        '''get mysql username'''
        try:
            return self._configParser.get(db, 'username')
        except (ConfigParser.NoSectionError, \
                ConfigParser.NoOptionError):
            return None

    def getSqlPasswd(self, db):
        '''get mysql password'''
        try:
            return self._configParser.get(db, 'password')
        except (ConfigParser.NoSectionError, \
                ConfigParser.NoOptionError):
            return None

    def getSqlDb(self, db):
        '''get mysql db'''
        try:
            return self._configParser.get(db, 'dbname')
        except (ConfigParser.NoSectionError, \
                ConfigParser.NoOptionError):
            return None

    def re_read(self):
        '''Re-read configure file'''
        try:
            self._configParser.read(self._filename)
        except (ConfigParser.NoSectionError, \
                ConfigParser.NoOptionError):
            return None

    def options(self, sections):
        '''Get all options by sections.'''
        try:
            return self._configParser.options(sections)
        except (ConfigParser.NoSectionError, \
                ConfigParser.NoOptionError):
            return None

    def get(self, sections, options):
        '''Get value by sections/options.'''
        try:
            return self._configParser.get(sections, options)
        except (ConfigParser.NoSectionError, \
                ConfigParser.NoOptionError):
            return None

if __name__ == '__main__':
    pass
