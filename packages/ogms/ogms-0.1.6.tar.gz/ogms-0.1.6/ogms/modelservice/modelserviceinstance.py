#Data : 2020-5-30
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : Provide model instances service

import time
from .base import Service
from .utils import HttpHelper
from .runninglog import RunningLog
from .utils import CommonMethod

INSTA_UNKNOWN = 0
INSTA_RUNNING = 1
INSTA_REQUESTING = 2
INSTA_HANGING = 3
INSTA_FINISHED = 4

class ModelServiceInstance(Service):
    def __init__(self, ip: str, port: int, state: str, eventname: str, guid: str, startDT: str, serviceID: str, status = INSTA_UNKNOWN, statusDes: str = ""):
        Service.__init__(self, ip, port)
        self.state = state
        self.event = eventname
        self.guid = guid
        self.startDT = startDT
        self.serviceID = serviceID
        self.logs = []
        self.status = status
        self.statusDes = statusDes
    
    def getNewLogs(self) -> list:
        newlogs = []
        for index, item in enumerate(self.logs):
            if item.mark == False:
                newlogs.append(item)
                item.setMark(True)
        return newlogs

    def kill(self) -> bool:
        path = "/modelins/" + self.guid + "?ac=kill"
        jsData = HttpHelper.Request_put_sync(self.ip, self.port, path)
        if jsData["result"] == "suc":
            return True
        return False

    def pause(self) -> bool:
        path = "/modelins/" + self.guid + "?ac=pause"
        jsData = HttpHelper.Request_put_sync(self.ip, self.port, path)
        if jsData["result"] == "suc":
            return True
        return False

    def restart(self) -> bool:
        path = "/modelins/" + self.guid + "?ac=restart"
        jsData = HttpHelper.Request_put_sync(self.ip, self.port, path)
        if jsData["result"] == "suc":
            return True
        return False

    def wait4Status(self, status, timeout: int = 7200, log: bool = False) -> int:
        time_end = time.time() + timeout
        time_now = time.time()
        while self.status != status and time_now < time_end:
            if log:
                newlogs = self.getNewLogs()
                for index, item in enumerate(newlogs):
                    print (item.type + " - " + item.state + " - " + item.event + " - " + item.message)
            time.sleep(2)
            self.refresh()
            time_now = time.time()
        if time_now >= time_end :
            return -1
        return 1

    def wait4StateEvent(self, statename, eventname, timeout = 7200, log = False) -> int:
        time_end = time.time() + timeout
        time_now = time.time()
        if statename == "":
            statename = None
        if eventname == "":
            eventname = None
        while (statename != None or self.state != statename) and (eventname != None or self.event != eventname) and time_now < time_end:
            if log:
                newlogs = self.getNewLogs()
                for index, item in enumerate(newlogs):
                    print (item.type + " - " + item.state + " - " + item.event + " - " + item.message)
            time.sleep(2)
            self.refresh()
            time_now = time.time()
        return 1

    def refresh(self) -> None:
        jsData = HttpHelper.Request_get_sync(self.ip, self.port, "/modelins/json/" + self.guid)
        if jsData["result"] == "suc":
            jsMis = jsData["data"]
            if jsMis != None:
                self.state = CommonMethod.getJsonValue(jsMis, "state")
                self.event = CommonMethod.getJsonValue(jsMis, "event")
                self.status = ModelServiceInstance.ConvertString2Status(CommonMethod.getJsonValue(jsMis, "status"))
                RunningLog.AppendJson2Log(self.logs, CommonMethod.getJsonValue(jsMis, "log"))
                self.statusDes = CommonMethod.getJsonValue(jsMis, "statusDes")
            else :
                self.status = INSTA_FINISHED

    @staticmethod
    def ConvertString2Status(strStatus):
        if strStatus == "RUNNING":
            return INSTA_RUNNING
        elif strStatus == "REQUESTING":
            return INSTA_REQUESTING
        elif strStatus == "HANGING":
            return INSTA_HANGING
        return INSTA_UNKNOWN
