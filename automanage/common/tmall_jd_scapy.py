#!/usr/bin/env python3
# -*- coding-utf-8 -*-

# tmall网站代码改进，爬取方式已不可用
# jd 可用

import os
import re
import json
import sqlite3
from urllib3 import *
from bs4 import BeautifulSoup

disable_warnings() # 忽略告警是不安全的选择，即证书报错会被忽略
manager = PoolManager() # 控制并发 http://www.cnblogs.com/shadowwalker/p/5283372.html

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

# response.data 出现乱码 中文解码 GB18030 确认乱码是奇数，偶数为UTF-8
def decoded_response_data(response):
    try:
        decoded_data = response.data.decode('gb18030')
    except UnicodeDecodeError:
        decoded_data = response.data.decode('utf-8')
    return decoded_data



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

# 获取所有相关商品ID
# xpath //*[@id="root"]/div/div[3]/div[1]/div[1]/div[2]/div[3]/div/div[1]/a
def get_tm_product_id_list(url):
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
        if re.match('.*[Mm][Aa][Tt][Ee]\s*60.', product_name.strip()):
            filter_product_id_list.append(product_id)

    return filter_product_id_list

# 获取某商品某一页的详情
def get_tm_json_detail(url, id, current_page):
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
def get_tm_last_page(url, id):
    # tmall_json = get_tm_json_detail(url, itemId, 1)
    return get_tm_json_detail(url, id, 1)['rateDetail']['paginator']['lastPage']

# # TMALL_MATE10_Final.py 运行爬虫模块
def tmall_scapy():
    file = "../data/phone_tmall.sqlite"
    spiderdb = SpiderDB(file)

    url = "https://s.taobao.com/search?fromTmallRedirect=true&q=mate%2060&spm=875.7931836%2FB.a2227oh.d100&tab=mall"
    product_id_list = get_tm_product_id_list(url)

    url = "https://h5api.m.tmall.com/h5/mtop.alibaba.review.list.for.new.pc.detail/1.0/?jsv=2.7.0&appKey=12574478&t=1696307461355&sign=fc53149fa8f15a9dd3b280b8275f38d1&api=mtop.alibaba.review.list.for.new.pc.detail&v=1.0&isSec=0&ecode=0&timeout=10000&ttid=2022%40taobao_litepc_9.17.0&AntiFlood=true&AntiCreep=true&preventFallback=true&type=jsonp&dataType=jsonp&callback=mtopjsonp4&data=%7B%22itemId%22%3A%22735607375083%22%2C%22bizCode%22%3A%22ali.china.tmall%22%2C%22channel%22%3A%22pc_detail%22%2C%22pageSize%22%3A20%2C%22pageNum%22%3A2%7D"

    for id in product_id_list:
        try:
            page_max_num = get_tm_last_page(url, id)
            for num in range(1, page_max_num + 1):
                tmall_json = get_tm_json_detail(url, id, num)
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
            print(e)
            continue

    spiderdb.close_db()

# tmall_scapy()

