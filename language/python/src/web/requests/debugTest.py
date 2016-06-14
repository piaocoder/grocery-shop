# coding:utf8
import requests
import logging

# These two lines enable debugging at httplib level
# (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA,
# and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

requests.adapters.DEFAULT_RETRIES = 5
headers = {'hosts':   'explicit.newdun.com.cn'}
headers = {'hosts':   'explicit.bamboo.com'}
headers = {'hosts':   'invisible.bamboo.com'}
# rsp = s.get("http://192.168.199.12/")
rsp = requests.get('http://192.168.199.12/', headers=headers)
if rsp.history:
    print '跳转的历史记录为:', rsp.history
    s1 = rsp.history[0].status_code
    print '首次挑战的返回码／类型：{}/{}'.format(s1, type(s1))
print '最后请求的头／url为：{}/{}'.format(rsp.headers, rsp.url)
print '最终的返回码:', rsp.status_code
print '返回值:', rsp.text
