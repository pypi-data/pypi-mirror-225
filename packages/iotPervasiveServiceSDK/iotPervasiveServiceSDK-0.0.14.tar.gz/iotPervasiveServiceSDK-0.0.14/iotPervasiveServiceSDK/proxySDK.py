import sys
import os
from .utils import logutil
from .utils import netUtils
log = logutil.get_logger(__name__)
# 获取主程序所在的目录
program_dir = os.path.dirname(sys.argv[0])
program_path = os.path.abspath(program_dir)
log.info("程序所在目录:"+ program_path)
# 获取当前文件的绝对路径
model_file_path = os.path.abspath(__file__)
# 获取当前文件所在的目录
model_directory = os.path.dirname(model_file_path)
log.info("模块所在目录:"+ model_directory)

from typing import Callable
from .systemService.mqttService import MqttService
from .core import applicationContext
from .core.loader.proxyLoader import ProxyLoader
from .core.loader.serversLoader import ServiceLoader
from .utils import pathUtils as PathUtil
from .core.scheduleService import ScheduleService
from .core.job.mqttCheckMessageJob import MqttCheckMessageJob
from .core.job.contextUpLoadJob import ContextUploadJob
from .core.job.eventListenerJob import EventListenerJob
from . import config
from .utils import netUtils
from .core.loader import thingProxyFuncLoader
import  json
from .core.eventInvoker import EventInvoker
from .core.loader.hardwareInfoLoader import HardwareInfoLoader
from .core.sender.hardwareUpLoadSender import HardwareUpLoadSender


class ProxySDK:
  # 泛在web服务
  webServer = None

  # 泛在mqtt服务
  mqttClient = None


  """
  * 全部功能初始化
  * deviceId   泛在平台设备id
  * timer      需要使用的定时器
  * setThingModel 物模型读写函数
  * wlan 网络对象 micropython连接网络和存储网络信息的对象
  * deviceTypeId 所属设备类型的id
  * proxyPath 代理所在路径（用户自定义代理）（默认proxy文件夹）
  * servicePath 服务存储到哪个位置（默认"/service"）
  * BASE_PATH 程序基本路径（默认为根目录）
  * SDK_PATH SDK所在路径（默认upip下载路径）
  * openHttp 是否开启局域网调用功能（默认开启）
  """
  def __init__(self,deviceId:str,setThingModel:Callable,
                deviceTypeId:str,hardwareInfoLoader:HardwareInfoLoader,proxyPath = PathUtil.joinPath(program_path,"proxy"),servicePath = "service",
                BASE_PATH=program_path,SDK_PATH=model_directory,openHttp=True):
    # 初始化配置文件
    config.initTopic(deviceId)
    config.initPath(BASE_PATH,servicePath,proxyPath)
    # 配置物模型读写函数
    thingProxyFuncLoader.setFunc(setThingModel)
    # 读取proxy字典
    #   加载用户代理
    applicationContext.proxyDict = ProxyLoader.loadProxyDict(proxyPath,BASE_PATH)
    #   加载系统代理
    applicationContext.proxyDict.update(ProxyLoader.loadProxyDict( PathUtil.joinPath(SDK_PATH,"proxy"),BASE_PATH))
    # 解析并存储服务字典
    applicationContext.serviceDict = ServiceLoader.LoadServiceDict(servicePath,BASE_PATH)
    # 保存硬件信息加载回调
    applicationContext.hardwareInfoLoader = hardwareInfoLoader
    # 初始化mqtt服务
    applicationContext.pervasiveMqttClient = MqttService(deviceId)


    # mqtt上报设备状态信息
    serviceList = applicationContext.getServiceListInfo()
    ip, mac, bssid = netUtils.getNetInfo()
    deviceInfo = {}
    deviceInfo["macAddress"] = mac.lower()
    deviceInfo["routerMacAddress"] = bssid.lower()
    deviceInfo["ipAddress"] = ip.lower()
    deviceInfo["serviceList"] = serviceList
    deviceInfo["deviceTypeId"] = deviceTypeId
    log.info(deviceInfo)
    applicationContext.stateInfo = deviceInfo
    config.deviceInfo = deviceInfo

    applicationContext.pervasiveMqttClient.sendMsg(config.UPLOAD_SERVICE_LIST_TOPIC,json.dumps(deviceInfo, ensure_ascii=False))

    # 初始化定时任务  
    tasks = []
    # tasks.append(MqttHealthJob(intervalTime=60000))
    tasks.append(ContextUploadJob(intervalTime=10000))
    tasks.append(MqttCheckMessageJob(intervalTime=500))
    tasks.append(EventListenerJob(intervalTime=5000))
    applicationContext.taskServer = ScheduleService(tasks)
    # 初始化服web服务 
    if(openHttp):
      from .systemService import httpService
      self.webServer = httpService.webServerInit()
    EventInvoker.invokeSystemEvent("ONLINE")
    HardwareUpLoadSender.send()

  
    



    

    
  