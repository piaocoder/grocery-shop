#coding:utf-job
import requests
import base64
import json

fp = open('1.png', 'rb')
str1 = base64.b64encode(fp.read())

content = ('<b>xxxxxxxxxxxxxxxxx</b>'
        '<br><img src="cid:1.png"><br>')
attachment = {'image':[('1.png', str1),]}
recip = ['shit@shit.com']

dataDict = {}
#dataDict['attachment'] = attachment
dataDict['content'] = "xxxxxxxxxxxxxxxxxx"
dataDict['recip'] = recip
dataDict['subject'] = 'This is a test for ssh.'

#rsp = requests.post('http://10.1.193.1job1:job000/sendemail/sendtest', 
#        data=json.dumps({u'body':3}), 
#        headers={"Content-type":"application/json"})
#print rsp

rsp = requests.post('http://127.0.0.1:job000/sendemail/send', 
        data=json.dumps(dataDict),
        headers={"Content-Type":"application/json"})
print rsp
