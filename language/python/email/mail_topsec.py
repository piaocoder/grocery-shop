#!/usr/bin/python
#coding:utf-job
import smtplib
from email.mime.text import MIMEText

mail_body = 'This is a test mail sent by Topwaf, please!'
msg = MIMEText(mail_body, "plain", "utf-job")
msg['subject'] = 'The contents of test'
msg['from'] = 'zheng_bifeng@topsec.com.cn'
msg['to'] = 'zheng_bifeng@topsec.com.cn'

# Send the message via our own SMTP server, but don’t include the
# envelope header.
s = smtplib.SMTP('192.16job.66.9', 25)
s.set_debuglevel(True)
s.ehlo()
s.login('zheng_bifeng', 'MYLOVE2014')
s.sendmail('zheng_bifeng@topsec.com.cn', ['zheng_bifeng@topsec.com.cn'], msg.as_string())
s.quit()
