# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 20:28:51 2021

@author: Administrator
"""
import requests
import json
def translate(word = "数据分析师"):
    url='http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    #使用post需要一个链接
    data={'i': word,
          'from': 'zh-CHS',# 'AUTO'
          'to': 'en',# 'AUTO'
          'smartresult': 'dict',
          'client': 'fanyideskweb',
          'doctype': 'json',
          'version': '2.1',
          'keyfrom': 'fanyi.web',
          'action': 'FY_BY_REALTIME',
          'typoResult': 'false'}
    #将需要post的内容，以字典的形式记录在data内。
    r = requests.post(url, data)
    #post需要输入两个参数，一个是刚才的链接，一个是data，返回的是一个Response对象
    answer=json.loads(r.text)
    #你可以自己尝试print一下r.text的内容，然后再阅读下面的代码。
    result = answer['translateResult'][0][0]['tgt']
    return result

#from langdetect import detect
#from langdetect import detect_langs
#from langdetect import DetectorFactory
#DetectorFactory.seed = 0
#detect(result)
#detect_langs(result)
#import langid
#langid.classify(result)


def is_chinese(s = '数据分析师'):
    r=0
    try:
        for i in s:
            if u'\u4e00' <= i <= u'\u9fff':
                r=r+1
        if r>0:
            return True
        else:
            return False
    except:
        return False


def get_name(s = '数据分析师'):
    # 检测关键字是否存在中文，并将中文翻译成英文
    # import youdao as yd
    if is_chinese(s)==True:
        rs = translate(s)
    else:
        rs = s
    name = rs.replace(" ","_")
    return name