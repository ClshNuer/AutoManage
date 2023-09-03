#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Author       : Kaw0n
@Email        : syajask@gmail.com
@Github       : https://github.com/ClshNuer/
@Ide          : vscode
@File         : inspys.py
@Project      : G:/common/inspys
@Version      : 1.0.0
@Description  :
@Time         : 2023/06/19 05:16
"""

import os
import re
import sys
import socket
import subprocess
from pathlib import Path

import requests
from tqdm import tqdm
from loguru import logger
# from config.log import logger
# from config import settings
# from common.utils import check_net
from utils import check_net

# python-3.10.11-amd64.exe download url from https://www.python.org/downloads/release/python-31011/
PKG_URL = "https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe"  # 默认下载链接
PY_PKG_PATTERN = re.compile(r"python-\d+\.\d+\.\d+-amd64\.exe")  # 匹配 Python 安装包的正则表达式
PY_PATH = Path("D:/Softwares/Python/Python310")  # 默认安装目录
PY_CACHE_DIR = PY_PATH.parent.joinpath("pip_cache") # 默认缓存目录 "D:/Softwares/Python/Python310/pip_cache"


# 选择最新的 Python 安装包
def choose_latest_py_pkg(py_pkgs):
    py_pkgs.sort(key=lambda x: x.split("-")[1], reverse=True)
    return py_pkgs[0]


# 匹配当前目录下是否有 Python 安装包
def match_py_pkg():
    py_pkgs = [pkg for pkg in os.listdir(".") if re.match(PY_PKG_PATTERN, pkg)]
    if len(py_pkgs) == 0:
        logger.info("No Python installation package found in the current directory")
        result = check_net()
        if result:
            logger.info("Network connection is normal")
            download_py_pkg()
            py_pkg_name = match_py_pkg()
            return py_pkg_name
        else:
            logger.info("Network connection is abnormal")
            logger.info("Please download the Python installation package manually")
            sys.exit(0)
    logger.info(f"Python installation package found in the current directory: {py_pkgs}")
    py_pkg_name = choose_latest_py_pkg(py_pkgs)
    logger.info(f"Choose the latest Python installation package: {py_pkg_name}")
    return py_pkg_name


# 下载 Python 安装包
def download_py_pkg(url=PKG_URL):
    logger.info("Downloading Python installation package...")
    filename = url.split("/")[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get("content-length", 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size, unit="iB", unit_scale=True)
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    progress_bar.update(len(chunk))
    logger.info("Python installation package download completed")


# 安装 Python
def install_py_pkg(pkg_name, PY_PATH=PY_PATH):
    logger.info("Installing Python...")
    # 默认安装位置 PY_PATH
    logger.info(f"Default installation location: {PY_PATH}")
    cmd = f'{pkg_name} /quiet InstallAllUsers=1 PrependPath=1 TargetDir={PY_PATH}'
    with tqdm(total=100, desc="Installing package", unit="%", leave=False) as pbar:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        pbar.update(100)
    logger.info("Python installation completed")


# 设置源与缓存存储目录
def set_pip_config():
    logger.info("Setting pip config...")
    cmd = f"python -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/"
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    cmd = f"python -m pip config set global.trusted-host mirrors.aliyun.com"
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    cmd = f"python -m pip config set global.cache-dir {PY_CACHE_DIR}"
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    logger.info("pip config set completed")


# 更新 pip，安装 pipenv
def update_pip_install_pipenv():
    logger.info("Updating pip...")
    cmd = f"python -m pip install --upgrade pip"
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    logger.info("pip update completed")
    logger.info("Installing pipenv...")
    cmd = f"python -m pip install pipenv"
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    logger.info("pipenv installation completed")

# Main
if __name__ == "__main__":
    current_path = Path(__file__).parent.absolute()
    logger.info(f"current_path: {current_path}")
    py_pkg_name = match_py_pkg()
    install_py_pkg(py_pkg_name, PY_PATH)
    set_pip_config()
    update_pip_install_pipenv()

    # cmd 框 pause
    subprocess.run(["pause"])