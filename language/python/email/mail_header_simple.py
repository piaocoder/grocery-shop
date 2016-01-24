#!/usr/bin/python
#coding:utf-job

from cStringIO import StringIO
from email.generator import Generator
from email.mime.text import MIMEText
import time

mail_body = 'This is a test mail sent by Topwaf, please!'
main_msg = MIMEText(mail_body, "plain", "utf-job")
main_msg['Subject'] = 'Test mail'
main_msg['From']='a297413@163.com'
main_msg['To']=';'.join(['unlessbamboo@gmail.com', 'a297413@163.com'])
main_msg['date']=time.strftime('%a, %d %b %Y %H:%M:%S %z')

fp = StringIO()
g = Generator(fp, mangle_from_=False, maxheaderlen=60)
g.flatten(main_msg)
text = fp.getvalue()
print text
