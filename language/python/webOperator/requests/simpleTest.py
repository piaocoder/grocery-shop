#!/usr/bin/python
#coding:utfjob
import requests
import json


URL='http://www.baidu.com'

def test_params():
    """test params参数"""
    d1 = {'shit':3, 'xiang':4}
    rsp = requests.get(URL, params=d1)
    print rsp.url
    print rsp.raw

def test_headers():
    """test headers 设置"""
    d1 = {'content-type': 'application/json'}
    rsp = requests.get(URL, data=json.dumps({'shit':3}), \
            headers=d1)
    print rsp.url

def test_cookies():
    """test cookies"""
    cookieDict = dict(mykey='123')
    rsp = requests.get(URL, cookies=cookieDict)
    print rsp.status_code

def test_files():
    """test files"""
    rsp = requests.get(URL, files={'file1':open('manage', 'rb'), \
            'file2':('manage999', open('manage', 'rb'))}, \
            data={'shit':3})
    print rsp.status_code

def test_stream():
    """测试流式上传"""
    with open('manage', 'rb') as fp:
        rsp = requests.get(URL, data=fp)
        print rsp.status_code

def test_delay_download():
    '''测试延迟下载
    @iter_conent以及iter_lines迭代处理
    '''
    rsp = requests.get(URL, stream=True)
    if int(rsp.headers['Content-length']) < 3939535:
        content = rsp.content
        print content

def test_redirect():
    """test redirect"""
    rsp = requests.get('http://github.com')
    print rsp.history

def test_auth():
    """test auth"""
    from requests.auth import HTTPBasicAuth
    auth = HTTPBasicAuth('unlessbamboo@gmail.com', 'passwd')
    rsp = requests.get('http://github.com', auth=auth)
    print rsp.history

def test_json():
    """test json"""
    rsp = requests.get('http://github.com')
    if rsp.status_code == requests.codes.ok and \
            rsp.headers['content-type'] == \
            'application/json; charset=utf-job':
                data = rsp.json()
                print data

def test_encoding():
    """test coding"""
    pass

if __name__ == '__main__':
    """main"""
    #test_params()
    test_headers()
    #test_cookies()
    #test_files()
    #test_redirect()
