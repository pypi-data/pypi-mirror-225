from ...utils import pathUtils
from ...utils import logutil
from ...pojo.serviceBean import ServiceBean
from ...pojo.capabilityBean import CapabilityBean
from ...pojo.eventBean import EventBean
from ..exception.serviceException import LoadingServiceException
from ..exception.serviceException import LoadPathNotfoundException
import os
from ... import config
from .. import applicationContext
import ujson
import sys
from ...ownService.systemServiceFactory import SystemServiceFactory



log = logutil.get_logger(__name__)
'''
服务加载工具
'''
class ServiceLoader:

  '''
  加载服务字典
  input：
    - servicePath = 服务的相对路径（相对于项目根目录的）
    - BASE_PATH = 基本路径（设备中mian.py所在文件夹的绝对路径）
  '''
  def LoadServiceDict(servicePath,BASE_PATH):
    applicationContext.events = []
    serviceDict = {}
    absolutePath=pathUtils.joinPath(BASE_PATH,servicePath)
    # 遍历文件
    serviceDict = ServiceLoader.dfsDir(absolutePath,servicePath,serviceDict)
    systemServer = ServiceLoader.loadSystemservice()
    serviceDict[systemServer.url] = systemServer
    log.info(serviceDict)
    return serviceDict

  '''
   递归扫描文件
  '''
  def dfsDir(path,servicePath,serviceDict):
    try:
      listdir=os.ilistdir(path)
    except :
      raise LoadPathNotfoundException(path)
    while(True):
      try: 
          pathInfo=next(listdir)
          # 如果是目录             
          if pathInfo[1] == 0X4000:
              # 忽略script文件夹
              if pathInfo[0] == "script":
                  continue
              ServiceLoader.dfsDir(pathUtils.joinPath(path,pathInfo[0]),pathUtils.joinPath(servicePath,pathInfo[0]),serviceDict)
          # 是文件             
          else:
            try:
              if pathInfo[0].find("config.json") >= 0:
                  ServiceLoader.loadingConfigJson(path,servicePath,pathInfo[0],serviceDict)
            except LoadingServiceException as e:
              log.error(e)
            except  Exception as e:
              sys.print_exception(e)
              log.error(repr(e.value))
      except StopIteration as e:
          break
    print(serviceDict.get("superlightServiceImpl",None))
    return serviceDict

  # 读取configJson文件并作解析，将解析后的结果存入字典
  def loadingConfigJson(serviceAbsPath,servicePath,jsonName,serviceDict):
    jsonPath = pathUtils.joinPath(serviceAbsPath,jsonName)
    file = open(jsonPath,"r")
    jsonString = file.read()
    file.close()
