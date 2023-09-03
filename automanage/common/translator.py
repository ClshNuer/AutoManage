#!/usr/bin/env python3
# -*- coding-utf-8 -*-
"""
docs:
https://fanyi-api.baidu.com/doc/21
https://fanyiapp.cdn.bcebos.com/api%2Fdemo%2FBaidu_Text_transAPI.rar
https://blog.csdn.net/qq_36944952/article/details/117697296
"""

import json
import random
import urllib
import hashlib
import http.client
import fire
from loguru import logger

import langid
import requests

headers = [
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 ' \
            'Firefox/4.0.1'
    },
    {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) ' \
            '(KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
    },
    {
        'User-Agent': 'Mozilla/4.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ ' \
            '(KHTML, like Gecko) Element Browser 5.0'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 ' \
            '(KHTML, like Gecko) Version/5.1 Safari/534.50'
    }
]
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

class BaiduTranslate(object):
    """
    Baidu Translate

    :param appid: 百度 appid
    :param appkey: 百度 appkey

    Example:
    # >>> # 示例 1: 直接传入 appid 和 secretKey, 不会生成密钥
    # >>> baiduTranslate = BaiduTranslate(appid, appkey)
    # >>> # 数据设置示例如下所示 2: 六位传入 appid 对应字段和 secretKey, 可以有多个 wont 自动装配会粉丝数据

        python translator.py main --text "hello world" # 翻译英文
        python translator.py translate_auto_to_other --text "你好，世界" --toLang "en" # 翻译中文
        # python translator.py main --text "hello world"
        # python translator.py main --text " 你好, 世界"

    Question:
        python translator.py main --text "hello, world" 时会出现报错，去掉逗号就不会报错
        lib\site-packages\langid\langid.py", line 273, in instance2fv
            state = self.tk_nextmove[(state << 8) + letter]
        TypeError: unsupported operand type(s) for +: 'int' and 'str'
    """
    # def __init__(self, appid, appkey, text):
    def __init__(self):
        # self.appid = appid
        self.appid = '20230608001705292'  # appid
        # self.appkey = appkey
        self.appkey = 'D1JAFUNpyjLZZthQy64y' # secretKey
        # self.text = text
        self.endpoint = 'http://api.fanyi.baidu.com'
        self.current_api = '/api/trans/vip/translate' # 通用翻译API HTTP地址
        self.url = self.endpoint + self.current_api

    def language_detect(self, text):
        """
        language detect
        """
        lang, _ = langid.classify(text)
        logger.debug(f"text lang : {lang}")
        return lang
        
    def make_md5(self, s):
        return hashlib.md5(s.encode('utf-8')).hexdigest()

    def translate_auto_to_other(self, text, fromLang = 'auto', toLang = 'zh'):
        lang = self.language_detect(text)
        if lang == toLang:
            logger.info(f"Text is already {toLang}, no need to translate.")
            return
        salt = random.randint(3276, 65536)
        sign = self.make_md5(self.appid + text + str(salt) + self.appkey)
        # url = f"{self.url}?appid={self.appid}&q={urllib.parse.quote(text)}" \
        #     f"&from={fromLang}&to={toLang}&salt={salt}&sign={sign}"
        payload = {
            'appid': self.appid,
            'q': text,
            'from': fromLang,
            'to': toLang,
            'salt': salt,
            'sign': sign
        }
        try:
            response = requests.post(self.url, params = payload, headers = headers)
            # response = requests.get(url, headers = headers)
            response.raise_for_status()
            new_text = response.json()
            logger.debug(new_text)
            return new_text
        except Exception as e:
            logger.error(e)
            return

    def main(self, text):
        self.translate_auto_to_other(text)

if __name__ == '__main__':
    fire.Fire(BaiduTranslate)
