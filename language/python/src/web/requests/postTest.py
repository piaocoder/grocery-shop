#!/usr/bin/env python
# coding:utf8
import requests
import json

paydata = {
    'domains':  'newdun.com',
    'types':    'months',
    'lines':    'all',
}
rsp = requests.post(
    'http://192.168.199.15:8989/api/v1.0/logparse',
    data=paydata,
    headers={"Accept": "application/json"})
rst = json.loads(rsp.text)
print 'xxxxxxxxxxxxxxxxxxxxxx返回一个月的字典xxxxxxxxxxxxxxxxxxxxxxx'
print rst
print '字典长度为:', len(rst['list'])


paydata = {
    'domains':  'newdun.cc',
    'types':    'halfs',
    'lines':    'all',
}
rsp = requests.post(
    'http://192.168.199.15:8989/api/v1.0/logparse',
    data=paydata)
rst = json.loads(rsp.text)
print '\n\nxxxxxxxxxxxxxxxxxxxxxx返回半年的字典xxxxxxxxxxxxxxxxxxxxxxx'
print rst
print '字典长度为:', len(rst['list'])


paydata = {
    'domains':  'newdun.cc',
    'types':    'weeks',
    'lines':    'all',
}
rsp = requests.post(
    'http://192.168.199.15:8989/api/v1.0/logparse',
    data=paydata)
rst = json.loads(rsp.text)
print '\n\nxxxxxxxxxxxxxxxxxxxxxx返回一周的字典xxxxxxxxxxxxxxxxxxxxxxx'
print rst
print '字典长度为:', len(rst['list'])


paydata = {
    'domains':  'newdun.net',
    'types':    'hours',
    'lines':    'all',
}
rsp = requests.post(
    'http://192.168.199.15:8989/api/v1.0/logparse',
    data=paydata)
rst = json.loads(rsp.text)
print '\n\nxxxxxxxxxxxxxxxxxxxxxx返回一天的字典xxxxxxxxxxxxxxxxxxxxxxx'
print rst
print '字典长度为:', len(rst['list'])
