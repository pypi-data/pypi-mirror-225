

# 服务bean
class ServiceBean:
  # 服务实现的包名，不同版本保持一致
  url = None
  # 名称
  name = None
  # 版本
  versionCode = None
  # 能力 K:能力id   V:能力信息
  capabilityBeanDict = {}
  
  # 事件 k:事件id  V:事件信息
  eventBeanDict = {}
  # 文件所在路径
  filePath = None
  def __init__(self) -> None:
    self.capabilityBeanDict = {}

  def __str__(self):
    return f"ServiceBean(filePath={self.filePath},url={self.url}, name={self.name}, versionCode={self.versionCode}, capabilityBeanDict={self.capabilityBeanDict} ,eventBeanDict = {self.eventBeanDict})"
 