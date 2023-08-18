#Data : 2020-5-30
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : Provide running log

import json
from .utils import CommonMethod

class RunningLog:
    def __init__(self, type: str, state: str, event: str, flag: str, message: str, datetime: str):
        self.type = type
        self.state = state
        self.event = event
        self.flag = flag
        self.message = message
        self.detatime = datetime
        self.mark = False

    def setMark(self, value: bool) -> None:
        self.mark = value

    @staticmethod
    def ConvertJson2Log(jsLogs: list) -> list:
        logs = []
        for index,item in enumerate(jsLogs):
            log = RunningLog(CommonMethod.getJsonValue(item, "Type"), CommonMethod.getJsonValue(item, "State"), CommonMethod.getJsonValue(item, "Event"), int(CommonMethod.getJsonValue(item, "Flag")), CommonMethod.getJsonValue(item, "Message"),CommonMethod.getJsonValue(item, "Datetime"))
            logs.append(log)
        return logs
            
    @staticmethod
    def AppendJson2Log(logs: list, jsLogs: list):
        count = len(logs)
        for index,item in enumerate(jsLogs):
            if index < count:
                continue
            log = RunningLog(CommonMethod.getJsonValue(item, "Type"), CommonMethod.getJsonValue(item, "State"), CommonMethod.getJsonValue(item, "Event"), int(CommonMethod.getJsonValue(item, "Flag")), CommonMethod.getJsonValue(item, "Message"), CommonMethod.getJsonValue(item, "DateTime"))
            logs.append(log)