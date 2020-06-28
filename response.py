import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse
from weather import weather

def get_sign():
    # 计算签名
    timestamp = str(round(time.time() * 1000))
    secret = 'SEC85f9a48519284ab7ee45b82686f6e28039704e9aec3aff4f04f4062f878d27fd'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign

def signed_webhook(webhook):
    # 加签
    timestamp, sign = get_sign()
    webhook = webhook+'&timestamp='+timestamp+'&sign='+sign
    return webhook

def text_message(reply):
    # 请求的URL，WebHook地址
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=94016c3f7bfc510156ea45fb88510d7721e9ce850e1f49d8fe1d59e702e54044"
    webhook = signed_webhook(webhook)
    # 构建请求头部
    header = {"Content-Type": "application/json",
              "Charset": "UTF-8"}
    # 构建请求数据
    message ={"msgtype": "text",
              "text": {"content": reply},
              #"at": {"isAtAll": True}
              }
    # 对请求的数据进行json封装
    message_json = json.dumps(message)
    # 发送请求
    info = requests.post(url=webhook,data=message_json,headers=header)
    # 打印返回的结果
    # print(info.text)
def early_response():
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=94016c3f7bfc510156ea45fb88510d7721e9ce850e1f49d8fe1d59e702e54044"
    webhook = signed_webhook(webhook)
    # 构建请求头部
    header = {"Content-Type": "application/json",
            "Charset": "UTF-8"}
    weathers = weather()
    # 构建请求数据
    message ={"msgtype": "markdown",
            "markdown": {
                "title":"今日最早开门",
                "text":"### 今日最早开门@15542443091\n"+
                "> ![screenshot](http://5b0988e595225.cdn.sohucs.com/images/20190121/73cc568180f449fa846818dd6e56fbc3.jpeg)\n\n" +
                weathers
                },

            "at": {"atMobiles": [
                    "15542443091"], 
                    "isAtAll": False}
            }
    # 对请求的数据进行json封装
    message_json = json.dumps(message)
    # 发送请求
    info = requests.post(url=webhook,data=message_json,headers=header)
    # 打印返回的结果
    print(info.text)
if __name__=="__main__":
    early_response()