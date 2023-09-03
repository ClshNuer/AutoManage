#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import sys
import time
from random import randint
import fire
from loguru import logger

import ipaddress
import multiprocessing
from scapy.all import *


class ScapyPing(object):
    """
    A class that represents a IP address

    Example:
        python deal_ipaddr_text.py
        # python deal_ipaddr_text.py main
        # python3 deal_ipaddr_text.py show_ips --ips_filepath /tmp/ips.txt
    """
    def __init__(self, host = None, hosts = None):
        self.host = host
        self.hosts = hosts

    def scapy_ping(self, host):
        packet = IP(dst = host, ttl = 2) / ICMP() / b'Welcome to qytang'
        ping = sr1(packet, timeout = 1, verbose = False)
        try:
            # logger.info(ping.getlayer(IP).fields['src'])
            # logger.info(ping.getlayer(ICMP).fields['type'])
            if ping.getlayer(IP).fields['src'] == host and ping.getlayer(ICMP).fields['type'] == 0:
                # 如果收到目的返回的ICMP ECHO-Replay 包
                return (host, 1) # 返回主机和结果，1 为通
            else:
                return (host, 2) # 回主机和结果，2 为不通
        except Exception:
            return (host, 3) # 出现异常也返回主机和结果，2 为不通

    def scan(self, ip):
        ip_id = randint(1,65535)
        icmp_id = randint(1,65535)
        icmp_seq = randint(1,65535)
        packet = IP(dst = ip, ttl = 64, id = ip_id)/ICMP(id = icmp_id, seq = icmp_seq)/b'rootkit'
        result = sr1(packet, timeout = 1, verbose = False)
        if result:
            scan_ip = result[IP].src
            print(scan_ip, 'is alive')
        else:
            print(ip, 'is down')

    def scapy_ping_scan(self, network):
        net = ipaddress.ip_network(network)
        ip_list = []

        for ip in net:
            ip_list.append(str(ip)) # 将IP 地址放入ip_list 清单

        pool = multiprocessing.Pool(processes = 100) # 创建多进程进程池（并发为100）
        result = pool.map(self.scapy_ping, ip_list) # 关联函数与参数，且提取结果到result
        pool.close() # 关闭pool，不再加入新进程
        pool.join() # 等待每一个进程结束
        scan_list = [] # 扫描结果IP 地址清单

        for ip, ok in result:
            if ok == 1: # 如果范围值为1
                scan_list.append(ip) # 将IP 加入scan_list 清单
            
        return(sort_ip(scan_list)) # 排序并打印清单
    
    def main(self):
        """
        主函数
        """
        # # 读取文件中的 IP 地址
        # ips = self.read_file('/tmp/ips.txt')
        # # 扫描 IP 地址
        # scan_ips = self.scapy_ping_scan(ips)
        # # 写入文件中
        # self.write_file('/tmp/scan_ips.txt', scan_ips)
        self.scapy_ping(self.host)

        # t1 = time.time()
        # logger.info('活动IP 地址如下：')
        # for ip in scapy_ping_scan(sys.argv[2]):
        #     logger.info(str(ip))
        
        # t2 = time.time()
        # # logger.info('本次扫描时间：%。2f' % (t2 - t1))

if __name__ == '__main__':
    fire.Fire(ScapyPing)

