#!/usr/bin/python
#coding:utf-8
import smtplib
from email.mime.text import MIMEText

filename = raw_input(">>>Input filename:")
fp = open(filename, "rb")
# create a text/plain message
msg = MIMEText(fp.read())
fp.close()

msg['subject'] = 'The contents of %s'%filename
msg['from'] = 'a297413@163.com'
msg['to'] = 'unlessbamboo@google.com'

# Send the message via our own SMTP server, but don’t include the
# envelope header.
s = smtplib.SMTP('smtp.163.com', 25)
s.set_debuglevel(True)
s.ehlo()
s.login('a297413', 'zbf104641719')
s.sendmail('a297413@163.com', ['unlessbamboo@gmail.com'], msg.as_string())
s.quit()
