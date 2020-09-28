#/usr/bin/env python
# coding:utf-8
#  __author__ = 'guoew'
#  __date__ = '2018/2/1'
#  __Desc__ = 实现zabbix报警类邮件

import urllib, urllib2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import sys

def sendEmail(*args):
    sender = username
    receivers = sys.argv[1]  #获得外部第一个参数，第一个参数为邮件接收者 
    msgg = sys.argv[3] + "\n" #获得外部第三个参数，第三个参数为消息主体
    
    msg = MIMEMultipart()
    msg['Subject'] = sys.argv[2]  #获得外部第二个参数，第二个参数为邮件主题
    msg['From'] = sender
    msg['To'] = receivers
    

    puretext = MIMEText(msgg, _charset="utf-8")
    msg.attach(puretext)
    print "******************************下面执行发送****************"

    try:
        client = smtplib.SMTP_SSL()
        client.connect("smtp.example.com", 465)  #smtp服务器
        client.login(username, password)
        client.sendmail(sender, receivers.split(','), msg.as_string())
        client.quit()
    
        print '邮件发送成功！'
    except smtplib.SMTPRecipientsRefused:
        print 'Recipient refused'
    except smtplib.SMTPAuthenticationError as e:
        print e
    except smtplib.SMTPSenderRefused:
        print 'Sender refused'
    except smtplib.SMTPException, e:
        print e.message  

if __name__ == '__main__':
    username = 'fool@example.com'
    password = 'password'
    
    sendEmail(username,password)
