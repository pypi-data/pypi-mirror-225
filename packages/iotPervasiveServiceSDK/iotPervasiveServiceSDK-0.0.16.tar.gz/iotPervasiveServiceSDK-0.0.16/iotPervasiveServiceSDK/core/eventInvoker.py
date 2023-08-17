from . import applicationContext
from .. import config
from ..pojo.serviceBean import ServiceBean
from ..pojo.eventBean import EventBean
from .exception.serviceException import ServiceNotExistException
from .exception.serviceException import EventNotExistException
from ..model.ujinja.source import TemplateEngine
from ..systemService.mqttService import MqttService
import json
import os

'''
* 事件调用类
'''
class EventInvoker:

  '''
  *调用系统事件
  '''
  @staticmethod
  def invokeSystemEvent(eventId:str,eventArgs:dict = {}):
    EventInvoker.invokeEvent("systemService",eventId,eventArgs)


  '''
  * 调用事件
  * serviceId 服务id
  * eventId 事件id
  * eventArgs 事件参数字典
  '''
  @staticmethod
  def invokeEvent(serviceId:str,eventId:str,eventArgs:dict = {}):
    eventArgs["system"] = applicationContext.getSystemInfo()
    
    service:ServiceBean = applicationContext.serviceDict.get(serviceId,None)
    if service == None:
      raise ServiceNotExistException(serviceId)
    
    event:EventBean = service.eventBeanDict.get(eventId,None)
    if event == None:
      raise EventNotExistException(eventId,serviceId)
    
    eventMsg = None
    if event.messageMapper!=None:
      if(event.messageLanguage == "jinja2" or event.messageLanguage == None):
          inputTemplateEngine = TemplateEngine()
          inputTemplateEngine.load_template(event.messageMapper)
          eventMsg = inputTemplateEngine.render_template(eventArgs)
          print("== event msg Mapper == ")
          print(eventMsg)

    # 默认是mqtt的方式上报topic
    if event.protocolType == "MQTT" or event.protocolType == None:
      EventInvoker._MQTTEventSender(service,event,eventMsg)


  '''
  * mqtt事件发送
  '''
  @staticmethod
  def _MQTTEventSender(service:ServiceBean,event:EventBean,eventMsg:str):
    host:str = event.attributes.get("host",None)
    isSystemMqtt = False
    mqttClient = None

    # 默认使用系统的mqtt客户端
    if host == "" or host == None:
      isSystemMqtt = True
      mqttClient = applicationContext.pervasiveMqttClient
    else:
      addressList:list = host.split(":")
      addressList[1] = int(addressList[1])
      if addressList[0] == config.MQTT_ADDRESS and addressList[1] == config.MQTT_PORT:
        isSystemMqtt = True
        mqttClient = applicationContext.pervasiveMqttClient
      else:
        mqttClient = MqttService(''.join([('0'+hex(ord(os.urandom(1)))[2:])[-2:] for x in range(8)]),addressList[0],addressList[1])

    topic = event.attributes.get("topic",config.ON_EVENT_TOPIC)
    msgJsonDict = {
      "deviceInstanceId":config.DEVICE_ID,
      "serviceUrl": service.url,
      "versionCode": service.versionCode,
      "eventId":event.eventId,
      "msg": eventMsg
    }

    mqttClient.sendMsg(topic,json.dumps(msgJsonDict, ensure_ascii=False))
    # 如果非系统的mqtt客户端则关闭
    if not isSystemMqtt:
      mqttClient.close()


  def getEventMsgStr(service:ServiceBean,event:EventBean,eventMsg:str):
    msgJsonDict = {
      "deviceInstanceId":config.DEVICE_ID,
      "serviceUrl": service.url,
      "versionCode": service.versionCode,
      "eventId":event.eventId,
      "msg": eventMsg
    }
    return json.dumps(msgJsonDict, ensure_ascii=False)
    


  
  

    
