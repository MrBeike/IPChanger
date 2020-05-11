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
            #tuple
            netcard_info = {
                'ip' : netcard.IPAddress[0],
                'name' : netcard.Description
            }
            self.netcard_infos.append(netcard_info)
        return self.netcard_infos

    def selectCard(self):
        '''
        Select which card to be modify.
        '''
        if self.netcard_infos.__len__ == 1:
            self.card = self.netcards[0]
        else:
            for index,info in enumerate(self.netcard_infos):
                print(f"【{index + 1}】-->{info['name']} | {info['ip']}")
            select = int(input('请选择要修改的显卡【序号】 ').strip()) -1
            self.card = self.netcards[select]
        return self.card

    def setCardInfo(self,info):
        '''
        Set the card using giving config info. 
        params: info: str[json.dumps], config info {ip,subnetmask,gateway,dns}
        '''
        setter_info = json.loads(info)
        # 开始设置IP地址段信息
        # FIXME 设置的值必须是数组形式？
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
    def getConfig(filename):
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


if __name__ == '__main__': 
    c = ChangeIP()
    c.getCardInfo()
    # wmi_object is not subscripabl
    ip = c.selectCard()['ip']
    dict = c.getConfig('config')
    info = json.dumps(dict)
    the_info = info[ip]
    c.setCardInfo(the_info)
