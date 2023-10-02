#!/usr/bin/env python3
# -*- coding-utf-8 -*-

# 网站代码改进，爬取方式已不可用

import os
import re
import json
import sqlite3
from urllib3 import *
from bs4 import BeautifulSoup

# # Spider_Def.py
"""
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cache-Control: max-age=0
Cookie: _samesite_flag_=true; cookie2=199f3aa5faf10d4e620eed2b9b503d90; t=4b02134ccc8242cbe4d7e243f2dca63a; _tb_token_=73b675e7fdf3a; cna=m1agHZ+v8yICASShRJqsDBg6; sgcookie=E100fcfeATWT2I3bKt1Lm1Grb2gHpUPH7%2FE3kDmi4XLOUYo%2F4Ea7yAyjT1%2BDrbRllclZ83eZGdEi5X%2FhpKhKOSUls3mkK1KF%2Bz2jdjSPc4UUxQE%3D; unb=4197911411; uc3=lg2=UtASsssmOIJ0bQ%3D%3D&vt3=F8dCsGupzUj8wmFuTQ0%3D&nk2=F5RFgtebLzegEqM%3D&id2=Vy0aOcndF0YBPw%3D%3D; csg=976d3501; lgc=tb025255690; cancelledSubSites=%5B%22xianyu%22%5D; cookie17=Vy0aOcndF0YBPw%3D%3D; dnk=tb025255690; skt=21103ea75627eafe; existShop=MTY5NjE2NDE3Mw%3D%3D; uc4=nk4=0%40FY4O63BunDry88eLMgr8eHX%2BJM8IWw%3D%3D&id4=0%40VXqUOEXM40VSlM%2BHq19fMDG8aNBl; tracknick=tb025255690; _cc_=VT5L2FSpdA%3D%3D; _l_g_=Ug%3D%3D; sg=01d; _nk_=tb025255690; cookie1=B0arGrMSBoimz4ft8kfQKF7bcruqxgcv5SNs048HW6Q%3D; uc1=cookie15=W5iHLLyFOGW7aA%3D%3D&cookie14=Uoe9a7rE%2BhB0KA%3D%3D&existShop=false&cookie21=VFC%2FuZ9aiKCaj7AzMHh1&pas=0&cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D; _m_h5_tk=742824769372c88746c8655c9aaa0012_1696198580213; _m_h5_tk_enc=8d9f88b8e1d252a53840e98b8d52ad45; JSESSIONID=25CE8ECAEB6526BA1A13591EE16D3E82; l=fBN2N36rPNwEqIzCBO5Zourza77tmQRf1sPzaNbMiIEGa6MFMFTKMNCtCBVDydtjgTCv0FKyMAhYGdeeSG4pgKbgjKtrCyConxvtaLcYX; isg=BL-_UEVs5u_L5uLzKSZX2TUbTpNJpBNGkCD4FFGO-G60YNziXHeClnByojCeOOu-
Referer: https://www.tmall.com/
Sec-Ch-Ua: "Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36
"""

# 将请求报文的字符串转为HTTP Headers
def get_headers(file):
    headers = {}
    with open(file, 'r') as f:
        headers_text = f.read()
        headers_list = re.split('\n', headers_text)
        for header in headers_list:
            header_type, header_value = re.split(':', header, maxsplit = 1)
            headers[header_type] = header_value.strip()
    return headers

class SpiderDB:
    """
    将爬取的数据写入数据库
        id 唯一ID；itemid 产品ID；color 产品颜色；size 内存大小；source 数据源；discuss 客户评论；time 时间
    """
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = self.connect_db()
        self.cursor = self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        sql_cmd = """create table phone_sales
                            (id integer primary key autoincrement not null,
                            itemid text not null,
                            color text,
                            size text,
                            source text not null,
                            discuss mediumtext not null,
                            time text not null);"""
        cursor.execute(sql_cmd)
        return cursor

    def connect_db(self):
        if os.path.exists(self.dbname):
            os.remove(self.dbname)
        conn = sqlite3.connect(self.dbname)
        return conn

    def insert(self, itemid, color, size, source, discuss, time):
        sql_cmd = """insert into phone_sales(itemid, color, size, source, discuss, time)
                        values('%s', '%s', '%s', '%s', '%s', '%s')""" % (itemid, color, size, source, discuss, time)
        self.cursor.execute(sql_cmd)

    def commit(self):
        self.conn.commit()

    def close_db(self):
        self.cursor.close()
        self.conn.close()

