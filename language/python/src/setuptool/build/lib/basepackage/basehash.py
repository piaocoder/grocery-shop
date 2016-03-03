#!/usr/bin/python
#coding:utf-8
'''
    server Consistent hashing wrapper class.
'''
import sys
import requests
import md5
#from hashlib import md5
import socket


class HashRing(object):
    def __init__(self, nodes=None, replicas=3):
        """Manages a hash ring.

        `nodes` is a list of objects that have a proper __str__ representation.
        `replicas` indicates how many virtual points should be used pr. node,
        replicas are required to improve the distribution.
        """
        self.replicas = replicas

        self.ring = dict()
        self._sorted_keys = []

        if nodes:
            for node in nodes:
                self.add_node(node)

    def add_node(self, node):
        """Adds a `node` to the hash ring (including a number of replicas).
        """
        for i in xrange(0, self.replicas):
            key = self.gen_key('%s:%s' % (node, i))
            self.ring[key] = node
            self._sorted_keys.append(key)

        self._sorted_keys.sort()

    def remove_node(self, node):
        """Removes `node` from the hash ring and its replicas.
        """
        for i in xrange(0, self.replicas):
            key = self.gen_key('%s:%s' % (node, i))
            del self.ring[key]
            self._sorted_keys.remove(key)

    def get_node(self, string_key):
        """Given a string key a corresponding node in the hash ring is returned.

        If the hash ring is empty, `None` is returned.
        """
        return self.get_node_pos(string_key)[0]

    def get_node_pos(self, string_key):
        """Given a string key a corresponding node in the hash ring is returned
        along with it's position in the ring.

        If the hash ring is empty, (`None`, `None`) is returned.
        """
        if not self.ring:
            return None, None

        key = self.gen_key(string_key)

        nodes = self._sorted_keys
        for i in xrange(0, len(nodes)):
            node = nodes[i]
            if key <= node:
                return self.ring[node], i

        return self.ring[nodes[0]], 0

    def get_nodes(self, string_key):
        """Given a string key it returns the nodes as a generator that can hold the key.

        The generator is never ending and iterates through the ring
        starting at the correct position.
        """
        if not self.ring:
            yield None, None

        node, pos = self.get_node_pos(string_key)
        for key in self._sorted_keys[pos:]:
            yield self.ring[key]

        while True:
            for key in self._sorted_keys:
                yield self.ring[key]

    def gen_key(self, key):
        """Given a string key it returns a long value,
        this long value represents a place on the hash ring.

        md5 is currently used because it mixes well.
        """
        #m = md5()
        m = md5.new()
        m.update(key)
        return long(m.hexdigest(), 16)

