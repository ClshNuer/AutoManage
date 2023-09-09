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

