#!/usr/bin/python
#coding:utf-8

#Import smtplib for the actual sending function
import os
import smtplib

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

me = "a297413@163.com"
family = ["unlessbamboo@gmail.com"]

COMMASPACE = ','
# Create the container (outer) email message.
msg = MIMENonMultipart()
msg['Subject'] = 'Our family reunion'
# me == the sender's email address
# family = the list of all recipients' email addresses
msg['From'] = me
msg['To'] = COMMASPACE.join(family)
msg.preamble = 'Our family reunion'

# Assume we know that the image files are all in PNG format
dirname = raw_input(">>>Input dirname:")
pngfiles = os.listdir(dirname)
for file in pngfiles:
    # Open the files in binary mode. Let the MIMEImage class automatically
    # guess the specific image type.
    file = dirname + "/" + file
    fp = open(file, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

# Send the email via our own SMTP server.
s = smtplib.SMTP('smtp.163.com', 25)
s.login('a297413', 'zbf104641719')
s.sendmail(me, family, msg.as_string())
s.quit()
