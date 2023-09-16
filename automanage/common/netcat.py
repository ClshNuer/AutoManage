#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import sys
import socket
import getopt
import threading
import subprocess
import fire
from loguru import logger

target = ""
port = 0
listen = False
command = False
upload = False
execute = ""
upload_destination = ""

class NetCatClient(object):
    def __init__(self) -> None:
        pass
        
    def send_command(target, port, byte = 4096): # 发送命令
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            try:
                client.connect((target, port)) # 连接远程 socket
                while True: # 接受客户端输入，发送输入数据，打印响应数据
                    buffer = input("") + "\n"
                    client.send(buffer.encode()) # 传入buffer，发送到远端 socket
                    response = bytearray(byte) # 可变字节缓冲区
                    recv_len = client.recv_into(response) # recv_into 方法直接写入缓冲区
                    # logger.info("Received: %s" % response[:recv_len]。decode())
                    print(response[:recv_len].decode(), end = " ", flush = True) # 打印响应数据，刷新输出缓冲区
            except Exception as e:
                logger.error(e)
                logger.info("Exception! Exiting.")
            finally:
                logger.info("Close connection.")

    def upload_file(target, port, file): # 上传文件
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            try:
                client.connect((target, port)) # 连接远端 socket
                client.send(file.encode() + b'\n') # 发送文件名
                with open(file, 'rb') as file_to_upload:
                    client.sendfile(file_to_upload) # 使用 sendfile 直接发送文件内容
                # file_to_upload = open(file, 'rb') # 读取本地文件
                # file_to_upload_fragment = file_to_upload.read(1024) # 每次读取 1024 字节
                # while file_to_upload_fragment:
                #     client.send(file_to_upload_fragment) # 发送数据分片
                #     file_to_upload_fragment = file_to_upload.read(1024) # 继续读取数据
            except Exception as e:
                logger.error(e)
                logger.info("Exception! Upload file Exiting.")
            finally:
                logger.info("Close connection.")


def server_loop(target):
    if not target:
        target = "0.0.0.0"

    addr_info = socket.getadrinfo(target, port, type = socket.SOCK_STREAM)
    with socket.socket(*addr_info[0][:3]) as server:
        server.bind(addr_info[0][4])
        server.listen(5)

        while True:
            with server.accept() as client_socket:
                client_thread = threading.Thread(target = client_handler, args = (client_socket, ), asemon = True)
                client_thread.start()

def download_file(client_socket): # upload
    if upload: # 上传文件
        file_buffer = b""
        while True:
            data = client_socket.recv(1024)
            # logger.info(data)
            print(data)
            if not data:
                break
            file_buffer += data
        try:
            with open(upload_destination, 'wb') as file_descriptor:
                file_descriptor.write(file_buffer)
            str_to_send = "Successfully saved file to %s\r\n" % upload_destination
        except Exception as e:
            # logger.error(e)
            print(e)
            str_to_send = "Failed to save file to %s\r\n" % upload_destination
        client_socket.send(str_to_send.encode())

def client_handler(client_socket): # execute, command
    download_file(client_socket)
    if len(execute): # 执行命令就回显结果
        run_command(client_socket, execute)
        
    if command: # shell 交互
        while True:
            client_socket.send("<sh:#> ".encode())
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024).decode()
                run_command(client_socket, cmd_buffer)

def run_command(client_socket, command): # 执行命令，且返回结果
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr = subprocess.STDOUT, shell = True)
    except Exception as e:
        # logger.error(e)
        print(e)
        output = "Failed to execute command. \r\n"
    client_socket.send(output)

def main():
    # if not listen and len(target) and port > 0 and not upload_destination:
    #     # send_command(buffer)
    #     send_command()
    
    # if not listen and len(target) and port > 0 and upload_destination:
    #     upload_file(upload_destination)
    #     # logger.info(upload_destination)
    #     # with open(upload_destination, 'rb') as file_to_upload:
    #     #     file_to_upload_fragment = file_to_upload.read(1024)
    #     #     while file_to_upload_fragment:
    #     #         send_command(file_to_upload_fragment) # 发送数据分片
    #     #         file_to_upload_fragment = file_to_upload.read(1024) # 继续读取数据

    # if listen:
    #     server_loop(target)
    pass

class NetCat(object):
    """
    NetCat is a simple command line client/server for the file transfer protocol.

    Usage:
        # netcat [-l] [-c] [-u] [-d <destination>] [-p <port>] [-p <command>] [<file>]
        python netcat.py -t target -p port
    Client Usage:
        python netcat.py -t 202.100.1.224 -p 5555
        python netcat.py -t 202.100.1.224 -p 5555 -u upload_src.txt
    Server Usage:
        python netcat.py -l -p 5555 -c
        python netcat.py -l -p 5555 -u upload_dst.txt
        python netcat.py -l -p 5555 -e 'cat /etc/passwd'
    """
    def __init__(self):
        """
        Initializes the client/server.

        Args:
            target (str): The hostname or IP address of the target.
            port (int): The port number of the target.
            listen (bool): listen on [host]:[port] for incoming connections
            execute (str): file_to_run - excute to given file upon receiving a connection
            command (bool): initialize a command shell
            upload_destination (str): upon receiving connection upload a file and write to [destination]
        """
        # self.port = port
        pass

    # client = NetCatClient()

if __name__ == '__main__':
    # main()
    fire.Fire(NetCatClient)
