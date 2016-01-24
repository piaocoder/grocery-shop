#!/usr/bi/env python
#coding: gbk

import sys
import os
import signal
import time

from g_log import mylog

import read_db
import g_conf
import position
import common
import user_login
import user_model
import segment
import insert_model
from pykafka import KafkaClient
import logging
import logging.config
import json
import re
import traceback
import threading
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import switch_log

myinsert = None

def init() :
	global myinsert

	t0 = time.time()
	# 加载词典和login_time
	if common.init_env() < 0 :
		return -1
	
	# 读取DB中的数据，载入缓存
	if read_db.read_tables() < 0 :
		return -1

	# 与xxxxx_rec库建立连接
	myinsert = insert_model.InsertModel()
	if myinsert.init_conn() < 0 :
		return -1

	# 对职位标题进行统计，建立索引
	if position.read_positions() < 0 :
		return -1	

	use_time = time.time() - t0
	mylog.log_notice('init() finished, uses time: %.2f secs [%.2f hours]'%(use_time, use_time/3600.0))
	return 0

def rec_offline() :
	'''
	离线更新用户兴趣
	'''
	global myinsert

	t0 = time.time()
	mylog.log_trace("begin rec_offline")
	if myinsert.ping() != 0 :
		mylog.log_fatal("ping mysql failed")
		return -1

	# 解析登录时间
	common.read_login_time()
	if user_login.parse_user_login() < 0 :
		return -1

	# 读取DB中的数据，载入缓存
	if read_db.read_tables() < 0 :
		return -1

	# 建立兴趣模型
	if user_model.build_models(myinsert) < 0 :
		return -1

	# 将login_time写入文件
	common.write_login_time(user_login.g_max_login_time_int)

	use_time = time.time() - t0
	mylog.log_notice('rec_offline() finished, uses time: %.2f secs [%.2f hours]' % \
						(use_time, use_time/3600.0))
	return 0

def release_resource() :
	'''
	释放资源(该函数目前没有被调用)
	'''

	global myinsert

	# 释放分词器
	mylog.log_trace('starting to release wordrank...')
	segment.release()
	mylog.log_trace('finished to release wordrank: <%d> seg lines'%(len(segment.line2seg)))
	
	# 释放数据库连接
	myinsert.close_conn()
	mylog.log_trace('release db connection')

	mylog.log_trace('resource have released')

def rec_intime():
	'''
	实时更新兴趣模型
	'''
	global myinsert

	#logging.config.fileConfig(g_conf.conf_path+"/logging.conf")
	logging.basicConfig()
	mylog.log_trace("begin rec_intime");

	deliver_topic = g_conf.deliver_topic
	deliver_group = g_conf.deliver_group
	broker1 = g_conf.deliver_broker
	deliver_zookeeper = g_conf.deliver_zookeeper

	interest_topic = g_conf.interest_topic
	broker2 = g_conf.interest_broker

	# 用于接收消息的kafka-client
	client1 = KafkaClient(hosts = broker1)
	topic1 = client1.topics[deliver_topic]
	consumer = topic1.get_balanced_consumer(consumer_group = deliver_group,
									zookeeper_connect = deliver_zookeeper)

	# 用于发送消息的kafka-client
	client2 = KafkaClient(hosts = broker2)
	topic2 = client2.topics[interest_topic]
	producer = topic2.get_producer()

	# 接收order消息
	receive_num = 0
	while True:
		message = consumer.consume()
		if message is not None :
			receive_num += 1
			# 每接收500条消息提交一次offset
			if receive_num % 500 == 0 :
				consumer.commit_offsets()
			try :
				order = json.loads(message.value)
				if order :
					status = order["orderStatus"]
					userid = order["userId"]
					positionid = order["positionId"]
					createtime = order["createTime"]
					line = "\t".join([str(userid),str(positionid),createtime,status])
					mylog.log_trace("RECEIVE MSG: %s" % line)
					# 只消费状态为WAIT和AUTO_FILTER的订单消息
					if status and userid and positionid and createtime \
								and (status=="WAIT" or status=="AUTO_FILTER") :
						now_tutple = datetime.datetime.now().timetuple()
						create_tuple = datetime.datetime.strptime(createtime, "%Y-%m-%d %H:%M:%S").timetuple()
						# 只消费当天产生的投递
						if now_tutple[:3] == create_tuple[:3]:
							# 更新该用户的兴趣
							if user_model.update_user_model(line, myinsert) >= 0 :
								mylog.log_debug("update user %d's interest success" % userid)
								# 发消息通知其他进程，该用户的兴趣已更新
								updatetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
								msg = {"userid":userid,"updatetime":updatetime,"delivertime":createtime}
								msg_str = json.dumps(msg)
								producer.produce([msg_str])
								mylog.log_trace("SEND MSG: %s" % msg_str)
			except :
				mylog.log_warning('update user interest intime error, raised exception : %s' % \
									traceback.format_exc())

if __name__ == '__main__' :
	mylog.log_trace("system start")
	mylog.log_trace('python version is: %s' % (sys.version.replace('\n', '|')))
	if init() < 0 :
		mylog.log_fatal("system init failed")
		sys.exit()
	# 开一个后台线程去实时更新用户兴趣
	thd = threading.Thread(target = rec_intime,)
	thd.setDaemon(True)
	thd.start()

	# 用apscheduler的问题在于：在任务开始调度的时间点上必须保证主线程和其他子线程已全部运行完毕，不占用CPU
	# 每天3:15进行rec_offline
	scheduler = BlockingScheduler()
	scheduler.add_job(rec_offline,'cron', hour='3',minute='15')
	scheduler.add_job(switch_log.switchLog,'cron', hour='0')
	try:
		scheduler.start()
	except (KeyboardInterrupt, SystemExit):
		mylog.log_fatal("add scheduler job raise exception: %s" % traceback.format_exc())
		scheduler.shutdown()
