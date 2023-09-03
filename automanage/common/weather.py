#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import time
import json
import random
import fire
from loguru import logger

import requests
from lxml import etree
import csv

key = 'c5b0947203624ef1ab99dfb3bd9cdc0c'
headers = [
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
    },
    {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'
    },
    {
        'User-Agent': "Mozilla/4.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ " \
            "(KHTML, like Gecko) Version/5.0 Safari/533.16"
    },
    {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 " \
            "(KHTML, like Gecko) Version/5.1 Safari/534.50"
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
            '(KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
]
city_to_cityID = {
    'beijing': 'CN101010100',
    'shanghai': 'CN101020100',
    'zhengzhou': 'CN101180101',
    "xi'an": 'CN101110101',
    'chengdu': 'CN101270101',
    'wuhan': 'CN101200101',
    'changsha': 'CN101250101',
    'guangzhou': 'CN101280101',
    'shenzhen': 'CN101280601',
    'hangzhou': 'CN101210101',
    'nanjing': 'CN101190101'
}

class Weather(object):
    """
    Get weather info.
    """
    def __init__(self):
        pass
    
    # ----------------- https://devapi.qweather.com -----------------
    def qcityId(self):
        city = random.choice(list(city_to_cityID.keys()))
        cityID = city_to_cityID[city]
        return [city, cityID]

    def qweatherHour(self, url, city, cityID):
        hour_data = []
        try:
            url = f"{url}/v7/weather/now?location={cityID}&key={key}"
            raw_data = requests.get(url, headers = random.choice(headers))
            time.sleep(1)
            if raw_data.status_code == 200:
                minute_data = json.loads(raw_data.text)
                hour_data = {
                    "city": city, "updateTime": minute_data["updateTime"],
                    "temp": minute_data["now"]["temp"], "feelsLike": minute_data["now"]["feelsLike"],
                    "text": minute_data["now"]["text"], "windDir": minute_data["now"]["windDir"],
                    "windScale": minute_data["now"]["windScale"], "humidity": minute_data["now"]["humidity"],
                    "precip": minute_data["now"]["precip"], "pressure": minute_data["now"]["pressure"],
                    "vis": minute_data["now"]["vis"], "cloud": minute_data["now"]["cloud"]
                }
                logger.debug(hour_data)
            else:
                logger.error(f"HTTP Error: {raw_data.status_code}")
        except Exception as e:
            logger.error(f"Get {city} weather info failed, Exception: {e}")
        return hour_data
    
    def show_qweather(self, url, num):
        logger.info(f"Start to use weather API to get weather info: {url}")
        hour_datas = []
        for i in range(num):
            city, cityID = self.qcityId()
            hour_data = self.qweatherHour(url, city, cityID)
            hour_datas.append(hour_data)
        logger.info(f"Get weather info finished.")
        return hour_datas
    
    def qweather_to_csv(self, url, num, file_name):
        hour_datas = self.show_qweather(url, num)
        with open(file_name, 'w', newline = '', encoding = 'utf-8') as csvfile:
            fieldnames = ['city', 'updateTime', 'temp', 'feelsLike', 'text', 'windDir', 'windScale', 'humidity', 'precip', 'pressure', 'vis', 'cloud']
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
            writer.writeheader()
            for hour_data in hour_datas:
                writer.writerow(hour_data)

    # ----------------- http://lishi.tianqi.com -----------------
    def tqcity(self, url):
        logger.info(f"Start to get cities from {url}")
        # session = requests.Session()
        # session.headers.update(random.choice(headers))
        # try:
        #     raw_data = session.get(url)
        #     raw_data.raise_for_status()
        #     html = etree.HTML(raw_data.text)
        #     cities = [element.xpath('./a/@href')[0].split('/')[0] for element in html.xpath('//li[a/@target="_blank"]')[1:]]
        #     logger.debug(cities)
        # except requests.exceptions.RequestException as e:
        #     logger.error(f"HTTP Error: {e}")
        #     cities = []
        raw_data = requests.get(url, headers = random.choice(headers))
        cities = []
        if raw_data.status_code == 200:
            html = etree.HTML(raw_data.text)
            elements = html.xpath('//li[a/@target="_blank"]')[1:]
            for element in elements:
                city = element.xpath('./a/@href')[0]
                city = city.split('/')[0]
                if city == 'http:' or city == 'https:' or city == '':
                    continue
                cities.append(city)
            # logger.debug(cities)
            logger.debug(f'Total cities: {len(cities)}, get cities finished.')
        else:
            logger.error(f"HTTP Error: {raw_data.status_code}")
        return cities

    def tqdate(self, start, end):
        # month 1 - 12
        return [f'{year}{month:02d}' for year in range(start, end) for month in range(1, 13)]
    
    def tqweather_month(self, url, city, date):
        if not date.isdigit() or len(date) != 6:
            logger.error(f"Date: {date} is not valid.")
            return []
        url = f'{url}/{city}/{date}.html'
        raw_data = requests.get(url, headers = random.choice(headers))
        time.sleep(1)
        html = etree.HTML(raw_data.text)
        li_list = html.xpath('//ul[@class="thrui"]/li')
        month_data = [{
            'date_time': li.xpath('./div[1]/text()')[0].split(' ')[0],
            'city': city,
            'high': li.xpath('./div[2]/text()')[0].replace('℃', ''),
            'low': li.xpath('./div[3]/text()')[0].replace('℃', ''),
            'weather': li.xpath('./div[4]/text()')[0].strip() if li.xpath('./div[4]/text()') else 'N/A'
        } for li in li_list]
        return month_data
    
    def tqweather_day(self, month_data, day):
        if day < 1 or day > len(month_data):
            logger.error(f'Invalid day: {day}')
            day_data = []
        else:
            day_data = month_data[day-1]
        logger.debug(f'{day_data}')
        return day_data

    def show_tqweather(self, url, start, end):
        cities = self.tqcity(url)
        months = self.tqdate(start, end)

        city = random.choice(cities)
        month = random.choice(months)
        day = random.randint(1, 31)
        
        month_data = self.tqweather_month(url, city, month)
        day_data = self.tqweather_day(month_data, day)
        year_data = []
        return day_data, month_data

    def tqweather_to_csv(self, url, start, end, file_name):
        day_data, month_data = self.show_tqweather(url, start, end)
        with open(file_name, 'w', newline = '', encoding = 'utf-8') as csvfile:
            fieldnames = ['date_time', 'city', 'high', 'low', 'weather']
            writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
            writer.writeheader()
            for data in month_data:
                writer.writerow(data)

    def main(self):
        qweather_url = "https://devapi.qweather.com"
        file_name = '..\\data\\qweather.csv'
        num = 10000
        # self.show_qweather(qweather_url, num)
        self.qweather_to_csv(qweather_url, num, file_name)
        

        tq_url = 'http://lishi.tianqi.com'
        file_name = '..\\data\\tqweather.csv'
        [start, end] = [2021, 2022]
        # self.show_tqweather(tq_url, start, end)
        # self.tqweather_to_csv(tq_url, start, end, file_name)

if __name__ == '__main__':
    fire.Fire(Weather)
