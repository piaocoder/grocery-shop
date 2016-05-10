# coding:utf-8
import requests
# import json

paydata = {
    'pos': 'fujian-tel',
    'domain': 'google.com',
    'days': 30,
}

rsp = requests.post(
    'http://127.0.0.1:5000/v1/requests',
    data=paydata,
    headers={"Accept": "application/json"})
print rsp.text
