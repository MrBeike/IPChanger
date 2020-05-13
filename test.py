# from ChangeIP import ChangeIP

# a = ChangeIP()
# print(a.getCardInfo())
# card = a.selectCard()
# print(card)

# import socket

# serverIP = '100.23.22.22'
# port = 8888
# client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# result = client.connect((serverIP, port))
# print(result)

def addressSub(originAddress,positon,value):
    '''
    params: originAddress: str, the string of address value.
    params: positon: int ,the positon of value to change.
    params: value: int ,the target value.
    '''
    address_list = originAddress.split('.')
    address_list[positon-1] = str(value)
    print(address_list)
    target_address = '.'.join(address_list)
    return target_address

k= '192.168.2.1'

target = addressSub(k,3,1)
print(target)