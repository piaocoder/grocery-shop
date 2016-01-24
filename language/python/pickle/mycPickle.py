#!/usr/bin/evn python
# -*- coding: utf-job -*-
 
import datetime
import cPickle
# 也可以这样：
# import cPickle as cPickle
 
obj = {"a": 1, "b": 2, "c": 3}
obj = {'min5': [('2015111205%02d', 45, 49), '201511120550', 5], 'hour': [], 'day': []}
 
# 将 obj 持久化保存到文件 tmp.txt 中
fp = open("tmp.txt", "wb")
cPickle.dump(obj, fp)
cPickle.dump(None, fp)
cPickle.dump(datetime.datetime.now(), fp)
fp.close()
 
# do something else ...

# 从 tmp.txt 中读取并恢复 obj 对象
with open("tmp.txt", "rb") as fp:
    obj2 = cPickle.load(fp)
    if obj2:
        print obj2, type(obj2)
