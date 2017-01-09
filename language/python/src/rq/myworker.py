#coding:utf8
import os
import requests


def count_words_at_url(url):
    """count_words_at_url
        rq中work和job不能处在同一个模块中，否则报错

    :param url:
    """
    resp = requests.get(url)
    len_value = len(resp.text.split())
    filename = './result.txt'
    if not os.path.exists(filename):
        with open(filename, "w") as fobj:
            pass

    with open(filename, "a+") as fobj:
        fobj.writelines("{}\n".format(len_value))
    return len_value
