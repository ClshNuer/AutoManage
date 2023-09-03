#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import os
import shutil
import subprocess
import fire
from loguru import logger

# 可配置的变量
NOTION_URL = "https://github.com/Reamd7/notion-zh_CN/releases/latest/download/notion-zh_CN.js"
JS_FILE = "notion-zh_CN.js"
JS_SRC = os.path.join(".", JS_FILE)

INS_DIR = "D:\\Softwares\\scoop\\apps\\notion"
RENDERER_DIR = os.path.join("current", "resources", "app", "renderer")
JS_DST = os.path.join(INS_DIR, RENDERER_DIR, JS_FILE)

PRELOAD_DIR = os.path.join("current", "resources", "app", "renderer", "preload.js")
PRELOAD_DST = os.path.join(INS_DIR, PRELOAD_DIR)

CODE_TO_ADD = """
//# sourceMappingURL=preload.js.map
require("./notion-zh_CN") // 添加该行
"""


class Notion(object):
    """
    A class that represents a notion
    """
    def __init__(self):
        pass

    def copy_js_file(self):
        """
        复制JS文件到Notion目录
        """
        if not os.path.exists(JS_DST):
            logger.error(f"{JS_DST} does not exist.")
            if os.path.exists(JS_SRC):
                logger.info(f"{JS_FILE} exists.")
            logger.info("Start to copy {JS_FILE} to Notion directory.")
            shutil.copy(JS_SRC, JS_DST)
            logger.info(f"Copy {JS_FILE} to Notion directory successfully.")

    def add_code_to_preload(self):
        """
        在preload.js中添加代码
        """
        with open(PRELOAD_DST, "r+", encoding = "utf-8") as f:
            content = f.read()
            if CODE_TO_ADD not in content:
                logger.info("Start to backup preload.js.")
                shutil.copy(PRELOAD_DST, PRELOAD_DST + ".bak") # 备份preload.js
                logger.info("Backup preload.js successfully.")
                logger.info("Start to add code to preload.js.")
                f.write(CODE_TO_ADD) # 添加代码
                logger.info("Add code to preload.js successfully.")            
            else:
                logger.info("Code already exists in preload.js.")

    def run(self):
        CMD = f"Invoke-WebRequest -Uri {NOTION_URL} -OutFile {PRELOAD_DIR}"
        subprocess.run(CMD, shell = True)
        CMD = f"Add-Content f{PRELOAD_DIR} 'require(\"./notion-zh_CN\")'"
        subprocess.run(CMD, shell = True)

    def main(self):
        try:
            self.copy_js_file()
            self.add_code_to_preload()
            logger.info("All done.")
        except Exception as e:
            logger.error(f"Error occurred: {e}")
        # self.run()

if __name__ == "__main__":
    fire.Fire(Notion)