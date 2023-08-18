from .. import applicationContext
from ... import config
from .baseSender import BaseSender
import json

class HardwareUpLoadSender(BaseSender):

  def send():
    hardwareInfo = applicationContext.hardwareInfoLoader.getHardwareInfo()
    msg = json.dumps(hardwareInfo)
    print(type(msg))
    applicationContext.pervasiveMqttClient.sendMsg(config.UPLOAD_HARDWARE_TOPIC,msg)