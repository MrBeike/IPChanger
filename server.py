# -*-coding:utf-8-*-

import socket
import json

from functions import *

class Server:
    def __init__(self):
        pass

    def getComputerInfo(self):
        self.pc_name = self.client.gethostname()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            self.pc_ip = s.getsockname()[0]
        finally:
            s.close()

    def star(self):
        self.server = socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        address = (pc_ip, 9999)
        self.server.bind(address)
        # 使用socket创建的套接字默认的属性是主动的，使用listen将其变为被动的，这样就可以接收别人的链接了
        self.server.listen(50)  # 这个值主要决定了同一时刻有多少个客户端可以连接
        while True:
            # 创建接收
            # 如果有新的客户端来链接服务器，那么就产生一个新的套接字专门为这个客户端服务
            # client_socket用来为这个客户端服务，相当于的tcp_server套接字的代理
            # server_socket就可以省下来专门等待其他新客户端的链接
            # 这里clientAddr存放的就是连接服务器的客户端地址
            # client_socket, clientAddr
            client_info = self.server.accept()
            self.setConfig(client_info)

    def sendConfig(self, client_info):
        client_socket, clientAddr = client_socket
        recv_data = client_socket.recv(1024)
        recv_data_json = json.loads(recv_data)
        if recv_data_json['name']:
            storeData(recv_data_json)
            config = getConfig(recv_data_json['name'])
            client_socket.send(json.loads(config))
            client_socket.close()

    def close(self):
        self.server.close()