# # TMALL_Def.py
file = "../data/head_tm.txt"
headers = get_headers(file) # 读取头部信息，主要读取Cookie 值
disable_warnings() # 忽略告警是不安全的选择，即证书报错会被忽略
manager = PoolManager() # 控制并发 http://www.cnblogs.com/shadowwalker/p/5283372.html

# response.data 出现乱码 中文解码 GB18030 确认乱码是奇数，偶数为UTF-8
def decoded_response_data(response):
    try:
        decoded_data = response.data.decode('gb18030')
    except UnicodeDecodeError:
        decoded_data = response.data.decode('utf-8')
    return decoded_data

# 获取所有相关商品ID
# xpath //*[@id="root"]/div/div[3]/div[1]/div[1]/div[2]/div[3]/div/div[1]/a
def get_product_id_list(url):
    response = manager.request('GET', url, headers = headers)
    decoded_data = decoded_response_data(response)
    xpath = '//*[@id="root"]/div/div[3]/div[1]/div[1]/div[2]/div[3]/div/div[1]/a'

    soup = BeautifulSoup(decoded_data, 'lxml')
    product_list = soup.find_all('div', class_ = 'product ')
    product_id_list = [data_id.attrs['data-id'] for data_id in product_list]

    filter_product_id_list = []
    for product_id in product_id_list:
        url = "https://detail.tmall.com/item.htm?id=" + product_id
        response = manager.request('GET', url, headers = headers)
        decoded_data = decoded_response_data(response)
        soup = BeautifulSoup(decoded_data, 'lxml')
        product_name = soup.find('div', class_ = 'tb-detail-hd').text
        if re.match('.*[Mm][Aa][Tt][Ee]\s*10.', product_name.strip()):
            filter_product_id_list.append(product_id)

    return filter_product_id_list

# 获取某商品某一页的详情
def get_json_detail(url, id, current_page):
    # match = re.match('.+id=(.+)&spuId.+&ns=(.+)&append.+abbucket=(.+)&', url)
    # default_id, page_num, callback = match.groups()
    match = re.match('.+abbucket=(.+)&id=(.+)&ns=(.+)&', url)
    if match:
        callback, default_id, page_num = match.groups()
    else:
        return 
    url = url.replace(default_id, str(id))
    # new_url = url.split('&currentPage=')[0] + '&currentPage=' + str(current_page) + '&append' + url.split('&append')[1]
    new_url = url.split('&abbucket=')[0] + '&abbucket=' + str(callback) + '&id=' + url.split('&id')[1]
    response = manager.request('GET', new_url, headers = headers)
    decoded_data = decoded_response_data(response)
    decoded_data = decoded_data.replace(callback + '(', '').replace(')', '').replace('false', '"false"').replace('true', '"true"')

    # tmall_json = json.loads(decoded_data)
    # return tmall_json

# 获取某商品详情的最后一页
def get_last_page(url, id):
    # tmall_json = get_json_detail(url, itemId, 1)
    return get_json_detail(url, id, 1)['rateDetail']['paginator']['lastPage']




# # TMALL_MATE10_Final.py 运行爬虫模块
file = "../data/phone_tmall.sqlite"
spiderdb = SpiderDB(file)

url = "https://s.taobao.com/search?fromTmallRedirect=true&q=mate%2060&spm=875.7931836%2FB.a2227oh.d100&tab=mall"
product_id_list = get_product_id_list(url)

url = "https://detail.tmall.com/item.htm?abbucket=15&id=735607375083&ns=1&spm=a21n57.1.0.0.56da523czTDZ4t&sku_properties=5919063:6536025"

for id in product_id_list:
    try:
        page_max_num = get_last_page(url, id)
        for num in page_max_num:
            tmall_json = get_json_detail(url, id, num)
            rate_list = tmall_json['rateDetail']['rateList']

            for rate in rate_list:
                rateContent = rate_list[rate]['rateContent']
                colorSize = rate_list[rate]['auctionSku']
                color, msize = re.split('[:;]', colorSize)[3], re.split('[:;]', colorSize)[7]
                msize = msize + 'GB'
                dtime = rate_list[rate]['rateDate']
                spiderdb.insert(id, color, msize, '天猫', rateContent, dtime)
                spiderdb.commit()
    except Exception as e:
        continue

spiderdb.close()
