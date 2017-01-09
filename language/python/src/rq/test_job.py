#coding:utf8
import time
from jobworker import test_job


if __name__ == '__main__':
    job = test_job.delay()
    time.sleep(1)
    print job.result
