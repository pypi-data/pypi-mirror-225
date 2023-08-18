# 代理类型的基类
class ProxyBase:
  operation = None
  
  def handle(self,request):
    print("编写代理类时需要重写代理类型的handle方法")