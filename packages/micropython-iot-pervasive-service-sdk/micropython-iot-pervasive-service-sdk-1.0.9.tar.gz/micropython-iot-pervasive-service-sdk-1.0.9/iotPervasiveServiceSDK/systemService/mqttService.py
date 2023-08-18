from umqtt.simple import MQTTClient    # MQTT库
from ..core.scheduleService import ScheduleBase
from .. import config
from ..router import mqttRouter
import ujson
import _thread
import time



# 泛在云mqtt服务
class MqttService(ScheduleBase):
  #mqtt客户端
  client = None
  deviceId = "Unknown Device"
  lock=_thread.allocate_lock()

  
  """
  * deviceId   泛在平台设备id
  * address   mqtt地址
  * port  mqtt端口号
  """
  def __init__(self,deviceId:str,address:str=config.MQTT_ADDRESS ,port=config.MQTT_PORT):
    print("((((((((((((((((((((((((((()))))))))))))))))))))))))))")
    print(address)
    print(port)
    self.deviceId = deviceId
    if address == config.MQTT_ADDRESS and port == config.MQTT_PORT:
        self._SystemMqttInit()
    else:
        self._MqttInit(address,port)
    print("MQTT Init Success")

    

  '''
  * 消息监听
  '''
  def check_msg(self):
    try:
        self.client.check_msg()
    except:
        print("check_msg error")
    

  """
  * mqtt初始化
  """
  def _SystemMqttInit(self):
    self.client = MQTTClient(self.deviceId, config.MQTT_ADDRESS, config.MQTT_PORT,keepalive=60)  # 创建MQTT对象
    willMsg = {
      "deviceInstanceId":config.DEVICE_ID,
      "serviceUrl": "systemService",
	    "versionCode": 0,
	    "eventId": "OFFLINE",
	    "msg": None
      }
    self.client.set_last_will(config.ON_EVENT_TOPIC,ujson.dumps(willMsg))
    self.client.set_callback(self.sub_cb)
    self.client.connect()
    # 消息订阅    
    self.client.subscribe(config.INVOCATION_SERVICE_EXECUTE_TOPIC)
    self.client.subscribe(config.UPDATE_SERVICE_TOPIC)

  """
  * mqtt初始化
  """
  def _MqttInit(self,address:str,port:int):
    self.client = MQTTClient(self.deviceId, address, config.MQTT_PORT,keepalive=60)  # 创建MQTT对象
    self.client.connect()



  """
  * 发送消息
  * topIc 主题消息 字符串消息
  * message 一般为一个json格式的字符串
  """
  def sendMsg(self,topic:str,message:str):
    if self.lock.acquire():
        try:
            self.client.publish(topic,message.encode('utf-8'))
        except :
            self._SystemMqttInit()
        finally :
            self.lock.release()

  def ping(self):
    self.client.ping()


  """
  * 消息回调
  """
  def sub_cb(self, topic, msg):
    try:
      topic = topic.decode()
      msg = msg.decode()
      mqttRouter.topicRouter(topic,msg)
    except:
      pass
  
  def close(self):
    self.client.disconnect()




