#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import re
import json
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
    headerDict = {}
    with open(file, 'r') as f:
        headersText = f.read()
        headers = re.split('\n', headersText)
        for header in headers:
            result = re.split(':', header, maxsplit = 1)
            headerDict[result[0]] = result[1].strip()
    return headerDict

print(get_headers('../data/head_tm.txt'))

class SpiderDB(object):
    """
    将爬取的数据写入数据库
    """
    pass

# # TMALL_Def.py
# 获取某商品某一页的详情
def getJSONDetail(url, itemId, currentPage):
    re_result = re.match('.+itemId=(.+)&spuId.+&currentPage=(.+)&append.+callback=(.+)$', url).groups()
    url_itemID = re_result[0]
    url_currentPage = re_result[1]
    url_callback = re_result[2]

    url = url.replace(url_itemID, str(itemId))
    url1 = url.split('&currentPage=')
    url2 = url.split('&append')
    url = url1[0] + '&currentPage=' + str(currentPage) + '&append' + url2[1]
    
    r = http.requent('GET', url, headers = headers)
    c = r.data.decode('GB18030')
    c = c.replace(url_callback + '(', '')
    c = c.replace(')', '')
    c = c.replace('false', '"false"')
    c = c.replace('true', '"true"')
    tmalljson = json.loads(c)

    return tmalljson

# 获取某商品详情的最后一页
def getLastPage(url, itemId):
    tmalljson = getJSONDetail(url, itemId, 1)
    return tmalljson['rateDetail']['paginator']['lastPage']

def getProductIdList():
    headers = get_headers('head_tm.txt') # 读取头部信息，主要读取Cookie 值
    disable_warnings() # 忽略告警是不安全的选择，即证书报错会被忽略
    http = PoolManager() # 用于控制并发 http://www.cnblogs.com/shadowwalker/p/5283372.html

    url = "https://list.tmall.com/search_product.html?spm=a220m.1000858l1000724.4.2f"
    r = http.request('GET', url, headers = headers)
    c = r.data.decode('GB18030')

    soup = BeautifulSoup(c, 'lxml')
    data_id_list = []
    div_product = soup.find_all('div', class_ = 'product')
    for data_id in div_product:
        data_id_list.append(data_id.attrs['data-id'])

    return_id_list = []
    for item in data_id_list:
        url = "https://detail.tmall.com/item.htm?id=" + item
        r = http.request('GET', url, headers = headers)
        r = r.data.decode('GB18030')
        soup = BeautifulSoup(r, 'lxml')
        item_name = soup.find('div', class_ = 'tb-detail-hd').text
        if re.match('.*[Mm][Aa][Tt][Ee]\s*10.'.item_name.strip()):
            return_id_list.append(item)

    return return_id_list


# 获取所有相关商品ID
def getProductId():
    pass


def main():
    print(get_headers('head_tm.txt'))
    pass


# # TMALL_MATE10_Final.py 运行爬虫模块
