# from ChangeIP import ChangeIP

# a = ChangeIP()
# print(a.getCardInfo())
# card = a.selectCard()
# a.setCardInfo(card)

import socket

serverIP = '100.23.22.22'
port = 8888
client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
result = client.connect((serverIP, port))
print(result)