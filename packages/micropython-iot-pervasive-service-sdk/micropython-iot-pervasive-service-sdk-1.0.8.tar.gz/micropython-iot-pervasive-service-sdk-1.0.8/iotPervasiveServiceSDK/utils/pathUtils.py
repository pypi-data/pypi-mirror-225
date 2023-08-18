
'''
路径拼接 
'''
def joinPath(path1:str, path2:str):
  if not path2.startswith("/") and not path2.startswith("."):
    return path1.endswith("/") and path1+path2 or path1+"/"+path2
  # 如果path2是绝对路径，直接返回path2
  if path2.startswith("/"):
    return path2
  # 如果path1以/结尾，去掉最后一个/
  if path1.endswith("/"):
    path1 = path1[:-1]
  # 如果path2以./开头，去掉前两个字符
  if path2.startswith("./"):
    path2 = path2[2:]
  # 如果path2以../开头，表示要返回上一级目录
  if path2.startswith("../"):
    # 用/分割path1和path2，并分别存入列表
    parts1 = path1.split("/")
    parts2 = path2.split("/")
    i=0
    # 从后往前遍历parts2列表
    while i <len(parts2):
      # 如果当前元素是..，则从parts1列表中弹出最后一个元素，并从parts2列表中删除当前元素
      if parts2[i] == "..":
        parts1.pop()
        parts2.pop(i)
        i = i-1
      else:
        break
      i=i+1
    # 用/连接parts1和parts2列表，并返回结果
    return "/".join(parts1 + parts2)
  # 否则，用/连接path1和path2，并返回结果
  return path1 + "/" + path2