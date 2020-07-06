import json
import urllib.request
import string
from pypinyin import lazy_pinyin

def name_change(user_name):
    namepinyin = lazy_pinyin(user_name)
    new_name = ''
    for i in namepinyin:
        new_name += string.capwords(i) + ''
    new_name = new_name.strip()
    return new_name

def chatting(content, user, chatterID):
    api_url = "http://openapi.tuling123.com/openapi/api/v2"
    user_name = name_change(user)
    req = {
        "perception":
        {
            "inputText":
            {
                "text": content
            },

            "selfInfo":
            {
                "location":
                {
                    "city": "大连",
                    "province": "辽宁",
                    "street": "大连理工大学"
                }
            }
        },

        "userInfo": 
        {
            "apiKey": chatterID,
            "userId": user_name
        }
    }
    # 将字典格式的req编码为utf8
    req = json.dumps(req).encode('utf8')
    # print(req)

    http_post = urllib.request.Request(api_url, data=req, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(http_post)
    response_str = response.read().decode('utf8')
    # print(response_str)
    response_dic = json.loads(response_str)
    # print(response_dic)

    intent_code = response_dic['intent']['code']
    results_text = response_dic['results'][0]['values']['text']
    
    chat_code = intent_code
    if chat_code == 4003:
        reply = "I'm a little tired today. You'd better chat with me tomorrow."
    elif chat_code == 4007:
        reply = "I'm a little tired today. You'd better chat with me tomorrow."
    else:
        reply = results_text
    return chat_code, reply

if __name__ == '__main__':
    content = '你真帅'
    user = '普通人'
    chatterID = 'c0022c9c3c134d6fb331ec14f585a89f'
    code, reply = chatting(content, user, chatterID)
    print(f"{code}, {reply}")