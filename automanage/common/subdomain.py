#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import fire
from loguru import logger

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Subdomain(object):
    """
    Subdomain class

    Example:
        python subdomain.py main --site=baidu.com --pages=5
    """
    def __init__(self, site = None, pages = None):
        self.site = site
        self.pages = pages

    def bing_search(self, site, pages):
        subdomains = []
        header = self.headers()
        session = requests.Session()
        soup = BeautifulSoup('', 'html.parser')
        for page in range(1, pages + 1):
            url = f"https://cn.bing.com/search?q=site%3a{site}&go=Search&qs=ds&first={str((page - 1) * 10)}&FORM=PERE"
            with session.get(url, headers = header) as html:
                soup = soup.__class__(html.content, 'html.parser')
            job_bt = soup.select('h2 a')
            for i in job_bt:
                link = i.get('href')
                domain = urlparse(link).scheme + "://" + urlparse(link).netloc
                if domain in subdomains:
                    continue
                subdomains.append(domain)
                logger.info(domain)
        return subdomains

    def headers(self):
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 " \
                "(KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': "https://cn.bing.com/search?q=site%3abaidu.com&sp=-1&pq=site%3a" \
                "baidu.com&sc=0-14&sk=&cvid=8D311FFB4F3C4F5E8F1F2F2F0F2F0F2F&first=1&FORM=PERE",
            'Cookie': "SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=8D311FFB4F3C4F5E8F1F2F2F0F2F0F2F; " \
                "SRCHUSR=DOB=20190801&T=1564705372000; _EDGE_V=1; MUID=2F0F2F0F2F0F2F0F; " \
                "MUIDB=2F0F2F0F2F0F2F0F; SRCHHPGUSR=CW=1920&CH=969&DPR=1&UTC=480&WTS=637009" \
                "75472; _EDGE_S=mkt=zh-cn&SID=2F0F2F0F2F0F2F0F; _SS=SID=2F0F2F0F2F0F2F0F&HV=156" \
                "4710000; ipv6=hit=1564713600018&t=4; _EDGE_CD=u=zh-cn",
        }
        return header
    
    def main(self):
        # site = self.site
        # pages = self.pages
        self.bing_search(self.site, self.pages)

if __name__ == '__main__':
    fire.Fire(Subdomain)