class ServerHash(HashRing):
    '''wrapper HashRing and request'''
    def __init__(self, globalLog, nodes=None):
        super(ServerHash, self).__init__(nodes)

        self._nodeStatus = {}
        self._globalLog = globalLog
        self._keyTuple = (socket.gethostname(), '1put', '2put', \
                '3put', '4put', '5put')
        self._keyLen = len(self._keyTuple)
        self.init_node(nodes)

    def init_node(self, nodes):
        '''init Nodes.'''
        for node in nodes:
            self._nodeStatus[node] = True

    def _get_node_len(self):
        '''get self._sorted_keys length'''
        return self._nodeStatus.__len__()

    def detect(self):
        '''monitor disable nodes'''
        for node in self._nodeStatus.keys():
            try:
                url = "http://%s/status/cluster"%node
                rsp = requests.get(url, headers={"Accept":"application/json"})
                if rsp.status_code is 200:
                    if not self._nodeStatus[node]:
                        self._globalLog.getInfo().log(self._globalLog.ERROR, \
                                "Disable node %s up."%node)
                        self._nodeStatus[node] = True
                else:
                    if self._nodeStatus[node]:
                        self._globalLog.getInfo().log(self._globalLog.ERROR, \
                                "Enable node %s down."%node)
                        self._nodeStatus[node] = False
                    else:
                        self._globalLog.getInfo().log(self._globalLog.ERROR, \
                                "Disable node %s still down."%node)
            except Exception, msg:
                exc_type, _, exc_tb = sys.exc_info()
                self._globalLog.getError().log(self._globalLog.ERROR, \
                        "Monitor reconnect failed. Exception type"\
                        ":%s, msg:%s"%(exc_type, msg)) 

    def _post(self, url, timeout = 1, data=None, **kwargs):
        '''post request to hbase'''
        rsp = requests.post(url, data=data, timeout=timeout, **kwargs)
        if rsp is None:
            self._globalLog.getInfo().log(self._globalLog.ERROR, \
                    "Rsp is None when post requests, url:%s"%(url))
        elif rsp.status_code is not 200:
            self._globalLog.getInfo().log(self._globalLog.ERROR, \
                    "Post data to hbase failed, url:%s, rsp:%d"%(\
                    url, rsp.status_code))
        return rsp

    def post(self, url, timeout = 1, data=None, **kwargs):
        '''post request to hbase'''
        nodeLen = self._get_node_len()
        for index in range(nodeLen):
            server = self.get_node(self._keyTuple[index%self._keyLen])
            if not self._nodeStatus[server]:
                continue
            urlstr = url%(server)
            try:
                return self._post(urlstr, data=data, \
                        timeout=timeout, **kwargs)
            except Exception,msg:
                exc_type, _, exc_tb = sys.exc_info()
                self._globalLog.getError().log(self._globalLog.ERROR, \
                        "Post request failed. Exception type"\
                        ":%s, url:%s, msg:%s"%(\
                        str(exc_type), urlstr, msg)) 
        self._globalLog.getError().log(self._globalLog.ERROR, \
                "Occur unknown error when call post,"\
                " url:%s, nodesLen=%d"%(url, nodeLen))
        return None

    def _get(self, url, timeout = 5,**kwargs): 
        '''get request'''
        rsp = requests.get(url, timeout=timeout, **kwargs)
        if rsp is None:
            self._globalLog.getInfo().log(self._globalLog.DEBUG, \
                    "Rsp is None when get requests, url:%s"%(url))
        elif rsp.status_code is not 200:
            self._globalLog.getInfo().log(self._globalLog.DEBUG, \
                    "Get data from hbase failed, url:%s, rsp:%d"%(\
                    url, rsp.status_code))
        return rsp

    def get(self, url, timeout = 5,**kwargs): 
        '''GET request'''
        nodeLen = self._get_node_len()
        for index in range(nodeLen):
            server = self.get_node(self._keyTuple[index%self._keyLen])
            if not self._nodeStatus[server]:
                continue
            urlstr = url%(server)
            try:
                return self._get(urlstr, timeout=timeout, **kwargs)
            except Exception,msg:
                exc_type, _, exc_tb = sys.exc_info()
                self._globalLog.getError().log(self._globalLog.ERROR, \
                        "Get request failed. Exception type"\
                        ":%s, url:%s, msg:%s"%(\
                        str(exc_type), urlstr, msg)) 
        self._globalLog.getError().log(self._globalLog.ERROR, \
                "Occur unknown error when call get,"\
                " url:%s, nodesLen=%d"%(url, nodeLen))
        return None

    def _put(self, url, data=None, timeout = 5,**kwargs): 
        '''GET request'''
        rsp = requests.put(url, data=data, timeout=timeout, **kwargs)
        if rsp is None:
            self._globalLog.getInfo().log(self._globalLog.ERROR, \
                    "Rsp is None when put requests, url:%s"%(url))
        elif rsp.status_code is not 200:
            self._globalLog.getInfo().log(self._globalLog.ERROR, \
                    "Http response unusual, url:%s, rsp:%d"%(\
                    url, rsp.status_code))
        return rsp

    def put(self, url, data=None, timeout = 5,**kwargs): 
        '''GET request'''
        nodeLen = self._get_node_len()
        for index in range(nodeLen):
            server = self.get_node(self._keyTuple[index%self._keyLen])
            if not self._nodeStatus[server]:
                continue
            urlstr = url%(server)
            try:
                return self._put(urlstr, data=data, timeout=timeout, \
                        **kwargs)
            except Exception,msg:
                exc_type, _, exc_tb = sys.exc_info()
                self._globalLog.getError().log(self._globalLog.ERROR, \
                        "Put request failed. Exception type"\
                        ":%s, url:%s, msg:%s"%(\
                        str(exc_type), urlstr, msg)) 
        self._globalLog.getError().log(self._globalLog.ERROR, \
                "Occur unknown error when call post,"\
                " url:%s, nodesLen=%d"%(url, nodeLen))
        return None

if __name__ == '__main__':
    '''main'''
    # 测试hbase中的get函数
    from baselog import BaseLogRecord
    globalLog = BaseLogRecord(disableExistLog=False, module="common")

    hbaseHash = ServerHash(globalLog, \
            ['10.10.116.229:8080', '10.10.138.212:8080'])
    rsp = hbaseHash.get(
            'http://%s/basic/lg-main-nginx-bjc-001:201510101010', \
            headers={"Accept":"application/json"})
    print rsp.text

    #
    # 测试post函数
    #
    paydata = ('{"Row":[{'
        '"key":"bGctbWFpbi1uZ2lueC1iamMtMDAxOjIwMTQxMDEwMTAxMA==",'
        '"Cell":['
        '{"column":"bmV0OmJ5dGVzX3NlbnQ=","timestamp":1444443002138,'
            '"$":"MTAxNTY0NA=="},'
        '{"column":"bmV0OmRyb3Bpbg==","timestamp":1444443002138,"$":"MA=="},'
        '{"column":"bmV0OmRyb3BvdXQ=","timestamp":1444443002138,"$":"MA=="},'
        '{"column":"bmV0OmVycmlu","timestamp":1444443002138,"$":"MA=="},'
        '{"column":"bmV0OmVycm91dA==","timestamp":1444443002138,"$":"MA=="},'
        '{"column":"bmV0OnBhY2tldHNfcmVjdg==","timestamp":1444443002138,'
            '"$":"MjUyMA=="},'
        '{"column":"bmV0OnBhY2tldHNfc2VudA==","timestamp":1444443002138,'
            '"$":"MTcxMA=="}]}]}')
    rsp = hbaseHash.post('http://%s/basic/lg-main-nginx-bjc-001:201410101010', headers={"Content-Type":"application/json"}, data=paydata)
    print rsp.text
