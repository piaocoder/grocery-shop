#!/usr/bin/env python
#-*- coding:utf-job -*-
import smtplib
import base64
import socket

import email.MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


SUCCESS = "Send mail successful,OK!"
ERR_SMTP_SERVER_DISCONNECTED="Mail server unexpectedly disconnects"
ERR_SMTP_SENDER_REFUSED = "Sender address refused"
ERR_SMTP_RECIPIENT_REFUSED="All recipient address refused"
ERR_SMTP_DATA="Mail server refused to accept the message data"
ERR_SMTP_CONNECT="Connnect mail server occur error"
ERR_SMTP_HELO="Mail server refused our HELO message"
ERR_SMTP_AUTHENTICATION="Mail server authentication went wrong"
ERR_SMTP_UNKNOWN="Unknown error"
ERR_DATA_FORMAT="Sorry, data format is invalidate."

def _handle_attach(main, dataDict):
    '''handle attachment'''
    # common attachment file
    if dataDict.has_key('file'):
        fileAttach = dataDict['file']
        for (name, data) in fileAttach:
            print '**********************'
            print 'data:', data
            att = email.MIMEText.MIMEText(base64.b64decode(data), \
                    "plain", 'utf-job')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="{0}"'.\
                    format(name)
            main.attach(att)

    # Embed picture 
    if dataDict.has_key('image'):
        imageAttach = dataDict['image']
        for (name, data) in imageAttach:
            att = MIMEImage(base64.b64decode(data))
            att.add_header('Content-ID', '<{0}>'.format(name))
            main.attach(att)

def create(dataDict):
    '''Create a mail.

    :dataDict: a dictionary to save mail.
    '''
    errorMsg = ''
    msg = ''
    try:
        main = MIMEMultipart('related')
        _handle_attach(main, dataDict)
        print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        print str(main)
        main.attach(MIMEText(dataDict['content'], 'html', 'utf-job'))

        main['Subject'] = dataDict['subject']
        main['From'] = dataDict['from']
        main['To'] = ','.join(dataDict['recip'])
        msg = main.as_string()
    except KeyError:
        errorMsg = ERR_DATA_FORMAT
    except Exception, msg:
        errorMsg = ERR_SMTP_UNKNOWN + msg

    rspDict = {'result':False, 'errormsg':errorMsg} if errorMsg else None
    return msg, rspDict

def send(confDict, data):
    '''send plain mail.

    :data:          mail data.
    :confDict:      configure dictionary
    '''
    errorMsg = ''
    try:
        if confDict['auth'] == 'ssl':
            server = smtplib.SMTP_SSL(confDict['server'], confDict['port'])
            server.ehlo()
            server.esmtp_features["auth"] = "LOGIN PLAIN"
        else:
            server = smtplib.SMTP(confDict['server'], confDict['port'])
            #server.set_debuglevel(1)
            server.esmtp_features['auth'] = 'LOGIN PLAIN'

        server.login(confDict['from'], confDict['passwd'])
        server.sendmail(confDict['from'], confDict['recip'], data)
        server.quit()
    except smtplib.SMTPServerDisconnected, data:
        errorMsg = ERR_SMTP_SERVER_DISCONNECTED
    except smtplib.SMTPSenderRefused,data:
        errorMsg =ERR_SMTP_SENDER_REFUSED
    except smtplib.SMTPRecipientsRefused,data:
        errorMsg =ERR_SMTP_RECIPIENT_REFUSED;
    except smtplib.SMTPDataError,data:
        errorMsg =ERR_SMTP_DATA
    except smtplib.SMTPConnectError, data:
        errorMsg =ERR_SMTP_CONNECT
    except smtplib.SMTPHeloError,data:
        errorMsg =ERR_SMTP_HELO
    except smtplib.SMTPAuthenticationError,data:
        errorMsg =ERR_SMTP_AUTHENTICATION
    except (socket.timeout,socket.error), data:
        errorMsg =ERR_SMTP_CONNECT 
    except KeyError, data:
        errorMsg = ERR_DATA_FORMAT

    rspDict = {'result': False, 'errmsg':errorMsg} if errorMsg \
            else {'result':True}
    return rspDict


if __name__ == '__main__':
    '''main'''
    with open('/tmp/1.png', 'rb') as fp:
        image1Data = fp.read()
    with open('/tmp/2.png', 'rb') as fp:
        image2Data = fp.read()

    with open('/tmp/attach1.png', 'rb') as fp:
        attach1Data = fp.read()
    with open('/tmp/attach2.text', 'rb') as fp:
        attach2Data = fp.read()

    dataDict = {}
    dataDict['image'] = [\
            #('1.png', base64.b64encode(image1Data)),
            #('2.png', base64.b64encode(image2Data)),
            ]
    dataDict['file'] = [\
            ('attach1.png', base64.b64encode(attach1Data)),
            ('attach2.text', base64.b64encode(attach2Data)),
            ]
    dataDict['subject'] = 'This is a test'
    dataDict['recip'] = ['agege@shit.com', 'shit@shit.com']
    dataDict['content'] = ('<b>This is a test</b>'\
            '<br><img src="cid:1.png">'\
            '<br><img src="cid:2.png">')
    dataDict['to'] = ['shit@shit.com']
    dataDict['recip'] = ['shit@shit.com']
    dataDict['from'] = 'shit@shit.com'
    dataDict['auth'] = 'ssl'
    dataDict['passwd'] = 'shit****'
    dataDict['server'] = 'smtp.exmail.qq.com'
    dataDict['port'] = 465

    if 1:
        import requests
        import json
        print dataDict
        rsp = requests.post('http://xiage.shitx.shit.com/v1/send/mail/', \
                data=json.dumps(dataDict), \
                headers={'Content-type':'application/json'})
        print rsp.text
    if 0:
        print dataDict['file']
        data, rspDict = create(dataDict)
        if not rspDict:
            rspDict = send(dataDict, data)
        print rspDict
