from ..core.loader import thingProxyFuncLoader
import ujson


'''
物模型属性读写代理
'''
class thingProxy():
  
  initdata = None
  def __init__(self,initdata) -> None:
    self.initdata = initdata
    pass

  def handle(self,request):
    if(self.initdata["operation"]=="read"):
      return thingProxyFuncLoader.readFunc()
    elif(self.initdata["operation"]=="writer"):
#       request=ujson.loads(request)
      return thingProxyFuncLoader.writerFunc(request)
    else:
      raise Exception("no operation is"+ self.initdata["operation"])