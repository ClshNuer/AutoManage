#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import hashlib
import fire
from loguru import logger

class Dec2Hash(object):
    """
    十进制转 MD5
    """
    def __init__(self, data):
        pass

    def dec2hash(dict_file, md5_file):
        with open(md5_file, 'w') as md5_data, open(dict_file).readlines() as passwords:
            for password in passwords:
                # hash = hashlib.md5()
                # hash.update(password.strip().encode('utf-8'))
                hash = hashlib.md5(password.strip().encode('utf-8'))
                print(password.strip())
                print(hash.hexdigest())
                md5_data.write(hash.hexdigest() + '\n')


if __name__ == '__main__':
    fire.Fire(Dec2Hash)
