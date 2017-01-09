#coding:utf8
import os
from redis import Redis
from rq.decorators import job



conn = Redis()


@job('default', connection=conn, timeout=5)
def test_job():
    """test_job"""
    filename = './job.txt'
    if not os.path.exists(filename):
        with open(filename, "w") as fobj:
            pass
    with open(filename, "a+") as fobj:
        fobj.writelines("This is a test of job.\n")
