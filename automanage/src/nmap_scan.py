#!/usr/bin/env python3
# -*- coding-utf-8 -*-
# docs : https://pypi.org/project/python-nmap/

import fire
from loguru import logger

import nmap


class NmapScan(object):
    """
    A class that represents a nmap scan

    Example:
        # python3 nmap_scan.py
        python nmap_scan.py main --hosts=192.168.31.0/24
        python nmap_scan.py main --hosts=192.168.31.1-124
        # python3 nmap_scan.py scan_alive_hosts --host
        # python3 nmap_scan.py scan_entire_hosts --hosts
    """
    def __init__(self, host = '127.0.0.1', hosts = '127.0.0.1'):
        self.host = host
        self.hosts = hosts
        self.port_scanner = nmap.PortScanner()

    def config_params(self, host, hosts):
        self.host = host
        self.hosts = hosts
        # self.port_scanner = port_scanner

    def nmap_scan_alive_hosts(self, arguments = '-v -n -sn'):
        """
        使用 nmap 进行 ping 扫描，返回存活主机列表
        :param arguments: 扫描参数
        :return: 存活主机列表
        """
        try:
            # arguments = '-sn -PE'
            scan_results = self.port_scanner.scan(hosts = self.hosts, arguments = arguments)
            # state = scan_results['scan'][self.hosts]['status']['state']
        except nmap.nmap.PortScannerError as e:
            logger.error(f'扫描失败：{e}')
            return []
        host_list = []
        for result in scan_results['scan'].values():
            if result['status']['state'] == 'up':
                host_list.append(result['addresses']['ipv4'])
        return host_list

    def nmap_entire_scan_hosts(self, arguments = '-v -n -A'):
        """
        使用 nmap 进行完全扫描，返回扫描结果
        :param arguments: 扫描参数
        :return: 扫描结果
        """
        logger.info(f'开始扫描主机：{self.hosts}')
        hosts = self.nmap_scan_alive_hosts()
        if not hosts:
            logger.info('扫描完成，无存活主机')
            return {}
        scan_results = {}
        for host in hosts:
            result = {'os': [], 'ports': {}}
            try:
                logger.info(f'开始扫描主机：{host}')
                scan_result = self.port_scanner.scan(hosts = host, arguments = arguments)
                scan_result = scan_result['scan'][host]
            except nmap.nmap.PortScannerError as e:
                logger.error(f'扫描失败：{e}')
                continue
            finally:
                logger.info(f'扫描主机：{host} 完成')
            # 操作系统猜测
            for os in scan_result.get('osmatch', []):
                result['os'].append({'name': os['name'], 'accuracy': os['accuracy']})
            # 服务端口扫描
            protos = ['tcp', 'udp']
            for proto in protos:
                if proto not in scan_result.keys():
                    continue
                for port in scan_result[proto].keys():
                    port_list = [proto]
                    port_list.append(list(scan_result[proto][port].values()))
                    result['ports'][port] = port_list
            scan_results[host] = result
        return scan_results
        
    def show_nmap_entire_scan_hosts(self):
        host_scan_results = self.nmap_entire_scan_hosts()
        if not host_scan_results:
            logger.info('请检测网络连接情况，然后重新扫描')
            return
        
        for host, scan_result in host_scan_results.items():
            logger.info(f'Nmap scan report for {host}')
            logger.info(f'操作系统猜测结果为：')
            if scan_result['os']:
                for os in scan_result['os']:
                    logger.info(f'操作系统可能为 {os["name"]}，可能性为 {os["accuracy"]} %')
            else:
                logger.info('未能猜测出操作系统，请重新检测或使用 Nmap 自行扫描')
            logger.info(f'服务端口扫描结果为：')
            if scan_result['ports']:
                for port, port_info in scan_result['ports'].items():
                    logger.info(f'{port} {port_info}')
            else:
                logger.info('未能扫描到服务端口，请重新检测或使用 Nmap 自行扫描')

    def show_nmap_scan_alive_hosts(self, arguments='-v -n -sn'):
        """
        显示存活主机列表
        :param arguments: 扫描参数
        """
        logger.info(f'开始扫描主机：{self.hosts}')
        hosts = self.nmap_scan_alive_hosts(arguments)
        if not hosts:
            logger.info('扫描完成，无存活主机')
            return
        for host in hosts:
            logger.info( '%-20s %5s' % (host, 'is UP'))
        logger.info('扫描完成，存活主机数量：%d' % len(hosts))
    
    def main(self):
        host = '127.0.0.1'
        hosts = '127.0.0.1'
        # # self.config_params(host, hosts)
        self.show_nmap_scan_alive_hosts()
        self.show_nmap_entire_scan_hosts()

if __name__ == '__main__':
    fire.Fire(NmapScan)
