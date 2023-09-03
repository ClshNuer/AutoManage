#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#https://mp.weixin.qq.com/s/FfgCnMrTPHIp7VxER74gaA


import time
import base64
import requests
from lxml import etree

import fire
from loguru import logger

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Cookie' : 'fofapro_ars_session=b34bfe980c5f5c287ee671a41418f869; \
        result_per_page=20',
    'Referer' : 'https://fofa.so/',
}

class SjtuEduSrc(object):
    def __init__(self):
        pass

    def get_school_name(self, r_url = "https://src.sjtu.edu.cn/", sign = 0):
        page_count = 208
        page_count = 5
        national_universities_num = 0 # 全国高校
        for page_num in range(1, page_count):
            url = f"{r_url}rank/firm/{national_universities_num}/?page={page_num}"
        
            try:
                result = requests.get(url).content.decode("utf-8")
                soup = etree.HTML(result)
                name = soup.xpath('//td[@class="am-text-center"]/a/text()')
                logger.debug('page -> ' + str(page_num))
                logger.debug(name)
                name = '\n'.join(name)
                with open(r'edu_name.txt', 'a+', encoding = 'utf-8') as f:
                    f.write(name + '\n')
            except Exception as e:
                logger.debug(e)
                time.sleep(0.5)

        # for num in range(1, 34):
        #     province_universities_num = num # 各省
        #     pu_num_api = f"rank/firm/{num}/"

    def fofa_search(self, search, page_num):
        proxies = {'http' : 'http://tps185.kdlapi.com:15818', 'https' : 'http://tps185.kdlapi.com:15818'}
        search = 'title="BIG-IP&reg;- Redirect"'
        bs_search = str(base64.b64encode(search.encode('utf-8')), 'utf-8')
        for page in range(1, page_num + 1):
            url = 'https://fofa.so/result?qbase64=' + bs_search + '&page=' + str(page)
            try:
                result = requests.get(url, headers = headers, proxies = proxies).content
                logger.debug(result.decode('utf-8'))
                soup = etree.HTML(result)
                # result_ip = soup.xpath('//*[@id="ajax_content"]/div/div/div/a/text()') # 获取a 便签的文本
                # result_ip = soup.xpath('//*[@id="ajax_content"]/div/div/div/a/@href') # 获取a 便签的href
                # result_ip = soup.xpath('//*[@target=" _blank"]/@href') # 获取符合条件的href 内容
                result_ip = soup.xpath('//div[@class="fl box-sizing"]/div[@class="re-domain"]/a[@target="_blank"]/@href') # 获取符合条件的href 内容
                logger.debug(f'正在爬取第{page}页: ')
                logger.debug(result_ip)
                result_ip = '\n'.join(result_ip)
                with open(r'edu-url.txt', 'a', encoding = 'utf-8') as f:
                    f.write(result_ip)
                    f.write('\n')
            except Exception as e:
                logger.error(e)
                logger.error('爬取失败')
            time.sleep(1)

if __name__ == "__main__":
    fire.Fire(SjtuEduSrc)
