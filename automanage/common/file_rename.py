#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import os
import fire
from loguru import logger

class ReName(object):
    def __init__(self) -> None:
        pass

    def file_rename(self, folder_path, old_str, new_str):
        """
        批量修改具有相同字符串的文件名。

        Args:
            folder_path (str): 要操作的文件夹路径。
            old_string (str): 要被替换的旧字符串。
            new_string (str): 替换后的新字符串。
        """
        logger.info(f"Start to rename files in {folder_path}.")
        for entry in os.scandir(folder_path):
            if entry.is_file() and entry.name.startswith(old_str):
                new_filename = entry.name.replace(old_str, new_str)
                os.rename(os.path.join(folder_path, entry.name), os.path.join(folder_path, new_filename))
                logger.debug(f"Renamed {entry.name} to {new_filename}.")
        logger.info(f"Finish to rename files in {folder_path}.")

    def main(self):
        folder_path = "./word/" # "./your_folder_path/"  # 要操作的文件夹路径
        old_str = "202304" # "old_str"  # 要被替换的旧字符串
        new_str = "202205" # "new_str"  # 替换后的新字符串

        self.file_rename(folder_path, old_str, new_str)

if __name__ == '__main__':
    fire.Fire(ReName)