#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import fire
from loguru import logger

import crypt


class Shadow(object):
    """
    A class that represents a IP address

    Example:
        python deal_ipaddr_text.py
    """
    def __init__(self, host = None, hosts = None):
        self.host = host
        self.hosts = hosts

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
        读取文件中的 password
        """
        if not self.is_file_exists(filename):
            return 
        try:
            with open(filename, 'r') as f:
                passwds = [line.strip() for line in f]
        except Exception as e:
            logger.error(f"发生错误：{e}")
        return passwds

def get_linelist(file):
    "将文件读取为行列表"
    with open(file,"r") as f:
        datalist = f.readlines()
        return datalist

def get_userinfo(datalist):
    "获得shadow文件的密码列表"
    userlist = []
    for user in datalist:
        linelist = user.split(":")
        saltpass = linelist[1] # 得到带盐的密码元素
        if len(saltpass)>3:
            userlist.append(user) # 把所有带密码的用户行加入列表
    return userlist

def pass_crypt(userlist,passdic_list):
    "传入有效用户列表和密码字典列表，爆破"
    for user in userlist:
        username = user.split(":")[0] # 取出用户名
        passwd = user.split(":")[1] # 取出带盐密码元素
        print('-----',passwd)
        salt = "$6$"+passwd.split("$")[2] # 取出盐值
        print(crypt.crypt('123456',salt))
        for clearPasswd in passdic_list:
            #print(type(str(clearPasswd.split())),"---")
            clearPasswd = clearPasswd.split()[0]
            #print(clearPasswd)
            encodePasswd = crypt.crypt(clearPasswd,salt)
            #print(encodePasswd)
            if encodePasswd == passwd:
                print("用户： %s,密码是： %s"%(username,clearPasswd))
                break

def main():
    passwordfile = ".\\shadow.txt"
    passworddicfile = ".\\passdic.txt"

    datalist = get_linelist(passwordfile)
    passdic_list = get_linelist(passworddicfile)
    userlist = get_userinfo(datalist)

    pass_crypt(userlist,passdic_list)

if __name__ == '__main__':
    fire.Fire(Shadow)
