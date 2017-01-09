#coding:utf8
import time
from redis import Redis
from rq import Queue
from myworker import count_words_at_url


if __name__ == '__main__':
    qobj = Queue(connection=Redis())
    # 将一个worker推入队列中并等待处理
    for num in xrange(100):
        job = qobj.enqueue(\
                count_words_at_url, 
                'https://weixinshu.com/')
    print "当前的jobs数目为:{}.".format(len(qobj))
    # qobj.jobs工作实例队列，fetch_job(id)用于遍历所有对象
    print "所有的jobs id列表为：{}".format(qobj.job_ids)
    print job.result

    # 等待worker处理结束
    time.sleep(2)
    print job.result