# ----------------------------------------------------------------
"""
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
Cache-Control: max-age=0
Cookie: unpl=JF8EALpnNSttC00GUUhRGxAWQw9dWw4KSUdWb2EBXA5RS1RWElZOFkd7XlVdXxRLFh9uZRRVVVNLUA4ZBisSEXtdVV9fD0oeBm5vNWRVCB4GBRlVSBp-SzMjGgdhKWECaz0MFW1bS2QEKwIcGhJIX11ZWw5LFgNsYQFRWVFMUgQrAysSGE9tZG5YCEoWAmdgBFNcaEpkBxoDHhYRTFxXWW1DJRZOb2ANVl5aQlMDHQIaEhNNWVFaVA9NFjNuVwY; __jdv=76161171|www.baidu.com|t_1003608409_|tuiguang|b7cebb1379c84b33ad1759b811b8ed5f|1696295736296; areaId=14; ipLoc-djd=14-1201-0-0; PCSYCityID=CN_340000_341700_0; shshshfpa=a959dee6-4899-9f73-c5f8-73fad3583010-1696295738; shshshfpx=a959dee6-4899-9f73-c5f8-73fad3583010-1696295738; jsavif=1; jsavif=1; rkv=1.0; avif=1; __jda=122270672.1693238677101275458670.1693238677.1693238677.1696295736.2; __jdc=122270672; wlfstk_smdl=lf7t81tycurcklp18p7dft85zruodxqz; TrackID=1Ty2HkcfnluCgr4Q-CY8TVI2A791I5HDMR6gvDpKGRxe015AA4pY0qJw4MpYdyfooiu4WnCD3onFSIVXzEPMfyR4tUzKNtfQvp2fxtxXkSd8; thor=55018F716877E68CFFC02B69FADA341937E2A79907EB2698CF1D5DF37E97DF3B14AF42F10F4BCBDB051DD8C7846875CFF794B7B99E59AD27AECA8493C8AB078973ED2A3B5D3FCBBF54655A086415E895F37A97330DFFD146E4475402404959F8ACA063A1EAA342E1E7703317AC108B89E0C66B060DC5E74C50B9354FFB5A344F3FB531985EB2DBDE614F2D3E8070608465B1372A6C6F4D1F7DB83673FC4F6F33; flash=2_lOyeU55DWeUfACZlQERQz-JvihR5oJB3L9gwg_LdeD8sIHiuYRff9K9VlWgXbS7KK-0kYzhBmGEhGzqRm29sZ08A-vJVYJfUmzJJVae5pDK*; pinId=kvHy4wYOfZDEvvK1A4KPD7V9-x-f3wj7; pin=jd_788313e804f90; unick=jd_173440zeh; ceshi3.com=000; _tp=xVi9xjrkpXx0ZXY7eZ25AG3h%2Bff4gof4jh8GQOgrmDQ%3D; _pst=jd_788313e804f90; qrsc=3; __jdb=122270672.9.1693238677101275458670|2.1696295736; shshshsID=d2e7eb3d850abcc0587cc293bd31efcd_4_1696297412818; shshshfpb=AAi9pNPOKElne5kiZn3PF-HP601gwEBaWKVc4RQAAAAA
Referer: https://search.jd.com/Search?keyword=mate%2060&enc=utf-8&wq=mate%2060&pvid=b5c51eec39b746ca9b595ec04fdcddbe
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
file = "../data/head_jd.txt"
headers = get_headers(file) # 读取头部信息，主要读取Cookie 值

# 获取所有相关商品ID
# xpath //*[@id="J_goodsList"]/ul/li[1]/div/div[1]/a
def get_jd_product_id_list(url):
    response = manager.request('GET', url, headers = headers)
    decoded_data = decoded_response_data(response)
    xpath = '//*[@id="J_goodsList"]/ul/li[1]/div/div[1]/a'

    soup = BeautifulSoup(decoded_data, 'lxml')
    tags = soup.find_all(href = re.compile('//item.jd.com/'))
    links = ['http:' + tag['href'].replace('#comment', '') for tag in tags]
    links = list(set(links))
    # pattern = r'\d+'
    # # id_list = [link for link in links if re.search(pattern, link).group()]
    # id_list = [re.search(pattern, link).group() for link in links if re.search(pattern, link)]
    
    filter_product_id_list = []
    for link in links:
        response = manager.request('GET', link, headers = headers)
        decoded_data = decoded_response_data(response)
        soup = BeautifulSoup(decoded_data, 'lxml')
        product_name = soup.find('div', class_ = 'sku-name').text
        if re.match('.*[Mm][Aa][Tt][Ee]\s*60.', product_name.strip()):
            filter_product_id_list.append(re.search(r'\d+', link).group())

    return filter_product_id_list

# 获取某商品某一页的详情
def get_jd_json_detail(url, id, current_page):
    # match = re.match('.+callback=(.*)&productId=(.*)&score.+&page=(.*)&pageSize.+', url)
    # default_id, page_num, callback = match.groups()
    match = re.match('.+productId=(.*)&score=.+&page=(.*)&pageSize.+', url)
    default_id, page, = match.groups()
    url = url.replace(default_id, str(id))

    new_url = url.split('&page=')[0] + '&page=' + str(current_page) + '&pageSize' + url.split('&pageSize')[1]
    response = manager.request('GET', new_url, headers = headers)
    decoded_data = decoded_response_data(response)
    jd_json = json.loads(decoded_data)

    return jd_json

# 获取某商品详情的最后一页
def get_jd_last_page(url, id):
    return get_jd_json_detail(url, id, 1)['maxPage']

# # JD_MATE10_Final.py 运行爬虫模块
def jd_scapy():
    file = "../data/phone_jd.sqlite"
    spiderdb = SpiderDB(file)

    url = "https://search.jd.com/search?keyword=mate%2060&qrst=1&wq=mate%2060&ev=exbrand_%E5%8D%8E%E4%B8%BA%EF%BC%88HUAWEI%EF%BC%89%5Eexprice_6000gt%5E&pvid=a9fbc27c178147b4a520f33eedc4f1e1&psort=3&click=0"
    product_id_list = get_jd_product_id_list(url)

    url = "https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&client=pc&clientVersion=1.0.0&t=1696305958461&loginType=3&uuid=122270672.1693238677101275458670.1693238677.1696301008.1696303375.4&productId=100065092578&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1&bbtf=&shield="
    
    for id in product_id_list:
        try:
            page_max_num = get_jd_last_page(url, id)
            for num in range(1, page_max_num + 1):
                jd_json = get_jd_json_detail(url, id, num)
                comments = jd_json['comments']
                for comment in comments:
                    discuss = comment['content']
                    productColor = comment['productColor']
                    createTime = comment['creationTime']
                    productSite = comment['productSize']
                    print(productColor, productSite, discuss, createTime)
                    spiderdb.insert(str(id), productColor, productSite, '京东', discuss, createTime)
                    spiderdb.commit()
        except Exception as e:
            print(e)
            continue

    spiderdb.close_db()

jd_scapy()