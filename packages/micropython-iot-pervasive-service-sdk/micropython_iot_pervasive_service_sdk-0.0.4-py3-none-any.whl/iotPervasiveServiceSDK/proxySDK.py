from machine import Timer
from .systemService.mqttService import MqttService
from .core import applicationContext
from .core.loader.proxyLoader import ProxyLoader
from .core.loader.serversLoader import ServiceLoader
from .utils import pathUtils
from .core.scheduleService import ScheduleService
from .core.job.mqttCheckMessageJob import MqttCheckMessageJob
from .core.job.mqttHealthJob import MqttHealthJob
from .core.job.contextUpLoadJob import ContextUploadJob
from .core.job.eventListenerJob import EventListenerJob
from . import config
from .utils import TimeUtil
from .core.loader import thingProxyFuncLoader
from .systemService import updateService
import  ujson
from .core.eventInvoker import EventInvoker
from .core.loader.hardwareInfoLoader import HardwareInfoLoader
from .core.sender.hardwareUpLoadSender import HardwareUpLoadSender

class ProxySDK:
  # 泛在web服务
  webServer = None

  # 泛在mqtt服务
  mqttClient = None


  """
  * 全部功能初始化
  * deviceId   泛在平台设备id
  * timer      需要使用的定时器
  * setThingModel 物模型读写函数
  * wlan 网络对象 micropython连接网络和存储网络信息的对象
  * deviceTypeId 所属设备类型的id
  * proxyPath 代理所在路径（用户自定义代理）（默认proxy文件夹）
  * servicePath 服务存储到哪个位置（默认"/service"）
  * BASE_PATH 程序基本路径（默认为根目录）
  * SDK_PATH SDK所在路径（默认upip下载路径）
  * openHttp 是否开启局域网调用功能（默认开启）
  """
  def __init__(self,deviceId:str,timer:Timer,setThingModel:function,wlan,
                deviceTypeId:str,hardwareInfoLoader:HardwareInfoLoader,proxyPath = "proxy",servicePath = "/service",
                BASE_PATH="/",SDK_PATH="/lib/sdk",openHttp=True):
    # 同步时间
    TimeUtil.setTime()
    # 初始化配置文件
    config.initTopic(deviceId)
    config.initPath(BASE_PATH,servicePath,proxyPath)
    # 配置物模型读写函数
    thingProxyFuncLoader.setFunc(setThingModel)
    # 保存硬件信息加载回调
    applicationContext.hardwareInfoLoader = hardwareInfoLoader
    # 读取proxy字典
    # todo basepath可以使用config里存储的内容
    applicationContext.proxyDict = ProxyLoader.loadProxyDict(proxyPath,BASE_PATH)
    applicationContext.proxyDict.update(ProxyLoader.loadProxyDict(pathUtils.joinPath(SDK_PATH,"./proxy"),BASE_PATH))
    # 解析并存储服务字典
    applicationContext.serviceDict = ServiceLoader.LoadServiceDict(servicePath,BASE_PATH)
    # 初始化mqtt服务
    applicationContext.pervasiveMqttClient = MqttService(deviceId)


    # mqtt上报设备状态信息
    print("=========wlanInfo=============")
    serviceList = applicationContext.getServiceListInfo()
    essid = wlan.config("essid")
    # 扫描附近的Wi-Fi网络
    networks = wlan.scan()
    print(networks)
    print(essid)
    routerMacBytes = None
    for network in networks:
        print(network)
        if bytes.decode(network[0]) == essid:
            routerMacBytes = network[1]
            break
    routerMac = ':'.join('{:02x}'.format(b) for b in routerMacBytes)
    macBytes = wlan.config("mac")
    macStr = ':'.join('{:02x}'.format(b) for b in macBytes)
    deviceInfo = {}
    deviceInfo["macAddress"] = macStr
    deviceInfo["routerMacAddress"] = routerMac
    deviceInfo["ipAddress"] = wlan.ifconfig()[0]
    deviceInfo["serviceList"] = serviceList
    deviceInfo["deviceTypeId"] = deviceTypeId
    print(deviceInfo)
    applicationContext.deviceInfo = deviceInfo
    config.deviceInfo = deviceInfo

    applicationContext.pervasiveMqttClient.sendMsg(config.UPLOAD_SERVICE_LIST_TOPIC,ujson.dumps(deviceInfo))

    # 初始化定时任务  
    tasks = []
    tasks.append(MqttHealthJob(intervalTime=60000))
    tasks.append(ContextUploadJob(intervalTime=10000))
    tasks.append(MqttCheckMessageJob(intervalTime=500))
    tasks.append(EventListenerJob(intervalTime=5000))
    applicationContext.taskServer = ScheduleService(timer,tasks)
    # 初始化服web服务 
    if(openHttp):
      from .systemService import httpService
      self.webServer = httpService.webServerInit()
    EventInvoker.invokeSystemEvent("ONLINE")
    HardwareUpLoadSender.send()

  
    



    

    
  