import urequests
import os
from ..utils import pathUtils
from .. import config

'''
 删除路径及其中文件
'''
def removePath(path:str):
    pathIterator = os.ilistdir(path)
    while(True):
        try:
            pathInfo=next(pathIterator)
            # 如果是目录             
            if pathInfo[1] == 0X4000:
                nextPath=pathUtils.joinPath(path,pathInfo[0])
                removePath(nextPath)
            # 是文件             
            else:
                nextPath=pathUtils.joinPath(path,pathInfo[0])
                os.remove(nextPath)
        except Exception as e:
            break
    os.rmdir(path)
    
    
    
    
'''
 下载文件
 url:文件链接
 path:目标路径（包含文件名）
'''
def downloadFile(url:str,path:str):
    # 确认路径存在    
    pathList = path.split('/')
    pathList[-1] = ""
    fileFolderPath = "/".join(pathList)
    
    # 删除已存在的文件     
    try:
        removePath(path)
    except:
        pass
    
    create_path(fileFolderPath)
    # 下载
    res = urequests.get(url)
    with open(path,"wb") as code:
        code.write(res.content)

'''
  创建路径
'''
def create_path(path):
    os.chdir(config.BASE_PATH)
    path_list = path.split('/')
    for i in range(1, len(path_list)):
        try:
            os.chdir(path_list[i])
        except:
            os.mkdir(path_list[i])
            os.chdir(path_list[i])
    os.chdir(config.BASE_PATH)