#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import time
import socket
import ipaddress
import multiprocessing
import fire
from loguru import logger

import psutil
# import netifaces # 暂时无法安装
from scapy.all import *


class ScapyScan(object):
    """
    A class that represents a IP address

    Example:
        python scapy_scan.py ping 127.0.0.1
        python scapy_scan.py scapy_ping_scan 192.168.31.0/28
        # python scapy_scan.py main
        # python3 scapy_scan.py show_ips --ips_filepath /tmp/ips.txt
    """
    def __init__(self, host = None, hosts = None):
        self.host = host
        self.hosts = hosts

    def iface_ip_mac(self, iface = 'WLAN'):
        # iface = netifaces.gateways()['default'][netifaces.AF_INET][1]
        # ifaces = list(psutil.net_if_addrs().keys()) # ifaces = ['本地连接* 1', '本地连接* 10', 'WLAN', 'Loopback Pseudo-Interface 1']
        wlan_addrs = psutil.net_if_addrs()[iface]
        mac = wlan_addrs[0].address.replace('-', ':').lower()
        ipv4 = wlan_addrs[1].address
        return iface, ipv4, mac

    def ping(self, dst):
        """
        Ping a host
        """
        data = "I'm a ping packet" # 数据层
        pkt = IP(dst = dst, ttl = 64, id = RandShort()) / ICMP(id = RandShort(), seq = RandShort()) / data
        try:
            reply = sr1(pkt, timeout = 1, verbose = 0) # dst 是目标主机， reply[IP].src 是回复主机，不一定是一个 IP，中间可能有路由器
            # reply[ICMP].display() # 查看ICMP 包的类型
            # reply.haslayer 方法
            if reply[IP].src == dst and reply[ICMP].type == 0:
                logger.info(f"Ping success! {dst}")
                return dst, True # dst 通
            else:
                logger.info(f"Ping failed! {dst}")
                return dst, False # dst 不通
        except Exception:
            logger.error(f"Ping failed! {dst}")
            return dst, False # 异常 不通

    def ping_scan(self, network, maxPool = 4):
        net = ipaddress.ip_network(network)
        ip_list = [str(ip) for ip in net] # ip list

        with multiprocessing.Pool(maxPool if maxPool else multiprocessing.cpu_count()) as pool: # 多进程进程池
            results = pool.map(self.ping, ip_list) # 关联函数与参数，且提取结果到 result

        scan_list = list(filter(lambda x: x[1] == 1, results)) # 使用filter 函数过滤出ping 成功的 IP 地址
        scan_list = [ip[0] for ip in scan_list] # 提取IP 地址

        return sorted(scan_list)

    def arp(self, pdst):
        iface, psrc, hwsrc = self.iface_ip_mac() # iface, ip, mac
        logger.info(f"{iface}, {psrc}, {hwsrc}")
        # pkt = ARP(pdst = pdst, psrc = self.host)
        pkt = Ether(src = hwsrc, dst = 'FF:FF:FF:FF:FF:FF') / ARP(op =1, hwsrc = hwsrc, hwdst = '00:00:00:00:00:00', psrc = psrc, pdst = pdst)
        try:
            reply, unreply = srp(pkt, iface = iface, timeout = 1, verbose = 0)
            if reply[0][1].psrc == pdst:
                logger.info(f"ARP success! {pdst}, MAC {reply[0][1].hwsrc}")
                return reply[0][1].hwsrc, True
            else:
                logger.info(f"ARP failed! {pdst}")
                return None, False
        except Exception:
            logger.error(f"ARP failed! {pdst}")
            return None, False

    def arp_scan(self):
        pass

    def tcp(self, dst, lport = 0, hport = 65535):
        _, ping_result = self.ping(dst)
        if ping_result:
            dports = []
            pkg = IP(dst = dst) / TCP(dport = (lport, hport), flags = "S")
            try:
                replies = sr(pkg, timeout = 1, verbose = 0)[0].res
                for reply in replies:
                    if reply[1].haslayer(TCP) and reply[1][TCP].fields['flags'] == 18:
                        dports.append(reply[1][TCP].sport)
                        logger.info(f"端口号 {reply[1][TCP].sport} is open")
                return dports, True
            except Exception:
                logger.error(f"TCP failed! {dst}:{lport}:{hport}")
                return dports, False

    def tcp_scan(self):
        pass

    def main(self):
        """
        主函数
        """
        self.ping(self.host)

        # # 读取文件中的 IP 地址
        # hosts = self.read_file('/tmp/ips.txt')
        # t1 = time.time()
        # logger.info('活动IP 地址如下：')
        # alive_hosts = self.ping_scan(hosts):
        # logger.info(alive_hosts)
        # t2 = time.time()
        # # logger.info('本次扫描时间：%。2f' % (t2 - t1))
        # # 写入文件中
        # self.write_file('/tmp/scan_ips.txt', alive_hosts)

if __name__ == '__main__':
    fire.Fire(ScapyScan)

