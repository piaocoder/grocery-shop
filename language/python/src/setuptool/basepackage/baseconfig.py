#!/usr/bin/python
#coding:utf-8
import os
import sys
import ConfigParser


CONF_DIR = "/data/conf/job/basepackage.ini"


def parseExcept(func):
    """Except exception when parse configure file"""
    def innerFunc(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError), msg:
            sys.stderr.write("Occure excecpt:{0}.n".format(msg))
            return None
    return innerFunc


class _ParseConfig(object):
    """Base configure"""
    def __init__(self, filename):
        """init"""
        self._filename = filename
        self._configParser = ConfigParser.ConfigParser()
        self._configParser.read(filename)

    @parseExcept
    def getDataDir(self):
        """getDataDir:Get data directory"""
        return self._configParser.get("directory", "data")

    @parseExcept
    def getLogDir(self):
        """getLogDir: Get log directory"""
        return self._configParser.get("directory", "logs")

    @parseExcept
    def getPidFile(self, key):
        """getPidFile:Get pid filename by key.

        :param key: pid key
        """
        return self._configParser.get("pid", key)

    @parseExcept
    def getJavaTrace(self):
        """getJavaTrace:get java trace log"""
        return self._configParser.get("java", "tracelog")

    @parseExcept
    def getKafkaConf(self):
        """getKafkaConf:get kafak configure"""
        return self._configParser.get("kafka", "kafka")


class BaseConfig(object):
    """Base configure class"""
    def __init__(self):
        """init"""
        self.filename = CONF_DIR
        self._configParser = _ParseConfig(self.filename)
        self._init()

    def _init(self):
        """_init"""
        try:
            self._datadir = self._configParser.getDataDir()
            if not os.path.isdir(self._datadir):
                os.makedirs(self._datadir)
        except Exception, msg:
            sys.stderr.write(
                "Occur error at BaseConfig init, msg:{0}\n".format(msg))
            sys.exit(0)

    def getJavaTrace(self):
        """getJavaTrace:get java trace log"""
        value = self._configParser.getJavaTrace()
        if not value:
            sys.stderr.write("Get java tracelog failed.n")
            return None
        return "{0}/{1}".format(self._datadir, value)

    def getKafkaConf(self):
        """getKafkaConf:get kafak configure"""
        value = self._configParser.getKafkaConf()
        if not value:
            sys.stderr.write("Get kafa configure failed.n")
            return None
        return "{0}/{1}".format(self.filename, value)

    def getPidFile(self, key):
        """getPidFile:Get pid filename by key.

        :param key: pid key
        """
        value = self._configParser.getPidFile(key)
        if not value:
            sys.stderr.write("Get kafa pid failed.n")
            return None
        return "{0}/{1}".format(self._datadir, value)

    def getDataDir(self):
        value = self._configParser.getDataDir()
        if not value:
            sys.stderr.write("Get data directory failed.n")
            return None
        return value

    def getLogDir(self):
        """getLogDir: Get log directory"""
        value = self._configParser.getLogDir()
        if not value:
            sys.stderr.write("Get log directory failed.n")
            return None
        return value


class KafkaParse(object):
    '''parse kafka.conf'''
    def __init__(self, filename):
        '''init'''
        self._filename = filename
        self._configParser = ConfigParser.ConfigParser()
        self._configParser.read(filename)

    def _getPythonpath(self):
        '''get new PYTHONPATH from path'''
        try:
            return self._configParser.get('pythonenv',
                                          'pythonpath').split('$')
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None

    def setPythonpath(self):
        '''add new path into sys.path'''
        # change systempath
        dir = os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))) + "/"
        addPythonPath = [
            dir + subpath for subpath in self._getPythonpath()]
        for path in addPythonPath:
            sys.path.insert(0, path)
        #sys.path.extend(addPythonPath)

    def getTopic(self, key):
        '''get topic for nginx'''
        try:
            return self._configParser.get('topic', key)
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None

    def getInterTime(self):
        '''get interval time'''
        try:
            return float(self._configParser.get('kafka', 'intervaltime'))
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None

    def getCacheTime(self, key):
        '''get cache time'''
        try:
            return int(self._configParser.get('cacheTime', key))
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None

    def getKvId(self, key):
        '''get KV'''
        try:
            return int(self._configParser.get('kvId', key))
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None

    def getApp(self, key):
        '''get KV'''
        try:
            return self._configParser.get('app', key).split('$')
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None

    def getBrokerList(self):
        '''get broker list.
        '''
        try:
            return self._configParser.get('kafka', 'broker').split('$')
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None

    def getHbaseTable(self, key):
        '''get hbase table'''
        try:
            return self._configParser.get('hbase', key)
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None

    def getHbaseList(self):
        '''get hbase list'''
        try:
            return self._configParser.get('hbaseserver', 'host').split('$')
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None

    def getMysqlHost(self):
        '''get mysql host'''
        try:
            return self._configParser.get('ossdb', 'host')
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None

    def getMysqlPort(self):
        '''get mysql port'''
        try:
            return float(self._configParser.get('ossdb', 'port'))
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None

    def getMysqlUser(self):
        '''get mysql username'''
        try:
            return self._configParser.get('ossdb', 'username')
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None

    def getMysqlPasswd(self):
        '''get mysql password'''
        try:
            return self._configParser.get('ossdb', 'password')
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None

    def getMyqlDb(self):
        '''get mysql db'''
        try:
            return self._configParser.get('ossdb', 'dbname')
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None

    def getModule(self, key):
        '''Get module information.

        :key: Lamon type, for example:basic,java
        '''
        try:
            return self._configParser.get('module', key)
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None

    def re_read(self):
        '''Re-read configure file'''
        try:
            self._configParser.read(self._filename)
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None

    def options(self, sections):
        '''Get all options by sections.'''
        try:
            return self._configParser.options(sections)
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None

    def get(self, sections, options):
        '''Get value by sections/options.'''
        try:
            return self._configParser.get(sections, options)
        except (ConfigParser.NoSectionError,
                ConfigParser.NoOptionError):
            return None


# base configure
globalBaseConfig = BaseConfig()

# kafak configure
_kafkaConfName = globalBaseConfig.getKafkaConf()
if not _kafkaConfName:
    sys.exit(-1)
else:
    globalConfigParse = KafkaParse(_kafkaConfName)


if __name__ == '__main__':
    pass
