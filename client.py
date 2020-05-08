# -*-coding:utf-8-*-

import socket
import json,time

class Client:
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

    def connect(self,serverIP,port):
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.client.connect((serverIP, port))

    def getConfig(self):
        pc_info = {
            'name':self.pc_name,
            'ip':self.pc_info
        }
        pc_info_json = json.dumps(pc_info)
        while True:
            # 向服务器发送数据
            self.client.send(pc_info_json.encode('utf-8'))
            # 等待接收服务器返回的数据
            recv_data = self.client.recv(1024)
            recv_data_json = json.loads(recv_data.decode('utf-8'))
            if recv_data_json['status'] == 'success':
                self.config = recv_data_json['data']
                break
            time.sleep(3)

    def close(self):
        self.client.close()