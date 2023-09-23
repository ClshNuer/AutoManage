import re
import fire
import requests
from bs4 import BeautifulSoup

from config.log import logger
from common.utils import gen_fake_header

class IP2Domain(object):
    """
    help summary page

    Example:
        python ip2domain.py run 39.156.66.10
    
    Note:
        --ip    One IP (target must be provided)

    :param str  ip:     One IP (target must be provided)
    """
    def __init__(self):
        self.headers = gen_fake_header()
        self.url = "https://site.ip138.com/"

    def run(self, ip):
        logger.log('INFOR', "Searching for " + ip)
        resp = requests.get(self.url + ip, headers=self.headers)
        pattern = re.compile('<li><span class="date".*?</li>', re.S)
        content = re.findall(pattern, resp.text)
        for line in content:
            soup = BeautifulSoup(line, 'lxml')
            # soup = BeautifulSoup(line)
            url = soup.a.attrs['href']
            logger.log('INFOR', url.strip('/'))

if __name__ == '__main__':
    fire.Fire(IP2Domain)
    
