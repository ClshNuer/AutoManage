#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import time
import json
import random
import fire
from loguru import logger

import requests
from lxml import etree
from typing import Dict, List

HEADERS = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
            "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 " \
            "(KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 " \
            "Firefox/54.0"
    }
]

SITE = "https://www.555dd1.com"

class Movie(object):
    """
    555dy movie spider
    
    Example:
        python 555dy.py main
        # python 555dy.py movie_update_list
        # python 555dy.py movie_rank_list
    """
    def __init__(self, url = None):
        self.url = url

    def movie_update_list(self) -> Dict[str, str]:
        """
        Get the movie update list from 555dy.com

        Returns:
            movie_dict: a dict of movie name and url
        """
        pages = 20 # only crawl the first 20 pages
        movie_dict = {}
        movie_api = f"/label/new/page/"
        xpath = '//div[@class="module-items module-poster-items"]//a[@class="module-poster-item module-item"]'
        for page in range(1, pages + 1):
            url = f"{SITE}/label/new/page/{page}.html"
            logger.info(f"正在爬取第 {page} 页，URL: {url}")
            header = random.choice(HEADERS)
            raw_data = requests.get(url, header)
            for element in etree.HTML(raw_data.text).xpath(xpath):
                title = element.get('title')
                href = element.get('href')
                movie_dict[title] = SITE + href
                logger.debug(f"电影名: {title}, URL: {SITE + href}")
                time.sleep(3)
        return movie_dict

    def movie_rank_list(self):
        movie_api = f"/label/hot.html"
        url = f"{SITE}/label/hot.html"
        
        logger.info(f"正在爬取 {url}")
        header = random.choice(HEADERS)
        with requests.get(url, header) as response:
            response.encoding = 'utf-8'
            raw_data = response.text

        time_frames = ['overall', 'month', 'week', 'day']
        movie_type = ['film', 'tv_series', 'welfare', 'anime', 'variety_record']
        movie_names = {} # 4 * 5 * 10 = 200

        root_xpath = '/html/body/div/div[3]/div/div/div' # overall, month, week, day # rank 1-5, 6-10, 11-15, 16-20
        sub_xpath = './div/div/div/div' # film, tv_series, welfare, anime, variety_record
        rank_name_xpath = f'./div[1]/h3' # list name
        top_xpath = f'./div[2]/a' # top name
        href_xpath = './@href' # movie href link
        top_num_xpath = f'./div[1]' # top 1-10
        movie_name_xpath = f'./div[2]/span' # movie name
        html = etree.HTML(raw_data)
        root_elements = html.xpath(root_xpath)[2:]
        # movie_elements = [top_element for root_element in root_elements for sub_element in root_element.xpath(sub_xpath) for top_element in sub_element.xpath(top_xpath)]
        # for i, top_element in enumerate(movie_elements):
        #     href = top_element.xpath(href_xpath)[0]
        #     movie_url = SITE + href
        #     top_num_element = top_element.xpath(top_num_xpath)[0]
        #     top_num = top_num_element.text
        #     movie_name_element = top_element.xpath(movie_name_xpath)[0]
        #     movie_name = movie_name_element.text
        #     logger.debug(f"排名: {top_num}, 名称: {movie_name}, URL: {movie_url}")
        for root_index, root_element in enumerate(root_elements):
            movie_names[time_frames[root_index]] = {}
            sub_elements = root_element.xpath(sub_xpath)
            for sub_index, sub_element in enumerate(sub_elements):
                movie_names[time_frames[root_index]][movie_type[sub_index]] = {}
                rank_name_element = sub_element.xpath(rank_name_xpath)[0]
                rank_name = rank_name_element.text
                logger.debug(rank_name)
                top_elements = sub_element.xpath(top_xpath)
                for top_index, top_element in enumerate(top_elements):
                    movie_names[time_frames[root_index]][movie_type[sub_index]][str(top_index)] = {}
                    href = top_element.xpath(href_xpath)[0]
                    movie_url = SITE + href
                    top_num_element = top_element.xpath(top_num_xpath)[0]
                    top_num = top_num_element.text
                    movie_name_element = top_element.xpath(movie_name_xpath)[0]
                    movie_name = movie_name_element.text
                    logger.debug(f"排名: {top_num}, 名称: {movie_name}, URL: {movie_url}")
                    # movie_names[time_frames[root_index]][movie_type[sub_index]][top_index]['top'] = top_num
                    movie_names[time_frames[root_index]][movie_type[sub_index]][str(top_index)]['name'] = movie_name
                    movie_names[time_frames[root_index]][movie_type[sub_index]][str(top_index)]['url'] = movie_url

        return movie_names
    
    def write_to_json(self, movie_dict: Dict[str, str], file_name: str):
        with open(file_name, 'w', encoding = 'utf-8') as f:
            f.write(json.dumps(movie_dict, indent=4, ensure_ascii=False))

    def main(self):
        file_name = '..\\data\\movie_rank_list.json'
        # movies = self.movie_update_list()
        movie_names = self.movie_rank_list()
        self.write_to_json(movie_names, file_name)

if __name__ == "__main__":
    fire.Fire(Movie)

