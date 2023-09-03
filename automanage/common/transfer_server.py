#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import re
import json
import struct
import socketserver
import fire
from loguru import logger

class FileTransferServer(socketserver.BaseRequestHandler):
# class FileTransSerHandler(socketserver.BaseRequestHandler): # # FileTransferServerHandler
    """
    This is a File Transfer Server.

    Usage:
        python transfer_server.py main --port=3332

    Example:
        python transfer_server.py main --port=3332
    """
    def __init__(self, port):
    # def __init__(self, port, request, client_address, server):
        # super().__init__(request, client_address, server)
        self.port = port
        self.buffsize = 1024
    
    def handle(self):
        logger.info(f'Connected from {self.client_address}')
        while True:
            filename = input('Please input the filename you want to send: ').strip()
            if filename == 'exit':
                break
            head_info, head_info_len = self.open_file(filename)
            self.send_file(head_info, head_info_len, filename)
        self.request.close()

    def send_file(self, head_info, head_info_len, filename):
        try:
            self.request.send(head_info_len)
            self.request.send(head_info.encode('utf-8'))
            with open(filename, 'rb') as f:
                while True:
                    data = f.read(self.buffsize)
                    if not data:
                        break
                    self.request.sendall(data)
            logger.info('Send success!' + filename)
        except Exception as e:
            logger.error(f'Send {filename} fail ! -> {e}')

    def open_file(self, filename):
        filesize_bytes = os.path.getsize(filename)
        pattern = re.compile(r'([^<>/\\\|:""\*\?]+\.\w+$)')
        data = pattern.findall(filename)
        head_dir = {
            'filename': data,
            'filesize_bytes': filesize_bytes
        }
        head_info = json.dumps(head_dir)
        head_info_len = struct.pack('i', len(head_info))
        return head_info, head_info_len

    def main(self):
        logger.info(f'Starting to run File Transfer Server on port {self.port}...')
        logger.info(f'Listening at {self.port}')
        # server = socketserver.ThreadingTCPServer(('127.0.0.1', self.port), FileTransSerHandler)
        server = socketserver.ThreadingTCPServer(('127.0.0.1', self.port), FileTransferServer)
        server.serve_forever()

if __name__ == '__main__':
    fire.Fire(FileTransferServer)
