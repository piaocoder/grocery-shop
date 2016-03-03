import requests


def getRecord(url, timeout=5, **kwargs):
    return requests.get(url, timeout=timeout, **kwargs)

def putRecord(url, data=None, timeout = 5,**kwargs):
    return requests.put(url, timeout=5, data=data, **kwargs)

url = "http://10.1.200.7:8080/basic_module/devops:201510221255"

for i in range(20):
    r1 = getRecord(url, headers={"Accept":"application/json"})
    print r1
    print 'xxxxxxxxxxxxxxxxxxxxxxxx'
    r2 = requests.get(url, headers={"Accept":"application/json"})
    print r2

import pdb
pdb.set_trace()
url = "http://10.1.200.7:8080/basic_module/devops:201510221552"
paydata = '{"Row": [{"key": "ZGV2b3BzOjIwMTUxMDIyMTU1Mg==", "Cell": [{"column": "aW86cmVhZF9ieXRlcw==", "$": "MC4wMA=="}, {"column": "bmV0OmJ5dGVzX3NlbnQ=", "$": "NjAzNC4wMA=="}, {"column": "bmV0OmJ5dGVzX3JlY3Y=", "$": "MTI1MDIuMDA="}, {"column": "Y3B1Omlvd2FpdA==", "$": "MC4xNQ=="}, {"column": "bWVtOm1lbXBlcmNlbnQ=", "$": "NTEuMjQ="}, {"column": "aW86d3JpdGVfdGltZQ==", "$": "MTYuMDA="}, {"column": "Y3B1OnNvZnRpcnE=", "$": "MC4wNw=="}, {"column": "bmV0OmVycmlu", "$": "MC4wMA=="}, {"column": "bmV0OmRyb3BvdXQ=", "$": "MC4wMA=="}, {"column": "bmV0OmRyb3Bpbg==", "$": "MC4wMA=="}, {"column": "Y3B1OnN5c3RlbQ==", "$": "MC43Mw=="}, {"column": "Y3B1OnVzZWQ=", "$": "NC4yMQ=="}, {"column": "bmV0OnBhY2tldHNfc2VudA==", "$": "NjguMDA="}, {"column": "bmV0OnBhY2tldHNfcmVjdg==", "$": "MTQ4LjAw"}, {"column": "bmV0OmVycm91dA==", "$": "MC4wMA=="}, {"column": "aW86cmVhZF90aW1l", "$": "MC4wMA=="}, {"column": "Y3B1OnVzZXI=", "$": "MS41Mw=="}, {"column": "aW86d3JpdGVfY291bnQ=", "$": "Ny4wMA=="}, {"column": "Y3B1OmlycQ==", "$": "MC4wMw=="}, {"column": "aW86d3JpdGVfYnl0ZXM=", "$": "NTY0NzAuMDA="}, {"column": "aW86cmVhZF9jb3VudA==", "$": "MC4wMA=="}]}]}'
r3 = putRecord(url, data = paydata, headers={"Content-Type":"application/json"})
print r3

url = "http://10.1.200.7:8080/basic/false-row-key"
paydata = '{"Row": [{"key": "201510221605", "Cell": [{"column": "Y3B1OnN5c3RlbQ==", "$": "MC4zNTIwMjE4NTc5MjQ="}, {"column": "bmV0OmRyb3Bpbg==", "$": "MC4w"}, {"column": "aW86cmVhZF9ieXRlcw==", "$": "MC4w"}, {"column": "Y3B1Omlvd2FpdA==", "$": "MC4xOTg5ODkwNzEwMzg="}, {"column": "bmV0OnBhY2tldHNfc2VudA==", "$": "NS4w"}, {"column": "aW86d3JpdGVfYnl0ZXM=", "$": "ODQ5NzguMA=="}, {"column": "aW86d3JpdGVfdGltZQ==", "$": "MjMuMA=="}, {"column": "Y3B1OnNvZnRpcnE=", "$": "MC4wNDkzNDQyNjIyOTUx"}, {"column": "bmV0OmVycmlu", "$": "MC4w"}, {"column": "bWVtOm1lbXBlcmNlbnQ=", "$": "ODguMw=="}, {"column": "Y3B1OmlycQ==", "$": "MC4w"}, {"column": "Y3B1OnVzZWQ=", "$": "Mi45MDI2Nzc1OTU2Mw=="}, {"column": "bmV0OmRyb3BvdXQ=", "$": "MC4w"}, {"column": "bmV0OmJ5dGVzX3JlY3Y=", "$": "MTEzNi4w"}, {"column": "bmV0OmJ5dGVzX3NlbnQ=", "$": "MTA3Ni4w"}, {"column": "aW86cmVhZF90aW1l", "$": "MC4w"}, {"column": "aW86d3JpdGVfY291bnQ=", "$": "Ny4w"}, {"column": "Y3B1OnVzZXI=", "$": "MC42MDgxNjkzOTg5MDc="}, {"column": "bmV0OmVycm91dA==", "$": "MC4w"}, {"column": "bmV0OnBhY2tldHNfcmVjdg==", "$": "Ny4w"}, {"column": "aW86cmVhZF9jb3VudA==", "$": "MC4w"}]}, {"key": "201510221605", "Cell": [{"column": "Y3B1OnN5c3RlbQ==", "$": "MC43MDgxOTY3MjEzMTE="}, {"column": "bmV0OmRyb3Bpbg==", "$": "MC4w"}, {"column": "aW86cmVhZF9ieXRlcw==", "$": "MjY4NS4w"}, {"column": "Y3B1Omlvd2FpdA==", "$": "MC4xOTgzNjA2NTU3Mzg="}, {"column": "bmV0OnBhY2tldHNfc2VudA==", "$": "MTQuMA=="}, {"column": "aW86d3JpdGVfYnl0ZXM=", "$": "MjkxNDIuMA=="}, {"column": "aW86d3JpdGVfdGltZQ==", "$": "MTIuMA=="}, {"column": "Y3B1OnNvZnRpcnE=", "$": "MC4xNDc1NDA5ODM2MDc="}, {"column": "bmV0OmVycmlu", "$": "MC4w"}, {"column": "bWVtOm1lbXBlcmNlbnQ=", "$": "MTQuMTY1NTczNzcwNQ=="}, {"column": "Y3B1OmlycQ==", "$": "MC4wMzI3ODY4ODUyNDU5"}, {"column": "Y3B1OnVzZWQ=", "$": "NS4xNTU3Mzc3MDQ5Mg=="}, {"column": "bmV0OmRyb3BvdXQ=", "$": "MC4w"}, {"column": "bmV0OmJ5dGVzX3JlY3Y=", "$": "MTM1NTUuMA=="}, {"column": "bmV0OmJ5dGVzX3NlbnQ=", "$": "MzkwMC4w"}, {"column": "aW86cmVhZF90aW1l", "$": "MS4w"}, {"column": "aW86d3JpdGVfY291bnQ=", "$": "NS4w"}, {"column": "Y3B1OnVzZXI=", "$": "Mi40MjQ1OTAxNjM5Mw=="}, {"column": "bmV0OmVycm91dA==", "$": "MC4w"}, {"column": "bmV0OnBhY2tldHNfcmVjdg==", "$": "MTkzLjA="}, {"column": "aW86cmVhZF9jb3VudA==", "$": "MC4w"}]}]}'
r4 = putRecord(url, data = paydata, headers={"Content-Type":"application/json"})
print r4
