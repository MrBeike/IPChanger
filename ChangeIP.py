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

    def selectCard(self):
        '''
        Select which card to be modify.
        '''
        if self.netcard_infos.__len__ == 1:
            card = self.netcards[0]
        else:
            for index,info in enumerate(self.netcard_infos):
                print(f"【{index + 1}】-->{info['name']}:{info['ip']}")
            select = int(input('请选择要修改的显卡【序号】 ').strip()) -1
            card = self.netcards[select]
        return card

    def setCardInfo(self,card,json):
        '''
        Set the card using giving config info. 
        params: card: wmi_object, the card to be modify.
        params: json: str, config info {ip,subnetmask,gateway,dns}
        '''
        setter_info = json.loads(json)
        # 开始设置IP地址段信息
        # FIXME 设置的值必须是数组形式？
        ip = [setter_info['ip']]
        subnetmask = [setter_info['subnetmask']]
        gateway = [setter_info['gateway']]
        dns = [setter_info['dns']]
        # 设置成1，代表DNS非自动选择
        gateway_CostMetrics = [1]
        ip_result = card.EnableStatic(IPAddress=ip, SubnetMask=subnetmask)
        if ip_result[0] == 0:
            print("设置IP地址成功")
        elif ip_result[0] == 1:
            print("设置IP成功，需要重启计算机")
        else:
            print("设置IP地址失败，请联系网络管理员")
            return False
        # 开始设置网关地址段信息
        gateway_result = card.SetGateways(DefaultIPGateway=gateway, GatewayCostMetrics=gateway_CostMetrics)
        if gateway_result[0] == 0:
            print("设置网关地址成功")
        else:
            print("设置网关地址失败，请联系网络管理员")
            return False
        # 开始修改DNS地址段信息
        dns_result = card.SetDNSServerSeaarchOrder(SetDNSServerSeaarchOrder=dns)
        if dns_result[0] == 0:
            time.sleep(3)
            os.system('ipconfig /flushdns')
            print("设置DNS地址成功")
        else:
            print("设置DNS地址失败，请联系网络管理员")
            return False
            
        # TODO 记录所有结果？
        def log(self):
            pass