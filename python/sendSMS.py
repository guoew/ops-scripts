#!/usr/bin/env python
#coding:utf-8
from qcloudsms_py import SmsMultiSender
from qcloudsms_py.httpclient import HTTPError
from qcloudsms_py import QcloudSms

def sendSMS(appid,appkey,template_id,phone_numbers,params):
    # 短信模板ID，需要在短信应用中申请
    template_id = template_id  # NOTE: 这里的模板ID`7839`只是一个示例，真实的模板ID需要在短信控制台中申请
    #template_id = 236103  # NOTE: 这里的模板ID`7839`只是一个示例，真实的模板ID需要在短信控制台中申请
    # 签名
    sms_sign = "腾讯云"  # NOTE: 这里的签名"腾讯云"只是一个示例，真实的签名需要在短信控制台中申请，另外签名参数使用的是`签名内容`，而不是`签名ID`
    msender = SmsMultiSender(appid, appkey)
    try:
        result = msender.send_with_param(86, phone_numbers,
            template_id, params, sign=sms_sign, extend="", ext="")   # 签名参数未提供或者为空时，会使用默认签名发送短信
        print(dir(msender.send_with_param))
    except HTTPError as e:
        print(e)
    except Exception as e:
        print(e)
    
    return result


#if __name__ == "__main__":
    
# 短信应用SDK AppID
appid = 1400xxxxx  # SDK AppID是1400开头
# 短信应用SDK AppKey
appkey = "xxxxxxxxxxxxxxxxxx"
# 需要发送短信的手机号码
phone_numbers = ["187xxxx1193",]

#短信参数
params = ['one','two','three']
#params = ["5678"]
    

sendSMS(appid,appkey,phone_numbers,params)

