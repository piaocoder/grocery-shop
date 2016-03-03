#coding:utf-8
#!/usr/bin/python
import os
import time
import sys
from collections import defaultdict

fp = open('result.output')

def tail(fp):
    fp.seek(5000)

    while 1:
        line = fp.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def parse_first():
    dstDict = defaultdict(set)
    dstDictIP = defaultdict(set)
    errorSet = set()

    errorFp = open('./error', 'w')

    for line in tail(fp):
        l1 = [str1.strip() for str1 in line.split('--')]
        if len(l1) < 3:
            continue

        if not l1[1] or not l1[2] or '-' in l1[0]:
            continue

        if l1[1] in errorSet:
            continue
        dstDict[l1[1]].update([l1[2]])
        dstDictIP[l1[1]].update([l1[0]])

        if len(dstDict[l1[1]]) > 1 and l1[0] not in dstDictIP[l1[1]] and l1[2]:
            print 'Error:key', l1[1], 'value:', dstDict[l1[1]], 'newIp:', l1[0]
            print dstDict[l1[1]]
            print dstDictIP[l1[1]]
            errorSet.update([l1[1]])
            errorFp.writelines(l1[1])

    errorFp.close()
    fp.close()


def parse_second():
    dstDict = defaultdict(set)
    dstDictIP = defaultdict(set)
    errorSet = set()

    errorFp = open('./error', 'w')

    for line in tail(fp):
        l1 = [str1.strip() for str1 in line.split('--')]
        if len(l1) < 3:
            continue

        if not l1[1] or not l1[2] or '-' in l1[0]:
            continue

        if l1[1] in errorSet:
            continue
        dstDict[l1[1]].update([l1[2]])
        dstDictIP[l1[1]].update([l1[0]])

        if len(dstDict[l1[1]]) > 1 and l1[2]:
            print 'Error:key', l1[1], 'value:', dstDict[l1[1]], 'newIp:', l1[0]
            print dstDict[l1[1]]
            print dstDictIP[l1[1]]
            errorSet.update([l1[1]])
            errorFp.writelines(l1[1])

    errorFp.close()
    fp.close()

parse_second()
