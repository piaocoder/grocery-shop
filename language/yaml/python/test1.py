#!/usr/bin/env python
# coding:utf8
import yaml

class Bamboo:
    def __init__(self, name, hp, sp):
        self.name = name
        self.hp = hp
        self.sp = sp
    def __repr__(self):
        return "%s(name=%r, hp=%r, sp=%r)" % (
            self.__class__.__name__, self.name, self.hp, self.sp)

stream = file('test1.yaml', 'r')
stream2 = file('test1.yaml', 'r')
print '文件中的原始字符串为：\n', stream2.read()

print "\n最终的结果输出为:"
for data in yaml.load_all(stream):
    print data
