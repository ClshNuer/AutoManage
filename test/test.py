#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import os
import re
import sys
import time
import glob
import json
import queue
import base64
import socket
import string
import logging
import difflib
import textwrap
import binascii
import argparse
import threading
import subprocess
import multiprocessing
from io import BytesIO
from pathlib import Path
from random import randint as rand
from random import choice as choice
import fire
from loguru import logger

import pywifi
import paramiko
import requests
# import mysql.connector
from pywifi import const
from lxml import etree, html
from ds_store import DSStore
from bs4 import BeautifulSoup
from selenium import webdriver
from colorama import Fore, init
from urllib.parse import urlparse
CUR_FOLDER = Path(__file__).parent.resolve()
from http.server import HTTPServer, SimpleHTTPRequestHandler




url = "http://120.78.174.238:8081/Page/MFinanceNEW/WageCalculationAccounts.aspx"

nums = range(1, 4695)
for num in nums:
    xpath = f'//*[@id="{num}"]'

raw_data = requests.get(url)
raw_data.encoding = 'utf-8'
content = raw_data.text

tree = html.fromstring(content)
links = tree.xpath('//a/@href')
logger.info(links)



# 创建一个浏览器对象
browser = webdriver.Chrome()

# 打开页面
browser.get(url)

# 点击弹框
browser.find_element_by_id("mname").click()

# 获取弹框中的数据
data = browser.find_element_by_id("id_of_data_element").get_attribute("value")
logger.info(data)

# 关闭浏览器
browser.quit()