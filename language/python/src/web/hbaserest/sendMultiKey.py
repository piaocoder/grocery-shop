#coding:utf-8
'''
    发送http数据到hbase上，有两点需要注意：
        1，每一个column的格式必须是(columnName:sub)，其中sub可以不存在，但是':'必须存在
        2，发送多个Keys时，URL为false-row-key
'''
import sys
import base64
import json
import requests

ageB64 = base64.b64encode('age:')
colorB64 = base64.b64encode('color:')
nameB64 = base64.b64encode('name:')
minmoduledict = {
        u'Row':[
            {
                u'key':base64.b64encode('panxiaoyuan:01'),
                u'Cell':[
                    {
                        u'column':ageB64,
                        u'$':base64.b64encode('24'),
                    },
                    {
                        u'column':colorB64,
                        u'$':base64.b64encode('red'),
                    },
                    {
                        u'column':nameB64,
                        u'$':base64.b64encode('mylove'),
                    },
                ]
            },
            {
                u'key':base64.b64encode('panxiaoyuan:02'),
                u'Cell':[
                    {
                        u'column':ageB64,
                        u'$':base64.b64encode('24'),
                    },
                    {
                        u'column':colorB64,
                        u'$':base64.b64encode('red'),
                    },
                    {
                        u'column':nameB64,
                        u'$':base64.b64encode('mylove'),
                    },
                ]
            },
            {
                u'key':base64.b64encode('panxiaoyuan:03'),
                u'Cell':[
                    {
                        u'column':ageB64,
                        u'$':base64.b64encode('24'),
                    },
                    {
                        u'column':colorB64,
                        u'$':base64.b64encode('red'),
                    },
                    {
                        u'column':nameB64,
                        u'$':base64.b64encode('mylove'),
                    },
                ]
            },
            {
                u'key':base64.b64encode('who:01'),
                u'Cell':[
                    {
                        u'column':ageB64,
                        u'$':base64.b64encode('27'),
                    },
                    {
                        u'column':colorB64,
                        u'$':base64.b64encode('blue'),
                    },
                    {
                        u'column':nameB64,
                        u'$':base64.b64encode('love'),
                    },
                ]
            },
        ],
    }

paydata = json.dumps(minmoduledict, separators=(',', ':'))
url = 'http://10.1.200.7:8080/bifeng/false-row-key'

rsp = requests.put(url, data=paydata, \
        headers= {"Content-Type":"application/json"})
if rsp is None:
    print 'return none'
    sys.exit(-1)
print rsp.status_code
