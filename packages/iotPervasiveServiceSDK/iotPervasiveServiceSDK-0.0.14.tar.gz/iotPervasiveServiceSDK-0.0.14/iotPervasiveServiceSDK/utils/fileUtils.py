import requests
import os
from .. import config
import shutil

'''
 删除路径及其中文件
'''
def removePath(path:str):
    shutil.rmtree(path)
    
    
    
    
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
    res = requests.get(url)
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