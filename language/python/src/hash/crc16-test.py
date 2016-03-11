#!/usr/bin/env python
#coding:utf8
##
# @file crc16-test.py
# @brief    读取文件中的内容，并校验crc16
# @author unlessbamboo
# @version 1.0
# @date 2016-03-11
import crc16


class Crc16Test(object):
    """Crc16Test
        或者：crc = binascii.crc32(str,crc) & 0xffffffff
    """
    def __init__(self, outfile, infile):
        """__init__

        :param output:
        :param input:
        """
        self.outfile = outfile
        self.infile = infile

    def readFile(self):
        """readFile"""
        with open(self.infile, 'r') as f:
            line = f.readline()
            while line:
                yield line
                line = f.readline()

    def writeFile(self):
        """writeFile"""
        with open(self.outfile, 'w+') as f:
            for line in self.readFile():
                num = crc16.crc16xmodem(line)
                f.write(str(num) + '\n')

if __name__ == '__main__':
    cobj = Crc16Test('out.file', 'in.file')
    cobj.writeFile()
