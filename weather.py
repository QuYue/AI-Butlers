# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 01:11:52 2020
@author: QuYue
"""
import requests
import json
import time

def weather(tomorrow=False):
    url  = 'http://wthrcdn.etouch.cn/weather_mini?city=大连'
    response = requests.request("GET", url)
    a = eval(response.content)
    # print('城市'+a.get('data').get('city'))
    # print('未来几天的天气情况：')
    # for day in a.get('data').get('forecast'):
    #     print('日期:'+day['date'])
    #     print('\t最高温度:' + day['high'])
    #     print('\t风力:' + day['fengli'])
    #     print('\t最低温度:' + day['low'])
    #     print('\t风向:' + day['fengxiang'])
    #     print('\t类型:' + day['type'])
    # print('感冒：'+a.get('data').get('ganmao'))
    now=time.localtime()
    text = "#### **"+a.get('data').get('city')+'**'+'今日天气\n\n'
    day = a.get('data').get('forecast')[0]
    text += str(now.tm_year)+'年'+str(now.tm_mon)+'月'+day['date']+'\n\n'
    text += "最高温度: " + day['high'][3:]+'\n\n'
    text += "风力: " + day['fengli'].split('[')[2].split(']')[0]+'\n\n'
    text += "最低温度: " + day['low'][3:]+'\n\n'
    text += "风向: " + day['fengxiang']+'\n\n'
    text += "类型: " + day['type']+'\n\n'
    text += a.get('data').get('ganmao')

    if tomorrow:
        text += "\n\n#### **"+a.get('data').get('city')+'**'+'明日天气\n\n'
        day = a.get('data').get('forecast')[1]
        text += str(now.tm_year)+'年'+str(now.tm_mon)+'月'+day['date']+'\n\n'
        text += "最高温度: " + day['high'][3:]+'\n\n'
        text += "风力: " + day['fengli'].split('[')[2].split(']')[0]+'\n\n'
        text += "最低温度: " + day['low'][3:]+'\n\n'
        text += "风向: " + day['fengxiang']+'\n\n'
        text += "类型: " + day['type']+'\n\n'
    return text

if __name__ == '__main__':
    print(weather(True))