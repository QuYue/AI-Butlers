import os
import subprocess
import random
import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse
from stack import Process_Stack
from XiaoMiSocket import Maid1_Commander
from weather import weather
from chatting import chatting

class Butler():
    def __init__(self, ID, name, secret, webhook):
        self.ID = ID
        self.name = name
        self.secret = secret
        self.webhook = webhook

    def get_sign(self):
        # 计算签名
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign

    def signed_webhook(self):
        # 加签
        timestamp, sign = self.get_sign()
        webhook = self.webhook+'&timestamp='+timestamp+'&sign='+sign
        return webhook

    def response(self, reply):
        if type(reply) == type(''):
            self.text_response(reply)
        elif type(reply) == type([]):
            if reply[0] == 'markdown':
                self.markdown_response(reply)
            else:
                self.text_response(reply)

    def text_response(self, reply):
        webhook = self.signed_webhook()
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

    def markdown_response(self, reply):
        webhook = self.signed_webhook()
        # 构建请求头部
        header = {"Content-Type": "application/json", "Charset": "UTF-8"}
        # 构建请求数据
        message ={"msgtype": "markdown",
                  "markdown": {"title": reply[1],
                    "text": reply[2]
                    },
                }
        # 对请求的数据进行json封装
        message_json = json.dumps(message)
        # 发送请求
        info = requests.post(url=webhook,data=message_json,headers=header)
        # 打印返回的结果
        print(info.text)
    
        

class Butler_Alfred(Butler):
    def __init__(self):
        self.ID = '$:LWCP_v1:$aQhMTAtIgfqDOZ+Y6qsX1hkbm8To5fEd'
        self.name = 'Alfred'
        self.secret = 'SEC85f9a48519284ab7ee45b82686f6e28039704e9aec3aff4f04f4062f878d27fd'
        self.webhook = "https://oapi.dingtalk.com/robot/send?access_token=94016c3f7bfc510156ea45fb88510d7721e9ce850e1f49d8fe1d59e702e54044"
        self.process_stack = Process_Stack()
        self.chatterID = 'd9b0bbaf848d4e108eea5591e55b80fa'

    def implement(self, content, user='stranger'):
        try:
            content = content.strip()
            if content[:4]=='www.': 
                # 读取网站
                cmd = 'chrome ' + content
                report = os.system(cmd)
                if report == 0:
                    reply = 'I have opened this website.'
                else:
                    reply = 'Sorry, I can not understand.'
            elif content == '天气' or content.lower() == 'weather':
                reply = ['markdown','Weather:', weather(True)]
            elif content == '开门' or content.lower() == 'open' or content.lower() == 'open the door':
                # 小米开关开门
                maid1_commander = Maid1_Commander()
                report = maid1_commander.command1()
                reply = report
            elif content == '门的状况' or content.lower() == 'door':
                # 小米开关的状况
                maid1_commander = Maid1_Commander()
                report = maid1_commander.command2()
                reply = f"Power:{report.power} | Temperature:{report.temperature}"
            elif content[:6].lower() == 'close ':
                # 关闭进程
                cmd = content[6:]
                report = self.process_stack.delete(cmd)
                if report[0]:
                    report[1].kill()
                    reply = f"{cmd} has been stopped."
                else:
                    reply = 'No need to close.'
            elif content[:2] == '关闭':
                # 关闭进程
                cmd = content[2:].strip()
                report = self.process_stack.delete(cmd)
                if report[0]:
                    report[1].kill()
                    reply = f"{cmd} has been stopped."
                else:
                    reply = 'No need to close.'
            elif content == '清空进程' or content.lower() == 'clear process':
                # 清空进程
                reply, clear_list = self.process_stack.clear()
                for process in clear_list:
                    process.kill()
            elif content == '查看进程' or content == '进程' or content.lower() == 'process':
                # 查看进程
                reply = self.process_stack.statistics()
            # elif content == '你好' or content == '嗨' or content.lower() == 'hello' or content.lower() == 'hi':
            #     # 夸奖
            #     r = random.randint(0,2)
            #     reply_list=['Hello.', "Hi.", "Glad to serve you."]
            #     reply = reply_list[r]
            # elif content == '干得漂亮' or content == '干得不错' or content == '做得不错' \
            #     or content == '做得漂亮' or  content == '谢谢' or content == '谢谢你' or content == '你真帅' \
            #     or content.lower() == 'good job' or content.lower() == 'well done' or content.lower() == 'nice' \
            #     or content.lower() == 'thank you' or content.lower() == 'thanks':
            #     # 夸奖
            #     r = random.randint(0,2)
            #     reply_list=['You are welcome.', "It's my pleasure.", "You're welcome."]
            #     reply = reply_list[r]
            else:
                # 执行cmd
                cmd = content
                try:
                    # 开启进程
                    p = subprocess.Popen(cmd)
                    self.process_stack.add(cmd, p)
                    reply = f"I have open {cmd}."                
                except:
                    # 聊天
                    code, reply = chatting(content, user, self.chatterID)
                    print(f"Chat Code:{code}")
            return reply
        except:
            # 出错
            return 'Something wrong with me.'

