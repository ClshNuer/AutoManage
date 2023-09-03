#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import os
import time
import datetime
import fire
from loguru import logger

class IPAddress(object):
    """
    A class that represents a IP address

    Example:
        python deal_ipaddr_text.py
        # python deal_ipaddr_text.py main
        # python3 deal_ipaddr_text.py show_ips --ips_filepath /tmp/ips.txt
    """
    def __init__(self):
        pass

    def is_file_exists(self, filename):
        """
        判断文件是否存在
        """
        if not os.path.exists(filename):
            logger.warning(f"{filename} 文件不存在：")
            return False
        return True

    def read_file(self, filename):
        """
        读取文件中的 IP 地址
        """
        if not self.is_file_exists(filename):
            return 
        try:
            with open(filename, 'r') as f:
                ips = [line.strip() for line in f]
        except Exception as e:
            logger.error(f"发生错误：{e}")
        return ips

    def write_file(self, filename, ips):
        """
        将 IP 地址写入文件
        """
        try:
            with open(filename, 'w') as f:
                for ip in ips:
                    f.write(ip + "\n")
        except Exception as e:
            logger.error("发生错误：", e)

    def create_backup_file(self, filename):
        """
        备份文件
        """
        if not self.is_file_exists(filename):
            return
        file_abspath = os.path.abspath(filename)
        file_path, file_name = os.path.split(file_abspath)
        logger.info(f"开始备份文件：{filename}")
        timestamp = time.strftime("%Y%m%d%H")
        backup_filename = os.path.join(file_path, f"{timestamp}_{file_name}")
        self.write_file(backup_filename, self.read_file(filename))
        logger.info(f"备份文件成功：{filename} -> {backup_filename}")
        return backup_filename

    def deduplication(self, filename):
        """
        去重文件中的 IP 地址
        """
        if not self.is_file_exists(filename):
            return
        backup_filename = self.create_backup_file(filename)
        logger.info(f"开始去重文件：{filename}")
        ips = set(self.read_file(filename))
        self.write_file(filename, ips)
        logger.info(f"文件去重成功：{filename}")
        return ips, backup_filename

    def rename_files(self, root_dir):
        """
        重命名文件
        :param root_dir: 根目录
        """
        for directory, subdir_list, file_names in os.walk(root_dir):
            for file_name in file_names:
                source_name = os.path.join(directory, file_name)
                timestamp = os.path.getmtime(source_name)
                modified_date = str(datetime.datetime.fromtimestamp(timestamp)).replace(':', '.')
                target_name = os.path.join(directory, f'{modified_date}_{file_name}')
                logger.info(f'Renaming: {source_name} to: {target_name}')
                os.rename(source_name, target_name)
                
    def compare_ips(self, ips1, ips2):
        """
        比较两个 IP 地址集合
        """
        common_ips = ips1.intersection(ips2)
        unique_ips1 = ips1.difference(ips2)
        unique_ips2 = ips2.difference(ips1)
        return common_ips, unique_ips1, unique_ips2

    def show_ips(self, ips_filepath):
        """
        显示文件中的 IP 地址
        """
        ips, backup_file = self.deduplication(ips_filepath)
        logger.info(f"{ips_filepath} 文件中去重后的IP地址：{ips}")

    def show_compare_result(self, file, ips):
        """
        显示比较结果
        """
        if ips:
            logger.info(f"{file} 文件中独有的 IP 地址：{ips}")
        else:
            logger.info(f"{file} 文件中没有独有的 IP 地址！")

    def show_compare_results(self, ips1_filepath, ips2_filepath):
        """
        显示比较结果
        """
        ips1, _ = self.deduplication(ips1_filepath)
        ips2, _ = self.deduplication(ips2_filepath)
        common_ips, unique_ips1, unique_ips2 = self.compare_ips(ips1, ips2)
        if common_ips:
            logger.info(f"共同的 IP 地址：{common_ips}")
        else:
            logger.info("没有共同的 IP 地址！")
        self.show_compare_result(ips1_filepath, unique_ips1)
        self.show_compare_result(ips2_filepath, unique_ips2)

    def main(self):
        """
        主函数
        """
        ips1_filepath = "..\\data\\ip1.txt"
        ips2_filepath = "..\\data\\ip2.txt"
        # show_ips(ips1_filepath)
        # show_ips(ips2_filepath)
        self.show_compare_results(ips1_filepath, ips2_filepath)

if __name__ == "__main__":
    fire.Fire(IPAddress)
    