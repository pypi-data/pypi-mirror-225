#Data : 2020-5-30
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : Provide data services

import urllib3
import json

from .utils import HttpHelper
from .utils import CommonMethod
from .base import Service

class Data(Service):
    def __init__(self, id: str, tag: str, type: str, size: int, value: str, datetime: str, ip: str, port: int):
        Service.__init__(self, ip, port)
        self.id = id
        self.tag = tag
        self.type = type
        self.size = size
        self.value = value
        self.datetime = datetime

    def isExist(self) -> bool:
        jsData = HttpHelper.Request_get_sync(self.ip, self.port, "/geodata/json/" + self.id)
        if CommonMethod.getJsonValue(jsData, "result") == "suc" :
            if CommonMethod.getJsonValue(jsData, "data") == "":
                return False
            return True
        return False

    def save(self, filepath: str) -> int:
        http = urllib3.PoolManager()
        response = http.request('GET', self.getBaseURL() + "geodata/" + self.id)
        with open(filepath, 'wb') as f:
            f.write(response.data)
        return 1

class DataConfigrationItem:
    def __init__(self, stateid: str, statename: str, eventname: str, dataid: str, destoryed: bool = False, requested: bool = False, optional: bool = False):
        self.stateid = stateid
        self.statename = statename
        self.eventname = eventname
        self.dataid = dataid
        self.destoryed = destoryed
        self.requested = requested
        self.optional = optional

    @staticmethod
    def MakeUpDataItem(jsData: object):
        dat = DataConfigrationItem(CommonMethod.getJsonValue(jsData, "StateId"), CommonMethod.getJsonValue(jsData, "StateName"), CommonMethod.getJsonValue(jsData, "Event"), CommonMethod.getJsonValue(jsData, "DataId"), bool(CommonMethod.getJsonValues(jsData,["Destroyed", "Destoryed"])))
        return dat