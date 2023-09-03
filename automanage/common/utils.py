import os
import sys
import json
import random
import requests
import tenacity
import platform
import subprocess
from tqdm import tqdm
from distutils.version import LooseVersion

# from config.log import logger
from loguru import logger
# from config import settings 


def init():
    """
    Initialize the environment
    """
    logger.log('INFOR', 'Initializing the environment')
    pass

def python_version():
    return sys.version

def check_dep():
    """
    Check dependent environment
    """
    logger.log('INFOR', 'Checking dependent environment')
    implementation = platform.python_implementation()
    version = platform.python_version()
    if implementation != 'CPython':
        logger.log('FATAL', f'AutoManage only passed the test under CPython')
        exit(1)
    if LooseVersion(version) < LooseVersion('3.10'):
        logger.log('FATAL', 'AutoManage requires Python 3.10 or higher')
        exit(1)

def gen_fake_header():
    """
    Generate fake request headers
    """
    headers = dict(settings.REQUEST_DEFAULT_HEADERS)
    if settings.ENABLE_RANDOM_UA:
        user_agents = list(settings.REQUEST_USER_AGENTS)
        ua = random.choice(user_agents)
        headers['User-Agent'] = ua
    headers['Accept-Encoding'] = 'gzip, deflate'
    return headers

def get_proxy():
    """
    Get random proxy
    """
    if settings.ENABLE_REQUEST_PROXY:
        try:
            return settings.REQUEST_PROXY_POOL.copy()
        except IndexError:
            return None
    return None

def get_net_env():
    logger.log('INFOR', 'Checking network environment')
    try:
        result = check_net()
    except Exception as e:
        logger.log('DEBUG', e.args)
        logger.log('ALERT', 'Please check your network environment.')
        return False
    return result

def set_request_conditions():
    header = gen_fake_header()
    proxy = get_proxy()
    timeout = settings.REQUEST_TIMEOUT_SECOND
    verify = settings.REQUEST_SSL_VERIFY
    session = requests.Session()
    session.trust_env = False
    return header, proxy, timeout, verify, session

def check_version(local):
    logger.log('INFOR', 'Checking for the latest version')
    api = 'https://api.github.com/repos/ClshNuer/AutoManage/releases/latest'
    header, proxy, timeout, verify, session = set_request_conditions()
    try:
        resp = session.get(url=api, headers=header, proxies=proxy,
                           timeout=timeout, verify=verify)
        resp_json = resp.json()
        latest = resp_json['tag_name']
    except Exception as e:
        logger.log('ALERT', 'An error occurred while checking the latest version')
        logger.log('DEBUG', e.args)
        return
    if latest > local:
        change = resp_json.get("body")
        logger.log('ALERT', f'The current version is {local} '
                            f'but the latest version is {latest}')
        logger.log('ALERT', f'The {latest} version mainly has the following changes')
        logger.log('ALERT', change)
    else:
        logger.log('INFOR', f'The current version {local} is already the latest version')

@tenacity.retry(stop=tenacity.stop_after_attempt(3),wait=tenacity.wait_fixed(2))
def check_net():
    times = 0
    while True:
        times += 1
        urls = ['https://www.baidu.com', 'https://www.bing.com',
                'https://www.cloudflare.com', 'https://www.akamai.com/',
                'https://www.fastly.com/', 'https://www.amazon.com/']
        url = random.choice(urls)
        logger.log('DEBUG', f'Trying to access {url}')
        header, proxy, timeout, verify, session = set_request_conditions()
        try:
            resp = session.get(url, headers=header, proxies=proxy,
                              timeout=timeout, verify=verify)
        except Exception as e:
            logger.log('ERROR', e.args)
            logger.log('ALERT', f'Unable to access Internet, retrying for the {times}th time')
        else:
            if resp.status_code == 200:
                logger.log('DEBUG', 'Access to Internet OK')
                return True
        if times >= 3:
            logger.log('ALERT', 'Access to Internet failed')
            return False


def win_download_app(app_name):
    """
    Download apps on Windows
    """
    url = settings.WIN_DOWNLOAD_URLS[app_name]
    package_name = url.split('/')[-1]
    if get_net_env():
        logger.info(f"Start downloading the {app_name} installation package from {url}")
        try:
            with requests.get(url, stream=True) as resp:
                resp.raise_for_status()
                total_size = int(resp.headers.get('content-length', 0))
                block_size = 1024
                progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
                path = settings.PKG_PATH
                file_name = os.path.join(path, package_name)
                with open(file_name, 'wb') as file:
                    for chunk in resp.iter_content(chunk_size=block_size):
                        if chunk:
                            file.write(chunk)
                            progress_bar.update(len(chunk))
                progress_bar.close()
                logger.info(f"{app_name} download completed")
                return True
        except Exception as e:
            logger.error(e.args)
            logger.error(f"{app_name} download failed")
            return False
    else:
        sys.exit(1)










