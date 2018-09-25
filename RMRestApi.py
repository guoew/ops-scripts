# -*- coding:utf-8 -*-

import urllib
import urllib2
import json
from sdk import Aldstat
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import sys

class Api():
    def __init__(self):
        pass

    def resApi(self,url,data):
        data = urllib.urlencode(data)
        url = '%s%s%s' % (url,'?',data)
        print url
        try:
            headers = {"Authorization":"Basic *********"}
            req = urllib2.Request(url,headers=headers)
            res_data = urllib2.urlopen(req,timeout=10)
            res = res_data.read()
            return res
        except Exception as httperr:
            print httperr

    def appInfo(self,core):
        """获取applicationId finaltatus,className finishedTime"""
        j = json.loads(core)
        l = j['apps']["app"]
        print  len(l)
        #s = json.dumps(json.loads(core),sort_keys=True,indent=4)
        #with open('list.txt','w') as f:
        #    f.write(s)
        # for i in range(0,len(l)):
        #     print
        # sys.exit()

        app_info = []
        for i in range(0,len(l)):
            d = {}
            d['applicationId'] = l[i]["id"]
            d['finaltatus'] = l[i]["finalStatus"]
            d['className'] = l[i]["name"]
            d["finishedTime"] = l[i]["finishedTime"]

            app_info.append(d)
        return app_info
    def messFormat(self,mess):
        """告警信息格式化输出"""
        Id = mess["applicationId"]
        urllink = "http://ip:port/cluster/app/%s"  % Id
        mess_info = """
        <html>
          <head></head>
          <body>
                <p>
                   <dl>
                    <h3><dt><b>Details of the problem : </b></dt></h3><br>
                       <dd><b>ClassName:</b>  %s </dd><br>
                       <dd><b>ApplicationId:</b>  %s </dd><br>
                       <dd><b>FinalStatus:</b>  %s </dd><br>
                       <dd><b>FinishedTime:</b>  %s </dd><br>
                       <dd>See more details by clicking <a href="%s"> here </a> .</dd> <br>
                    </dl>
                </p>
            </pre>
          </body>
        </html>
        """ %(i["className"],i["applicationId"],i["finaltatus"],i["finishedTime"],urllink)
        return mess_info

    def resvers(self,data):
        """根据不同项目，发送不同接收者"""
        ops = "ops@aldwx.com"
        push_resevers = ops + ",push@aldwx.com"
        stat_resevers = ops + ",stat@aldwx.com"
        adx_resevers = ops + ",adx@aldwx.com"

        if str(data).find("game"):
            return  stat_resevers
        elif str(data).find("stat"):
            return stat_resevers
        elif str(data).find("push"):
            return push_resevers
        else:
            return adx_resevers

    def sendEmail(self,username,password,receivers,subject,mess_info):

        sender = username
        receivers = receivers
        msgg = str(mess_info) + "\n"
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receivers

        puretext = MIMEText(msgg,"html", _charset="utf-8")
        msg.attach(puretext)

        # for f in files:
        #     part = MIMEApplication(open(f,'rb').read())
        #     part.add_header('Content-Disposition', 'attachment', filename=f)
        #     #part.add_header('Content-Disposition', 'attachment', filename=f.decode('utf-8').encode('gbk'))
        #     msg.attach(part)

        print "******************************下面执行发送****************"
        try:
            client = smtplib.SMTP_SSL()
            client.connect("smtp.ym.163.com", 465)
            client.login(username, password)
            client.sendmail(sender, receivers.split(","), msg.as_string())
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

if __name__ == "__main__":
    username = 'guoew25@gmail.com'
    password = ''

    url = "http://ip:port/ws/v1/cluster/apps"
    data = {
        "username":"",
        "password":""
    }

    api = Api()
    core = api.resApi(url,data)

    app_info = api.appInfo(core)
    print len(app_info)

    with open('app_info.txt','r') as f:
        content = f.read()

    with open('app_info.txt','a') as f:
        for i in app_info:
            if i["finaltatus"] == "FAILED" or i["finaltatus"] == "KILLED":
                    isExist = content.find(i["applicationId"])
                    if isExist <= 0:
                        #receivers = api.resvers(i)
                        receivers = "guoerwei@aldwx.com"
                        subject = "Application " + i["className"] + " run error!!!"
                        mess_info = api.messFormat(i)

                        api.sendEmail(username,password,receivers,subject,mess_info)
                        f.write(str(i))
                        f.write("\n")
