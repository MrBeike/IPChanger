# -*-coding:utf-8-*-

import socket

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
        self.server = socket(AF_INET,SOCK_STREAM)
        address = (pc_ip, 9999)
        self.server.bind(address)
        # 使用socket创建的套接字默认的属性是主动的，使用listen将其变为被动的，这样就可以接收别人的链接了
        self.server.listen(50)  #这个值主要决定了同一时刻有多少个客户端可以连接
        # 创建接收
        # 如果有新的客户端来链接服务器，那么就产生一个新的套接字专门为这个客户端服务
        # client_socket用来为这个客户端服务，相当于的tcp_server套接字的代理
        # tcp_server_socket就可以省下来专门等待其他新客户端的链接
        # 这里clientAddr存放的就是连接服务器的客户端地址
        client_socket, clientAddr = self.server.accept()
        #接收对方发送过来的数据
        recv_msg = client_socket.recv(1024)
        #发送数据给客户端
        send_data = client_socket.send("这是给您的回复".encode("gbk"))
        
        #7.关闭套接字
        #关闭为这个客户端服务的套接字，只要关闭了，就意味着为不能再为这个客户端服务了，如果还需要服务，只能再次重新连
        client_socket.close()
    
    def setConfig(self):
        pass

    def close(self):
        self.server.close()