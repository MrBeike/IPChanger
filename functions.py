import json

def writeConfig(filename='config.txt'):
    pass

def readConfig(username,department,filename='config.txt'):
    with open(filename,encoding='utf-8') as f:
        content = f.readlines()
    for item in content:
        config_list = item.splite(',')
        if (username == config_list[0]) and (department == config_list[1]):
            # 去除config_list中的username和department
            return config_list[2:]
        else:
            continue

def getConfig(name):
    username = name[4:-3]
    department = name[-3:]
    ip,subnetmask,gateway,dns = readConfig(username,department)
    config = {
        'ip': ip,
        'subnetmask': subnetmask,
        'gateway':gateway,
        'dns': dns
    }
    return config


def storeData(json):
    pass
