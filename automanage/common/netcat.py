#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import sys
import socket
import getopt
import threading
import subprocess
import fire
from loguru import logger

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

class NetCat(object):
    """
    NetCat is a simple command line client/server for the file transfer protocol.

    Usage:
        # netcat [-l] [-c] [-u] [-d <destination>] [-p <port>] [-p <command>] [<file>]
        python netcat.py -t target_host -p port
    """
    def __init__(self):
        """
        Initializes the client/server.

        Args:
            target_host (str): The hostname or IP address of the target.
            port (int): The port number of the target.
            listen (bool): listen on [host]:[port] for incoming connections
            execute (str): file_to_run - excute to given file upon receiving a connection
            command (bool): initialize a command shell
            upload_destination (str): upon receiving connection upload a file and write to [destination]
        """
        pass

def usage():
    print("Usage: NetCat.py -t target_host -p port")
    print("-l --listen - ")
    print("-e --execute ")
    print("-c --command - ")
    print("-u --upload_destination - upon receiving connection upload a file and write to [destination]")
    print("\n\n")
    print("Client Examples:")
    print("./NetCat.py -t 202.100.1.224 -p 5555")
    print("./NetCat.py -t 202.100.1.224 -p 5555 -u \'upload_src.txt\'")
    print("./NetCat.py -t 202.100.1.224 -p 5555")
    print("Server Examples:")
    print("./NetCat.py -l -p 5555 -c")
    print("./NetCat.py -l -p 5555 -u \'upload_dst.txt\'")
    print("./NetCat.py -l -p 5555 -e \'cat /etc/passwd\'")
    sys.exit(0)

def main():
    global listen, port, execute, command, upload_destination, target

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "command", "upload_destination", "target"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-l", "--listen"):
            listen = True
        elif opt in ("-e", "--execute"):
            execute = arg
        elif opt in ("-c", "--commandshell"):
            command = True
        elif opt in ("-u", "--upload"):
            upload_destination = arg
        elif opt in ("-t", "--target"):
            target = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        else:
            assert False, "Unhandled Option"
    if not listen and len(target) and port > 0 and not upload_destination:
        buffer = input()
        client_sender(buffer)

    if not listen and len(target) and port > 0 and not upload_destination:
        upload_file(upload_destination)
        # print(upload_destination)
        # file_to_upload = open(upload_destination, 'rb')
        # file_to_upload_fragment = file_to_upload.read(1024)
        # while file_to_upload_fragment:
        #     client_sender(file_to_upload_fragment) # 发送数据分片
        #     file_to_upload_fragment = file_to_upload.read(1024) # 继续读取数据

    if listen:
        server_loop()

def upload_file(file): # 客户端上传文件
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target, port)) # 连接远端 socket
        file_to_upload = open(file, 'rb') # 读取本地文件
        file_to_upload_fragment = file_to_upload.read(1024) # 每次读取 1024 字节
        while file_to_upload_fragment:
            client.send(file_to_upload_fragment) # 发送数据分片
            file_to_upload_fragment = file_to_upload.read(1024) # 继续读取数据
    except Exception as e:
        print(e)
        print("[*] Exception! Upload file Exiting.")
        client.close()

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port)) # 连接远程 socket
        if len(buffer): # 传入buffer，发送到远端 socket
            client.send(buffer.encode())

        while True: # 接受客户端输入，发送输入数据，打印响应数据
            recv_len = 1
            response = ""
            while recv_len:
                data = client.recv(4096).decode()
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break
            print(response, end = " ")
            buffer = input("")
            buffer += "\n"
            client.send(buffer.encode())
    except Exception as e:
        print(e)
        print("[*] Exception! Exiting.")
        client.close()

def server_loop():
    global target

    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target = client_handler, args = (client_socket, ))
        client_thread.start()

def run_command(command): # 执行命令，且返回结果
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr = subprocess.STDOUT, shell = True)
    except Exception as e:
        # print(e)
        output = "Failed to execute command. \r\n"
    
    return output

def client_handler(client_socket):
    global upload, execute, command

    if len(upload_destination): # 上传文件
        file_buffer = b""

        while True:
            data = client_socket.recv(1024)
            print(data)
            if not data:
                break
            else:
                file_buffer += data
        try:
            file_descriptor = open(upload_destination, 'wb')
            file_descriptor.write(file_buffer)
            str_to_send = "Successfully saved file to %s\r\n" % upload_destination
            client_socket.send(str_to_send.encode())
        except Exception as e:
            # print(e)
            str_to_send = "Failed to save file to %s\r\n" % upload_destination
            client_socket.send(str_to_send.encode())

    if len(execute): # 执行命令就回显结果
        output = run_command(execute)
        client_socket.send(output)

    if command: # shell 交互
        while True:
            client_socket.send("<QYTANG:#> ".encode())
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024).decode()
                try:
                    response = run_command(cmd_buffer)
                    client_socket.send(response)
                except:
                    response = b"Failed to execute command. \n"
                    client_socket.send(response)

if __name__ == '__main__':
    main()
