import os
import sys
  
'''
代理加载工具
'''
class ProxyLoader:
  """
  * 读取模块字典
  * modelPath   model所在路径,相对于src目录
  """
  def loadProxyDict(proxyPath,BASE_PATH):
    proxyDict = {}
    absolutePath=proxyPath[0]=='/' and BASE_PATH+proxyPath or BASE_PATH+"/"+proxyPath
    proxyList = []
    try:
      proxyList = os.listdir(absolutePath)
    except Exception as e:
      print("Search Path Fail:Path does not exist. modelPath is ",absolutePath)
    proxyPath = proxyPath[0]=='/' and proxyPath[1:] or proxyPath
    proxyPath = proxyPath.replace("/",".")+"."
    for proxyName in proxyList:
      if proxyName.index(".py")>0:
        name = proxyName.replace(".py","")
        exec('import '+ proxyPath + name , {} )
        proxyDict[name] = sys.modules[proxyPath + name]
        print("loading Proxy "+name)
    print("Load Proxy Success")
    return proxyDict



