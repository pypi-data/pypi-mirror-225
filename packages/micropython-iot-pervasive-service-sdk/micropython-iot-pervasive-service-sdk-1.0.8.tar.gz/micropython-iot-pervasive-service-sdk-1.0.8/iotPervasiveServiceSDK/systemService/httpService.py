from ..model.microWebSrv.microWebSrv import MicroWebSrv
from ..router import httpRouter  # ! 此语句引入了HTTP路由不要删除

#web服务
webserver = None


# web服务器初始化
def webServerInit():
  global webserver
  webserver = MicroWebSrv(webPath='www/')
  webserver.MaxWebSocketRecvLen     = 256
  webserver.WebSocketThreaded= False
  webserver.Start()