#     print(jsonString)
    jsonBean = ujson.loads(jsonString)
    print(jsonBean)
    serviceBean = ServiceLoader.loadingServiceInfo(jsonBean,serviceAbsPath)
    serviceDict[serviceBean.url] = serviceBean


  '''
  * 加载服务信息
  * jsonDict json解析后的字典
  * filePath 文件所在路径
  '''
  def loadingServiceInfo(jsonDict:dict,filePath:str)->ServiceBean:
    # 获取基本信息    
    identifier = jsonDict.get("identifier",None)
    if identifier == None:
      # todo 抛出异常
      print("identifier == None")
      pass
    serviceBean = ServiceBean()
    serviceBean.url = identifier.get("url",None)
    serviceBean.versionCode = identifier.get("versionCode",None)
    if serviceBean.url==None or serviceBean.versionCode==None:
      # todo 抛出异常
      print("serviceBean.url==None or serviceBean.versionCode==None")
      pass
    serviceBean.filePath = filePath
    serviceBean.name = identifier.get("name",None)
    try:
      # 解析其它文件信息
      metaData = jsonDict.get("meta-data",None)
      if metaData != None:
        capabilitiesFileName = metaData.get("capabilities",None)
        if capabilitiesFileName!=None:
          capabilitiesFilePath = pathUtils.joinPath(filePath,capabilitiesFileName)
          serviceBean.capabilityBeanDict=ServiceLoader.loadingCapabilitys(capabilitiesFilePath)
        eventsFileName = metaData.get("events",None)
        if eventsFileName != None:
          eventsFilePath = pathUtils.joinPath(filePath,eventsFileName)
          serviceBean.eventBeanDict = ServiceLoader.loadingEvents(eventsFilePath)
    except LoadingServiceException as e:
      raise LoadingServiceException("ServiceImplId(url) is "+serviceBean.url+str(e))
    except Exception as e:
      sys.print_exception(e)
      raise LoadingServiceException("unknown error : ServiceImplId(url) is "+serviceBean.url)



    return serviceBean
    
  '''
  * 加载能力列表
  '''
  def loadingCapabilitys(capabilitiesFilePath:str)->dict:
    res = {}
    try:
      capabilitiesFile = open(capabilitiesFilePath,"r")
      capabilitiesJsonString = capabilitiesFile.read()
      capabilitiesFile.close()
      capabilitiesJsonArray = ujson.loads(capabilitiesJsonString)["capabilities"]["capability"]
    except KeyError as e:
      # sys.print_exception(e)
      raise LoadingServiceException("keyError: event Json loadFail: Check whether the events and event tags exist in the json format ")
    except OSError as e:
      # sys.print_exception(e)
      raise LoadingServiceException("OsError: The file does not exist: Check whether the service pack is faulty,path:" + capabilitiesFilePath)
    for item in capabilitiesJsonArray:
      try:
        capabilityBean = CapabilityBean()
        capabilityBean.capabilityId = item.get("id",None)
        capabilityBean.proxyType = item.get("proxy",None)
        capabilityBean.attributes = item.get("attributes",None)
        # capabilityBean.inputLanguage = item[inputMapper]
        
        if(item.get("inputMapper",None)!=None):
          mapperInfo = item.get("inputMapper",None)
          capabilityBean.inputLanguage = mapperInfo.get("templateLanguage","jinja2")
          capabilityBean.inputMapper = mapperInfo["templateText"]
        if(item.get("outputMapper",None)!=None):
          mapperInfo = item.get("outputMapper",None)
          capabilityBean.outputLanguage = mapperInfo.get("templateLanguage","jinja2")
          capabilityBean.outputMapper = mapperInfo["templateText"]
        res[capabilityBean.capabilityId] = capabilityBean
        print("=====capability=====")
        print(capabilityBean)
      except Exception as e:
        sys.print_exception(e)
        if(capabilityBean.capabilityId!=None):
          raise LoadingServiceException("capability resolution error: occurred at the location of capability id "+ capabilityBean.capabilityId)
        else:
          raise LoadingServiceException("capability resolution error: The capability id does not exist")



    return res

  def loadingEvents(eventsFilePath:str)->dict:
    res = {}
    try :
      eventsFile = open(eventsFilePath,"r")
      eventsFileJsonStr = eventsFile.read()
      eventsFile.close()  
      eventsFileJsonArray = ujson.loads(eventsFileJsonStr)["events"]["event"]
    except KeyError as e:
      # sys.print_exception(e)
      raise LoadingServiceException("keyError: event Json loadFail: Check whether the events and event tags exist in the json format ")
    except OSError as e:
      # sys.print_exception(e)
      raise LoadingServiceException("OsError: The file does not exist: Check whether the service pack is faulty,path:" + eventsFilePath)
    for item in eventsFileJsonArray:
      try:
        eventBean = EventBean()
        eventBean.eventId = item.get("id",None)
        eventBean.attributes = item["attributes"]
        if(item.get("messageMapper",None)!=None):
          mapperInfo = item.get("messageMapper",None)
          eventBean.messageLanguage = mapperInfo.get("templateLanguage","jinja2")
          eventBean.messageMapper = mapperInfo["templateText"]
        res[eventBean.eventId] = eventBean
        print("=====event=====")
        print(eventBean)
      except Exception as e:
        sys.print_exception(e)
        if(eventBean.eventId!=None):
          raise LoadingServiceException("Event resolution error: occurred at the location of event id "+ eventBean.eventId)
        else:
          raise LoadingServiceException("Event resolution error: The event id does not exist")
    return res


  '''
  * 系统自带事件加载
  '''
  def loadSystemservice() -> ServiceBean:
    
    return SystemServiceFactory.loadSystemService()
    

    
    





