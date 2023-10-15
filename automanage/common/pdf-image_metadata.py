#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import os
import re
from urllib.parse import urlsplit
from io import FileIO as file

import exifread
from urllib3 import *
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup

def pdf_metadata(file_name):
    pdf_file = PdfReader(file(file_name, 'rb'))
    doc_info = pdf_file.metadata
    print(f"[*] PDF MetaData For: {file_name}")
    for key, value in doc_info.items():
        print(f"[+] {key}: {value}")

def get_image_gps(file_name):
    gps = {}
    date = ''
    tags = exifread.process_file(open(file_name, 'rb').read())

    tag_map = {
        'GPS GPSLatitudeRef': 'GPSLatitudeRef',
        'GPS GPSLongitudeRef': 'GPSLongitudeRef',
        'GPS GPSAltitudeRef': 'GPSAltitudeRef',
        'GPS GPSLatitude': 'GPSLatitude',
        'GPS GPSLongitude': 'GPSLongitude',
        'GPS GPSAltitude': 'GPSAltitude'
    }

    for tag, value in tags.items():
        if tag in tag_map:
            key = tag_map[tag]
            if key in ('GPSLatitude', 'GPSLongitude'):
                try:
                    value = value.values
                    gps[key] = value[0].num, value[1].num, value[2].num / value[2].den
                except:
                    gps[key] = repr(value)
            elif key == 'GPSAltitudeRef':
                gps[key] = value.values[0]
            else:
                gps[key] = repr(value)
        elif tag.endswith('Date'):
            date = repr(value)
    return {"GPS 信息": gps, "时间信息": date}

def find_images(url, manager):
    print('发现URL 上的图片文件：' + url)
    response = manager.request('GET', url).data
    soup = BeautifulSoup(response, 'lxml')
    images_tags = soup.find_all('img')
    prefix = 'http://' + '/'.join(url.split('/')[2:-1]) + '/'
    # prefix = url.replace(os.path.basename(urlsplit(url)[2]), '')
    images_url = [prefix + images_tag['src'] for images_tag in images_tags]
    return images_url

def download_images(images_url, images_file_path, manager):
    images_file_name = []
    print("开始下载文件...")
    for image_url in images_url:
        try:
            image_content = manager.request('GET', image_url).data 
            image_file_name = os.path.basename(urlsplit(image_url)[2])
            image_file_path = os.path.join(images_file_path, image_file_name)
            with open(image_file_name, 'wb') as image_file:
                image_file.write(image_content)
            image_file_name = str(images_file_path) + str(image_file_name)
            images_file_name.append(image_file_path)
        except Exception as e:
            print(e)
    
    print(f'下载完成, 共下载 {len(images_file_name)} 张图片')
    return images_file_name

def download_find_gps(url, images_file_path):
    images_url = find_images(url)
    images_file_name = download_images(images_url, images_file_path)

    for image_file_name in images_file_name:
        print(os.path.basename(image_file_name) + ': ' + get_image_gps(image_file_name))

if __name__ == '__main__':
    manager = PoolManager()

    pdf_path = '../data/pdf_test.pdf'
    image_path = '../data/image_test.jpg'
    pdf_metadata(pdf_path)
    get_image_gps(image_path)

    url = 'http://www.image.com/gps/gps.html'
    find_images(url, manager)

