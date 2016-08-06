#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
import base64
import socket
import sys
import os

import email.MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


sys.path.append("/data/python/")
import data as pythonVar


SUCCESS = "Send mail successful,OK!"
ERR_SMTP_SERVER_DISCONNECTED = "Mail server unexpectedly disconnects"
ERR_SMTP_SENDER_REFUSED = "Sender address refused"
ERR_SMTP_RECIPIENT_REFUSED = "All recipient address refused"
ERR_SMTP_DATA = "Mail server refused to accept the message data"
ERR_SMTP_CONNECT = "Connnect mail server occur error"
ERR_SMTP_HELO = "Mail server refused our HELO message"
ERR_SMTP_AUTHENTICATION = "Mail server authentication went wrong"
ERR_SMTP_UNKNOWN = "Unknown error"
ERR_DATA_FORMAT = "Sorry, data format is invalidate."


def _handle_attach(main, dataDict):
    '''handle attachment'''
    # common attachment file
    if 'file' in dataDict and not dataDict['file']:
        fileAttach = dataDict['file']
        for (name, data) in fileAttach:
            print '**********************'
            print 'data: ', data
            att = email.MIMEText.MIMEText(
                base64.b64decode(data), "plain", 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'filedir/attachment; "\
                "filename="{0}"'.format(name)
            main.attach(att)

    # Embed picture
    if 'image' in dataDict and not dataDict['image']:
        imageAttach = dataDict['image']
        for (name, data) in imageAttach:
            att = MIMEImage(base64.b64decode(data))
            att.add_header('Content-ID', '<{0}>'.format(name))
            main.attach(att)


def create(dataDict):
    '''Create a mail.

    : dataDict: a dictionary to save mail.
    '''
    errorMsg = ''
    msg = ''
    try:
        main = MIMEMultipart('related')
        _handle_attach(main, dataDict)
        print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        print str(main)
        main.attach(MIMEText(dataDict['content'], 'html', 'utf-8'))

        main['Subject'] = dataDict['subject']
        main['From'] = dataDict['from']
        main['To'] = ','.join(dataDict['recip'])
        msg = main.as_string()
    except KeyError:
        errorMsg = ERR_DATA_FORMAT
    except Exception, msg:
        errorMsg = '{}{}'.format(ERR_SMTP_UNKNOWN, msg)

    rspDict = {'result': False, 'errormsg': errorMsg} if errorMsg else None
    return msg, rspDict


def send(confDict, data):
    '''send plain mail.

    : data:          mail data.
    : confDict:      configure dictionary
    '''
    errorMsg = ''
    try:
        if confDict['auth'] == 'ssl':
            server = smtplib.SMTP_SSL(confDict['server'], confDict['port'])
            server.ehlo()
            server.esmtp_features["auth"] = "LOGIN PLAIN"
        else:
            server = smtplib.SMTP(confDict['server'], confDict['port'])
            # server.set_debuglevel(1)
            server.esmtp_features['auth'] = 'LOGIN PLAIN'

        server.login(confDict['from'], confDict['passwd'])
        server.sendmail(confDict['from'], confDict['recip'], data)
        server.quit()
    except smtplib.SMTPServerDisconnected, data:
        errorMsg = ERR_SMTP_SERVER_DISCONNECTED
    except smtplib.SMTPSenderRefused, data:
        errorMsg = ERR_SMTP_SENDER_REFUSED
    except smtplib.SMTPRecipientsRefused, data:
        errorMsg = ERR_SMTP_RECIPIENT_REFUSED
    except smtplib.SMTPDataError, data:
        errorMsg = ERR_SMTP_DATA
    except smtplib.SMTPConnectError, data:
        errorMsg = ERR_SMTP_CONNECT
    except smtplib.SMTPHeloError, data:
        errorMsg = ERR_SMTP_HELO
    except smtplib.SMTPAuthenticationError, data:
        errorMsg = ERR_SMTP_AUTHENTICATION
    except (socket.timeout, socket.error), data:
        errorMsg = ERR_SMTP_CONNECT
    except KeyError, data:
        errorMsg = ERR_DATA_FORMAT

    rspDict = {'result': False, 'errmsg': errorMsg} if \
        errorMsg else {'result': True}

    return rspDict


if __name__ == '__main__':
    '''main'''
    png1 = '/tmp/1.png'
    if os.path.exists(png1):
        with open(png1, 'rb') as fp:
            image1Data = fp.read()
    else:
        image1Data = None
    png2 = '/tmp/2.png'
    if os.path.exists(png2):
        with open(png2, 'rb') as fp:
            image2Data = fp.read()
    else:
        image2Data = None

    file1 = '/tmp/attach1.png'
    if os.path.exists(file1):
        with open(file1, 'rb') as fp:
            attach1Data = fp.read()
    else:
        attach1Data = None
    file2 = '/tmp/attach2.txt'
    if os.path.exists(file2):
        with open(file2, 'r') as fp:
            attach2Data = fp.read()
    else:
        attach2Data = None

    dataDict = {}
    dataDict['image'] = []
    if not image1Data:
        dataDict['image'].append(image1Data)
    if not image2Data:
        dataDict['image'].append(image2Data)

    dataDict['file'] = []
    if not attach1Data:
        dataDict['file'].append(attach1Data)
    if not attach2Data:
        dataDict['file'].append(attach2Data)

    dataDict['subject'] = 'This is a test'
    dataDict['content'] = ('<b>This is a test</b>'
                           '<br><img src="cid: 1.png">'
                           '<br><img src="cid: 2.png">')
    dataDict['recip'] = ['unlessbamboo@163.com']
    dataDict['from'] = pythonVar.MAIL_USERNAME
    dataDict['auth'] = 'ssl'
    dataDict['passwd'] = pythonVar.MAIL_PASSWD
    dataDict['server'] = pythonVar.MAIL_SERVER
    dataDict['port'] = pythonVar.MAIL_PORT

    if 0:
        import requests
        import json
        print dataDict
        rsp = requests.post(
            'http: //xiage.shitx.shit.com/v1/send/mail/',
            data=json.dumps(dataDict),
            headers={'Content-type': 'application/json'})
        print rsp.text

    if 1:
        print dataDict['file']
        data, rspDict = create(dataDict)
        if not rspDict:
            rspDict = send(dataDict, data)
        print rspDict
