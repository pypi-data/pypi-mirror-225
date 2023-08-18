from ..systemService import mqttService
from .scheduleService import ScheduleService
from .loader.hardwareInfoLoader import HardwareInfoLoader
from ..import config
from ..utils import TimeUtil




# 代理加载存储字典
proxyDict:dict = None

# 服务加载存储字典
serviceDict:dict = None

stateInfo:dict = None

# mqtt客户端
pervasiveMqttClient:mqttService.MqttService = None


# 定时器
taskServer:ScheduleService = None

# 硬件信息加载器
hardwareInfoLoader:HardwareInfoLoader = None


def getServiceListInfo():
    services = []
    for key in serviceDict.keys():
        serviceItem= serviceDict[key].__dict__
        serviceItem =  {
            'versionCode': serviceItem['versionCode'],
            'id': serviceItem['url'],
            'serviceId': serviceItem['url']
        }
        services.append(serviceItem)
    return services

def getSystemInfo():
    formatted_time = TimeUtil.getNowFormatDatetime()
    resDict = {
        "deviceId":config.DEVICE_ID,
        "dateTime":formatted_time,
        "stateInfo":stateInfo,
        "hardwareInfo":hardwareInfoLoader.getHardwareInfo()
    }
    return resDict

