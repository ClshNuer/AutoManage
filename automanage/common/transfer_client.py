#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import json
import struct
from socket import *

import fire
from loguru import logger

class FileTransferClient(object):
    """
    This is a File Transfer Client.

    Usage:
        python transfer_client.py main --ip=

        python fileClient.py -u 127.0.0.1 -p 3332
    """
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def recv_file(self, head_dir, tcp_client):
        filename = head_dir['filename']
        file_size = head_dir['file_size']
        logger.info(f'Filename: {filename[0]}, Filesize: {file_size[0]}')
        recv_len = 0
        with open(filename[0], 'wb') as f:
            while recv_len < file_size:
                recv_mesg = tcp_client.recv(1024)
                recv_len += len(recv_mesg)
                f.write(recv_mesg)
        logger.info(f'File transfer completed!')

    def main(self):
        tcp_client = socket(AF_INET, SOCK_STREAM)
        tcp_client.connect((self.ip, self.port))
        logger.info('Waiting for server response data...')
        struct_len = tcp_client.recv(4)
        struct_info_len = struct.unpack('i', struct_len)[0]
        logger.info(f'Received header information length: {struct_info_len}')
        
        head_info = tcp_client.recv(struct_info_len)
        head_dir = json.loads(head_info.decode('utf-8'))
        self.recv_file(head_dir, tcp_client)

if __name__ == '__main__':
    fire.Fire(FileTransferClient)
