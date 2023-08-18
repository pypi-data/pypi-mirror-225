from ..scheduleService import ScheduleBase
from .. import applicationContext
from ... import config
import network
from ...utils import TimeUtil
from ...proxy.thingProxy import thingProxy
import ujson


class ContextUploadJob(ScheduleBase):

  """
  * 发送情境消息
  """
  def handleInterrupt(self):
    wlan = network.WLAN(network.STA_IF)
    thingModel = thingProxy({"operation":"read"}).handle(None)
    services = applicationContext.getServiceListInfo()
    # 拼接msg
    msgDict = {
      "timestamp": TimeUtil.getTimerMs(),
      "lanIp" : wlan.ifconfig()[0],
      "thingModel":thingModel,
      "serviceList":services
    }
    applicationContext.pervasiveMqttClient.sendMsg(config.UPLOAD_CONTEXT_TOPIC,ujson.dumps(msgDict))
    
  def upLoadServiceList(self):
    services = applicationContext.getServiceListInfo()



    
        
    
    
    
    
    
    