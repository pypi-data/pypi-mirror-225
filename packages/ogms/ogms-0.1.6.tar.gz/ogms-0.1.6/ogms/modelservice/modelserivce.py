#Data : 2020-5-30
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : Provide model service

import time

from .utils import HttpHelper
from .utils import CommonMethod
from .base import Service
from .data import DataConfigrationItem
from .modelserviceinstance import ModelServiceInstance


class ModelService(Service):
    def __init__(self, ip: str, port: int, id: str, name: str, type: str, url: str, pid: str, mid: str, registered: bool, description: str, xml: str, version: str, platform: str, deploymenttime: str, img: str, deployorname: str, deployoremail: str, status: str, limitation: str, permission: str):
        Service.__init__(self, ip, port)
        self.id = id 
        self.name = name
        self.type = type
        self.url = url
        self.pid = pid
        self.mid = mid
        self.registered = registered
        self.description = description
        self.xml = xml
        self.version = version
        self.platform = platform
        self.deploymenttime = deploymenttime
        self.img = img
        self.deployorname = deployorname
        self.deployoremail = deployoremail
        self.status = status
        self.limitation = limitation
        self.permission = permission
    
    def invoke(self, list_data: list) -> str:
        path = "/modelser/" + self.id + "?ac=run&inputdata=["
        for index, item in enumerate(list_data):
            path += "{\"StateId\":\"" + item.stateid + "\",\"StateName\":\"" + item.statename + "\",\"Event\":\"" + item.eventname + "\",\"DataId\":\"" + item.dataid + "\",\"Destoryed\":\"" + str(item.destoryed) + "\"}"
        path += "]"
        jsData = HttpHelper.Request_get_sync(self.ip, self.port, path)
        recordid = -1
        if isinstance(jsData, str):
            raise Exception("Can not invoke model service correctly! message:[" + jsData + "]")
        if jsData["result"] == "suc":
            recordid = jsData["data"]
        return recordid

    def refresh(self) -> int:
        path = "/modelser/json" + self.id        
        jsData = HttpHelper.Request_get_sync(self.ip, self.port, path)
        if jsData["result"] == "suc":
            jsMs = jsData["data"]
            self.status = int(CommonMethod.getJsonValue(jsMs, "ms_status"))
            self.limitation = int(CommonMethod.getJsonValue(jsMs, "ms_limited"))
            return 1
        return -1

    def start(self) -> int:
        jsData = HttpHelper.Request_put_sync(self.ip, self.port, '/modelser/' + self.id + '?ac=start')
        if CommonMethod.getJsonValue(jsData, 'result') == 'suc':
            return 1
        return -1

    def testify(self, timeout: int = 7200) -> int:
        path = "/modelser/testify/" + self.id        
        jsData = HttpHelper.Request_get_sync(self.ip, self.port, path)
        if jsData["status"] == 1:
            title = None
            testifies = jsData["testifies"]
            for index, item in enumerate(testifies):
                title = item["title"]
                break
            if title == None:
                return -2 #! Error in read testify title
            jsData = HttpHelper.Request_put_sync(self.ip, self.port, "/modelser/testify/" + self.id + "?path=" + title)
            if jsData["status"] == 1:
                inputs = jsData["dataInputs"][0]['inputs']
                list_data = []
                for index, item in enumerate(inputs):
                    list_data.append(DataConfigrationItem(item["StateId"], "", item["Event"], item["DataId"]))
                recordid = self.invoke(list_data)
                if recordid != -1:
                    jsData = HttpHelper.Request_get_sync(self.ip, self.port, "/modelserrun/json/" + recordid)
                    msr = None
                    if jsData["result"] == "suc":
                        jsMsr = jsData["data"]
                        jsData = HttpHelper.Request_get_sync(self.ip, self.port, "/modelins/json/" + CommonMethod.getJsonValue(jsMsr, "msr_guid"))
                        mis = None
                        if jsData["result"] == "suc" and int(jsData["code"]) == 1 :
                            jsMis = jsData["data"]
                            mis = ModelServiceInstance(self.ip, self.port, str(CommonMethod.getJsonValue(jsMis, "state")), str(CommonMethod.getJsonValue(jsMis, "event")), str(CommonMethod.getJsonValue(jsMis, "guid")), str(CommonMethod.getJsonValue(jsMis, "start")), str(CommonMethod.getJsonValue(CommonMethod.getJsonValue(jsMis, "ms"), "_id")))
                            if mis.wait4Status(4, timeout) < 0:
                                mis.kill()
                                return -6 # Timeout
                            if mis.status == 4:
                                return 1
                            else:
                                return -5 #Error in running model service
                    return -4 #! Record can not be found
                return -3 #! Error in read testify files
        return -1 #! Error in read testify files
