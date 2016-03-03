#!/usr/bin/python
#!coding:utf-8
'''解析一个xml并输出'''

from os import path
import xml.etree.ElementTree as ET

class parseXml(object):
    def __init__(self):
        '''initialize'''
        self._root = None
    
    def constructTree(self, filename):
        '''从给定的文件名中构造一颗xml树'''
        if not path.isfile(filename):
            return None
        self._root = ET.parse(filename).getroot()

    def getRoot(self):
        '''获取树的根节点'''
        return self._root

    def findChildNode(self, element):
        '''find children node from a tree'''
        return self._root.findall(element)

    def displayTree(self, root):
        '''打印整棵树'''
        print root.tag, root.attrib, root.text
        for child in root:
            self.displayTree(child)

if __name__ == '__main__':
    '''main'''
    parse = parseXml()
    parse.constructTree('./filedir/test.xml')
    parse.displayTree(parse.getRoot())
    print("======================================\n")
    node = parse.findChildNode('./movie/type')
    for a in node:
        print(a.text)
