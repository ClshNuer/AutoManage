#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import re
import ssl
import fire
from loguru import logger

import requests
from bs4 import BeautifulSoup


class Domain2Mail(object):
    """
    A class that represents a IP address
    
    Example:
        python domain2mail.py main --url = www.baidu.com --pages = 10
    """
    def __init__(self, url = None, urls = None, pages = None):
        self.url = url
        self.urls = urls
        self.pages = pages

    def ssl_verify(self):
        logger.info("SSL Version: " + str(ssl.OPENSSL_VERSION))
        logger.info("SSL HAS: " + str(ssl.HAS_TLSv1_2))
    
    def domain2mail(self, url, pages):
        email_sum = []
        key_words = ['email', 'mail', 'mailbox', '邮件', '邮箱', 'postbox']
        if pages >= 1:
            logger.info('Start searching emails...')
            for page in range(1, pages + 1):
                for key_word in key_words:
                    email_sum.extend(self.bing_search(url, page, key_word))
                    email_sum.extend(self.baidu_search(url, page, key_word))
        email_sum = list(set(email_sum))
        logger.info('Search emails finished!')
        if email_sum:
            for email in email_sum:
                logger.info('Find emails: ' + str(email))
        else:
            logger.info('No emails found!')

    def bing_search(self, url, page, key_word):
        conn = requests.session()
        engine = "https://cn.bing.com"
        referer = f"{engine}/search?q=email+site%3a{url}&qs=n&sp=-1&pq=emailsite%3a{url}&first=1&FORM=PERE"
        bing_url = f"{engine}/search?q={key_word}+site%3a{url}&qs=n&sp=-1&pq={key_word}site%3a{url}&first={str(page)}&FORM=PERE"
        # conn.get(engine, headers = self.headers(referer))
        r = conn.get(bing_url, stream = True, headers = self.headers(referer), timeout = 3)
        emails = self.search_emails(r.text)
        return emails

    def baidu_search(self, url, page, key_word):
        conn = requests.session()
        engine = "https://www.baidu.com"
        emails = []
        referer = f"{engine}/s?wd=email+site%3A{url}&pn=1"
        baidu_url = f"{engine}/s?wd={key_word}+site%3A{url}&pn={str((page-1)*10)}"
        # conn.get(referer, headers = self.headers(referer))
        r = conn.get(baidu_url, stream = True, headers = self.headers(referer), timeout = 3)
        tagh3 = BeautifulSoup(r.text, 'lxml').find_all('h3')
        for h3 in tagh3:
            href = h3.find('a').get('href')
            try:
                with requests.get(href, headers = self.headers(referer), timeout = 3) as response:
                    emails.extend(self.search_emails(response.text))
            except Exception as e:
                logger.error('Error: ' + str(e))
        return emails

    def search_emails(self, html):
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", html, re.I)
        if emails:
            emails = list(set(emails))
        return emails

    def headers(self, referer):
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                "(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            'Accept': '*/*',
            'Referer': referer,
            'Accept-Encoding': 'gzip, deflate'
        }
        return headers

    def main(self):
        self.ssl_verify()
        self.domain2mail(self.url, self.pages)

if __name__ == '__main__':
    fire.Fire(Domain2Mail)
    