class Butler_WatchDog(Butler):
    def __init__(self):
        self.ID = '$:LWCP_v1:$YAVkoEiOgUnV0Gxcho4GJ8UoNh8J7t3x'
        self.name = '看门狗'
        self.secret = 'SEC81a276f50d5dc2e94dabfb7fdd7f75c628e5f678eb3409983125ea853c8384d7'
        self.webhook = "https://oapi.dingtalk.com/robot/send?access_token=d06752c825ed1e9d00d1d2034857fe3dc3e5a9bd98a4d0ebcd7d4ae2f27bed77"
        self.lasttime = time.localtime()
        self.chatterID = 'c0022c9c3c134d6fb331ec14f585a89f'

    def earliest(self):
        early = False
        now = time.localtime()
        if now.tm_mday != self.lasttime.tm_mday:
            self.early_response()
            early = True
        self.lasttime = now
        return early

    def early_response(self):
        # 构建请求头部
        webhook = self.signed_webhook()
        # 构建请求头部
        header = {"Content-Type": "application/json",
                "Charset": "UTF-8"}
        weathers = weather()
        # 构建请求数据
        message ={"msgtype": "markdown",
                "markdown": {
                    "title":"今日最早开门",
                    "text":"### 今日最早开门"+
                    "![screenshot](http://5b0988e595225.cdn.sohucs.com/images/20190121/73cc568180f449fa846818dd6e56fbc3.jpeg)\n\n" +
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

    def implement(self, content, user='stranger'):
        try:
            content = content.strip()
            if content == '天气' or content.lower() == 'weather':
                reply = ['markdown','Weather:', weather(True)]
            elif content == '开门' or content.lower() == 'open' or content.lower() == 'open the door':
                # 小米开关开门
                maid1_commander = Maid1_Commander()
                report = maid1_commander.command1()
                reply = report
                if self.earliest():
                    self.early_response()
            elif content == '门的状况' or content.lower() == 'door':
                # 小米开关的状况
                maid1_commander = Maid1_Commander()
                report = maid1_commander.command2()
                reply = f"Power:{report.power} | Temperature:{report.temperature}"
            # elif content == '你好' or content == '嗨' or content.lower() == 'hello' or content.lower() == 'hi':
            #     # 夸奖
            #     r = random.randint(0,2)
            #     reply_list=['Hello.', "Hi.", "Glad to serve you."]
            #     reply = reply_list[r]
            # elif content == '干得漂亮' or content == '干得不错' or content == '做得不错' \
            #     or content == '做得漂亮' or  content == '谢谢' or content == '谢谢你' or content == '你真帅' \
            #     or content.lower() == 'good job' or content.lower() == 'well done' or content.lower() == 'nice' \
            #     or content.lower() == 'thank you' or content.lower() == 'thanks':
            #     # 夸奖
            #     r = random.randint(0,2)
            #     reply_list=['You are welcome.', "It's my pleasure.", "You're welcome."]
            #     reply = reply_list[r]
            else:
                # 聊天
                code, reply = chatting(content, user, self.chatterID)
                print(f"Chat Code:{code}")
            return reply
        except:
            # 出错
            return 'Something wrong with me.'
        
class Butler_Lucius(Butler):
    def __init__(self):
        self.ID = '$:LWCP_v1:$P7hd6Cxkr3W29qYtgC8s+VRClrkPyY4r'
        self.name = 'Lucius'
        self.secret = 'SEC23b5e56a2c89eea70008ac05c33b0ad0c1ce6b4344b82590888788ff7dacf873'
        self.webhook = "https://oapi.dingtalk.com/robot/send?access_token=23980b365aa09feb59c29bd8ed928408817193afc925915e3731294083ccf043"
        self.lasttime = time.localtime()
        self.chatterID = "547c878963554230bb8a719d0f962f57"

    def implement(self, content, user= 'stranger'):
        try:
            content = content.strip()
            if content == '天气' or content.lower() == 'weather':
                reply = ['markdown','Weather:', weather(True)]
            elif content == '开门' or content.lower() == 'open' or content.lower() == 'open the door':
                # 小米开关开门
                maid1_commander = Maid1_Commander()
                report = maid1_commander.command1()
                reply = report
            elif content == '门的状况' or content.lower() == 'door':
                # 小米开关的状况
                maid1_commander = Maid1_Commander()
                report = maid1_commander.command2()
                reply = f"Power:{report.power} | Temperature:{report.temperature}"
            # elif content == '你好' or content == '嗨' or content.lower() == 'hello' or content.lower() == 'hi':
            #     # 夸奖
            #     r = random.randint(0,2)
            #     reply_list=['Hello.', "Hi.", "Glad to serve you."]
            #     reply = reply_list[r]
            # elif content == '干得漂亮' or content == '干得不错' or content == '做得不错' \
            #     or content == '做得漂亮' or  content == '谢谢' or content == '谢谢你' or content == '你真帅' \
            #     or content.lower() == 'good job' or content.lower() == 'well done' or content.lower() == 'nice' \
            #     or content.lower() == 'thank you' or content.lower() == 'thanks':
            #     # 夸奖
            #     r = random.randint(0,2)
            #     reply_list=['You are welcome.', "It's my pleasure.", "You're welcome."]
            #     reply = reply_list[r]
            else:
                # 聊天
                code, reply = chatting(content, user, self.chatterID)
                print(f"Chat Code:{code}")
            return reply
        except:
            # 出错
            return 'Something wrong with me.'




