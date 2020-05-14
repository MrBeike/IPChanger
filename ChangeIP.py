# -*-coding:utf-8-*-
import wmi
import json,time,os,io,sys

class ChangeIP:
    def __init__(self):
        # wmi instance
        wmi_service = wmi.WMI()
        self.netcards = wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True)

    def getCardInfo(self):
        '''
        Get all cards'info on this computer.
        '''
        self.netcard_infos =[]
        for netcard in self.netcards:
            #see wmi_object in file Tips
            netcard_info = {
                'ip' : netcard.IPAddress[0],
                'name' : netcard.Description,
                'subnetmask':netcard.IPSubnet[0],
                'gateway':netcard.DefaultIPGateway[0],
                'dns': netcard.DNSServerSearchOrder[0]
            }
            self.netcard_infos.append(netcard_info)
        return self.netcard_infos

    def selectCard(self):
        '''
        Select which card to be modify.
        '''
        if self.netcard_infos.__len__ == 1:
            self.card = self.netcards[0]
            self.card_info = self.netcard_infos[0]
        else:
            for index,info in enumerate(self.netcard_infos):
                print(f"【{index + 1}】-->{info['name']} | {info['ip']}")
            self.select = int(input('请选择要修改的显卡【序号】 ').strip()) -1
            self.card = self.netcards[self.select]
            self.card_info = self.netcard_infos[self.select]
        return self.card,self.card_info

    def setCardInfo(self,setterInfo):
        '''
        Set the card using giving config info. 
        params: info: dict, config info {ip,subnetmask,gateway,dns}
        '''
        # 开始设置IP地址段信息
        # FIXME 设置的值必须是数组形式？
        setter_info = setterInfo
        ip = [setter_info['ip']]
        subnetmask = [setter_info['subnetmask']]
        gateway = [setter_info['gateway']]
        dns = [setter_info['dns']]
        # 设置成1，代表DNS非自动选择
        gateway_CostMetrics = [1]
        ip_result = self.card.EnableStatic(IPAddress=ip, SubnetMask=subnetmask)
        if ip_result[0] == 0:
            print("设置IP地址成功")
        elif ip_result[0] == 1:
            print("设置IP成功，需要重启计算机")
        else:
            print("设置IP地址失败，请联系网络管理员")
            return False
        # 开始设置网关地址段信息
        gateway_result = self.card.SetGateways(DefaultIPGateway=gateway, GatewayCostMetrics=gateway_CostMetrics)
        if gateway_result[0] == 0:
            print("设置网关地址成功")
        else:
            print("设置网关地址失败，请联系网络管理员")
            return False
        # 开始修改DNS地址段信息
        dns_result = self.card.SetDNSServerSeaarchOrder(SetDNSServerSeaarchOrder=dns)
        if dns_result[0] == 0:
            time.sleep(3)
            os.system('ipconfig /flushdns')
            print("设置DNS地址成功")
        else:
            print("设置DNS地址失败，请联系网络管理员")
            return False
            
        # TODO 记录所有结果？
        # def log(self):
        #     pass
        
    @staticmethod
    def configParse(filename):
    # [originIP,newIP,subnetmask,gateway,dns]
        config ={}
        with open(filename,encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                config_list = line.split(',')
                # 构造value dict
                _key = ['ip','subnetmask','gateway','dns']
                _value = config_list[1:]
                value = dict(zip(_key,_value))
                key = config_list[0]
                config[key] = value
        return config
    
    def getConfig(self,config):
        ip = self.card_info['ip']
        setter_info = config[ip]
        return setter_info

    @staticmethod
    # 通过json数据判定修改某个部分，修改值匹配
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

    def infoReMaker(self):
        ip = self.card_info['ip']
        subnetmask = self.card_info['subnetmask']
        gateway = self.card_info['gateway']
        dns = self.card_info['dns']

    def configVerify(self):
        wmi_service = wmi.WMI()
        netcards = wmi_service.Win32_NetworkAdapterConfiguration(IPEnabled=True)
        selected_card = netcards[self.select]
        ip = selected_card.netcard.IPAddress[0]
        subnetmask = selected_card.IPSubnet[0]
        gateway= selected_card.DefaultIPGateway[0]
        if (ip == self.card_info['ip']) and (subnetmask == self.card_info['subnetmask']) and (gateway == self.card_info['gateway']):
            return True
        else:
            self.setCardInfo(self.setter_info)
        

if __name__ == '__main__': 
    c = ChangeIP()
    c.getCardInfo()
    c.selectCard()
    config = c.configParse('ip_map.csv')
    setter_info = c.getConfig(config)
    c.setCardInfo(setter_info)