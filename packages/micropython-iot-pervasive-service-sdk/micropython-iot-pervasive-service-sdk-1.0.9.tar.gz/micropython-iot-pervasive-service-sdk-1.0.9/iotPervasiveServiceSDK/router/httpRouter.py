from ..model.microWebSrv.microWebSrv import MicroWebSrv
from ..core.serverInvoker import ServerInvoker
import ujson
from ..systemService import updateService
from ..utils import TimeUtil


# web局域网服务调用
@MicroWebSrv.route("/client/invocation/<deviceId>/<serviceId>/<capabilityId>", "POST")
def _httpHandlerInvokerPost(httpClient, httpResponse, args):
    print("======rest server invoke======")
    event = httpClient.ReadRequestPostedFormData()
    keys = list(event.keys())
    msgJson = ujson.loads(keys[0])
    # TODO 根据模板引擎和参数合并出json 再做解析
    runSuccess = False
    responce = None
    try:
        responce = ServerInvoker.invokeService(
            args["serviceId"], args["capabilityId"], msgJson["param"]
        )
        runSuccess = True
    except Exception as e:
        runSuccess = False
        responce = e
    # 拼接msg
    msgDict = {
        "success": runSuccess,
        "data": responce,
        "timestamp": TimeUtil.getTimerMs(),
    }
    print(msgDict)
    httpResponse.WriteResponseOk(
        headers=None,
        contentType="text/json",
        contentCharset="UTF-8",
        content=ujson.dumps(msgDict),
    )


# web局域网服务下载
# @MicroWebSrv.route('/client/update/<deviceId>/<serviceId>','POST')
# def _httpHandlerInvokerPost(httpClient, httpResponse,args):
#   print("======rest server update======")
#   runSuccess = False
#   responce = None
#   try :
#     updateService.updateService(topic[4])
#     runSuccess = True
#   except Exception as e:
#     runSuccess = False
#     responce = e
#   # 拼接msg
#   msgDict = {
#     "success" : runSuccess,
#     "data" : responce,
#     "timestamp":TimeUtil.getTimerMs()
#   }
