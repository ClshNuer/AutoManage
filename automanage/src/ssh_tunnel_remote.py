#!/usr/bin/env python3
# -*- coding-utf-8 -*-

# 待优化

import fire
from loguru import logger

from sshtunnel import SSHTunnelForwarder

class SSHTunnelRemote(object):
    def __init__(self, ssh_username = 'root', ssh_passwd = 'root',
            ssh_tunnel_ip = '172.16.1.22', ssh_tunnel_port = 22, # 内网，目标服务端
            local_bind_address = '202.100.1.224',local_bind_port = 8080, # 中间人，边界目标服务端
            remote_bind_address = '127.0.0.1', remote_bind_port = 80 # 内网，目标转换服务端
        ):
        self.ssh_username = ssh_username
        self.ssh_passwd = ssh_passwd
        self.ssh_tunnel_ip = ssh_tunnel_ip
        self.ssh_tunnel_port = ssh_tunnel_port
        self.local_bind_ip = local_bind_address
        self.local_bind_port = local_bind_port
        self.remote_bind_ip = remote_bind_address
        self.remote_bind_port = remote_bind_port

    def ssh_tunnel_local_server(self, ssh_username = 'root', ssh_passwd = 'root',
            ssh_tunnel_ip = '172.16.1.22', ssh_tunnel_port = 22, # 内网，目标服务端
            local_bind_address = '202.100.1.224',local_bind_port = 8080, # 中间人，边界目标服务端
            remote_bind_address = '127.0.0.1', remote_bind_port = 80 # 内网，目标转换服务端
        ):
        server = SSHTunnelForwarder(
            (ssh_tunnel_ip, ssh_tunnel_port), # Setp 2 连接远端服务器SSH 端口
            ssh_username = ssh_username,
            ssh_password = ssh_passwd,
            local_bind_address = (local_bind_address, local_bind_port), # Setp 1 连接本地地址
            remote_bind_address = (remote_bind_address, remote_bind_port) # Step 3 跳转到远端服务器
        )

        server.start()

        print(server.local_bind_port) # 若不匹配local_bind_address，随机绑定本地端口

        # server.stop()
    
    def main(self):
        self.ssh_tunnel_local_server()
        self.ssh_tunnel_local_server(remote_bind_address = '172.16.1.21')

if __name__ == '__main__':
    fire.Fire(SSHTunnelRemote)

'''
from sshtunnel import SSHTunnelForwarder

server = SSHTunnelForwarder(
    ('172.16.1.22', 22), # Setp 2 连接远端服务器SSH 端口
    ssh_username = "root",
    ssh_password = "Cisc0123",
    local_bind_address = ('202.100.1.224', 8080), # Setp 1 连接本地地址
    remote_bind_address = ('127.0.0.1', 80) # Step 3 跳转到远端服务器
)

server.start()

print(server.local_bind_port) # 若不匹配local_bind_address，随机绑定本地端口

# server.stop()

'''