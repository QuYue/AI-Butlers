#%%
import http.client
import hashlib
import urllib
import random
import json

#%%
def language_dict():
    lang_dict = {'zh':'中文', 'en':'英语', 'yue':'粤语', 'wyw': '文言文', 
                 'jp': '日语', 'kor': '韩语', 'fra': '法语', 'spa': '西班牙语',
                 'th': '泰语', 'ara': '阿拉伯语', 'ru': '俄语', 'pt': '葡萄牙语',
                 'de': '德语', 'it': '意大利语', 'el': '希腊语', 'nl': '荷兰语',
                 'pl': '波兰语', 'bul': '保加利亚语', 'est': '爱沙尼亚语', 
                 'dan': '丹麦语', 'fin': '芬兰语', 'cs': '捷克语', 'rom': '罗马尼亚语',
                 'slo': '斯洛文尼亚语', 'swe': '瑞典语', 'hu': '匈牙利语', 
                 'cht': '繁体中文', 'vie': '越南语'}
    return lang_dict

def print_language():
    lang_dict = language_dict()
    lang = [f"{i}"+' '*(5-len(str(i)))+f"{lang_dict[i]}" for i in lang_dict.keys()]
    print_lang = ''
    for i in lang:
        print_lang += i + '\n'
    return print_lang
    

def Tolang(content):
    def is_contains_chinese(strs):
        for char in strs:
            if '\u4e00' <= char <= '\u9fa5':
                return True
        return False
    content = content.strip()
    c = content
    if c[0] == '-':
        lang = c[1:].split(' ')[0]
        c = content[len(lang)+2:]
        lang_dict = language_dict()
        if lang in lang_dict.keys():
            return lang, c
        elif lang in lang_dict.values():
            lang = list(lang_dict.keys())[list(lang_dict.values()).index(lang)]
            return lang, c

    if is_contains_chinese(c):
        return 'en', content
    else:
        return 'zh', content

def BaiduTranslate(word, toLang='zh'):
    def out(words):
        output = ''
        for word in words:
            output += word+' '
        return output
    appid = '20200722000524169'  # 填写你的appid
    secretKey = 'XHQTaatI6j2_DCcsuaMZ'  # 填写你的密钥

    httpClient = None
    myurl = '/api/trans/vip/translate'

    fromLang = 'auto'   #原文语种
    toLang = toLang   #译文语种
    salt = random.randint(32768, 65536)
    q= word
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
    salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        result = [i['dst'] for i in result['trans_result']]
        
        result = out(result)

        return result#['trans_result'][0]['dst']
    except Exception as e:
        print (e)
        return 'Error'
    finally:
        if httpClient:
            httpClient.close()

#%%
if __name__ == "__main__":
    a = BaiduTranslate("""Research and practice have demonstrated that integration of healthcare information has become essential for health informatics. Such integrated healthcare information systems are able to provide more comprehensive healthcare services than those where various information sources are disconnected. In this paper,
we construct an integrated health information database called LipperNet, which
consolidates heterogeneous information sources such as medical organizations,
doctors and medical research publications, etc. in China. Then, we conduct
some basic statistical analysis, such as checking the correlations among doctors
from their co-authorship networks, the spatial distribution of different levels of
hospitals, the doctor specialty distribution in different locations, etc., to show
the big potential of this database on understanding the current status of health
network in China. We hope this database could be an important resource to
help advance the health informatics research in China and improve the quality
of healthcare delivery.""")

# %%
