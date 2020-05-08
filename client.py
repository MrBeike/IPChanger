# -*-coding:utf-8-*-

import socket

class Client:
    def __init__(self):
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    
    def connect(self,serverIP,port):
        self.client.connect((serverIP, port))

    def communicate(self):
        # 向服务器发送数据
        self.client.send(data.encode('utf-8'))
        # 等待接收服务器返回的数据
        recv_data = self.client.recv(1024)
        print('服务器:', recv_data.decode('utf-8'))
        if recv_data == b'byebye':
            break
        
    def close(self):               
        self.client.close()