#Data : 2020-5-30
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : Provide server and service access

import requests
import json
import time
import os

from .utils import HttpHelper
from .utils import CommonMethod
from .base import Service
from .modelserivce import ModelService
from .modelservicerecord import ModelServiceRunningRecord
from .modelserviceinstance import ModelServiceInstance
from .data import Data
from .data import DataConfigrationItem

class ServiceAccess(Service):
    def __init__(self, ip: str, port: int):
        Service.__init__(self, ip, port)

    def getModelServicesList(self, start: int = 0, count: int = -1) -> list:
        query = ''
        if count < 1:
            query = ''
        else:
            query = ("?start=" + str(start) + "&count=" + str(count))
        jsData = HttpHelper.Request_get_sync(self.ip, self.port, "/modelser/json/all" + query)
        mslist = []
        if CommonMethod.getJsonValue(jsData, "result") == "suc":
            jsMss = CommonMethod.getJsonValue(jsData, "data")
            for index, item in enumerate(jsMss):
                model = CommonMethod.getJsonValue(item, "ms_model")
                if model == "":
                    continue
                user = CommonMethod.getJsonValue(item, "ms_user")
                if user == "":
                    user = { "u_name" : "", "u_email" : "" }
                try:
                    if CommonMethod.getJsonValue(item, "ms_limited") == "":
                        item['ms_limited'] = u'0'
                    ms = ModelService(self.ip, self.port, CommonMethod.getJsonValue(item, "_id"), CommonMethod.getJsonValue(model, "m_name"), CommonMethod.getJsonValue(model, "m_type"), CommonMethod.getJsonValue(model, "m_url"), CommonMethod.getJsonValue(model, "p_id"), CommonMethod.getJsonValue(model, "m_id"), CommonMethod.getJsonValue(model, "m_register"), CommonMethod.getJsonValue(item, "ms_des"), CommonMethod.getJsonValue(item, "mv_xml"),CommonMethod.getJsonValue(item, "mv_num"), int(CommonMethod.getJsonValue(item, "ms_platform")), CommonMethod.getJsonValue(item, "ms_update"), CommonMethod.getJsonValue(item, "ms_img"), CommonMethod.getJsonValue(user, "u_name"), CommonMethod.getJsonValue(user, "u_email"), int(CommonMethod.getJsonValue(item, "ms_status")), int(CommonMethod.getJsonValue(item, "ms_limited")), int(CommonMethod.getJsonValue(item, "ms_permission")))
                    mslist.append(ms)
                except ZeroDivisionError as ex:
                    print (str(ex))
        return mslist

    def getModelServiceByID(self, msid: str) -> ModelService:
        jsData = HttpHelper.Request_get_sync(self.ip, self.port, "/modelser/json/" + msid)
        ms = None
        if CommonMethod.getJsonValue(jsData, "result") == "suc":
            jsMs = CommonMethod.getJsonValue(jsData, "data")
            model = CommonMethod.getJsonValue(jsMs, "ms_model")
            if model == "":
                return None
            user = CommonMethod.getJsonValue(jsMs, "ms_user")
            if user == "":
                user = { "u_name" : "", "u_email" : "" }
            ms = ModelService(self.ip, self.port, CommonMethod.getJsonValue(jsMs, "_id"), CommonMethod.getJsonValue(model, "m_name"), CommonMethod.getJsonValue(model, "m_type"), CommonMethod.getJsonValue(model, "m_url"), CommonMethod.getJsonValue(model, "p_id"), CommonMethod.getJsonValue(model, "m_id"), CommonMethod.getJsonValue(model, "m_register"), CommonMethod.getJsonValue(jsMs, "ms_des"), CommonMethod.getJsonValue(jsMs, "ms_xml"), CommonMethod.getJsonValue(jsMs, "mv_num"), int(CommonMethod.getJsonValue(jsMs, "ms_platform")), CommonMethod.getJsonValue(jsMs, "ms_update"), CommonMethod.getJsonValue(jsMs, "ms_img"), CommonMethod.getJsonValue(user, "u_name"), CommonMethod.getJsonValue(user, "u_email"), int(CommonMethod.getJsonValue(jsMs, "ms_status")), int(CommonMethod.getJsonValue(jsMs, "ms_limited")), int(CommonMethod.getJsonValue(jsMs, "ms_permission")))
        return ms

    def getModelServiceRunningRecordByID(self, msrid: str) -> ModelServiceRunningRecord:
        jsData = HttpHelper.Request_get_sync(self.ip, self.port, "/modelserrun/json/" + msrid)
        msr = None
        if jsData["result"] == "suc":
            jsMsr = jsData["data"]
            msr = ModelServiceRunningRecord(self.ip, self.port, CommonMethod.getJsonValue(jsMsr, "_id"), CommonMethod.getJsonValue(CommonMethod.getJsonValue(jsMsr, "msr_ms"), "_id"), CommonMethod.getJsonValue(jsMsr, "msr_guid"), int(CommonMethod.getJsonValue(jsMsr, "msr_status")))
        return msr

    def getModelServiceInstanceByGUID(self, guid: str) -> ModelServiceInstance:
        jsData = HttpHelper.Request_get_sync(self.ip, self.port, "/modelins/json/" + guid)
        mis = None
        if jsData["result"] == "suc" and int(jsData["code"]) == 1 :
            jsMis = jsData["data"]
            mis = ModelServiceInstance(self.ip, self.port, str(CommonMethod.getJsonValue(jsMis, "state")), str(CommonMethod.getJsonValue(jsMis, "event")), str(CommonMethod.getJsonValue(jsMis, "guid")), str(CommonMethod.getJsonValue(jsMis, "start")), str(CommonMethod.getJsonValue(CommonMethod.getJsonValue(jsMis, "ms"), "_id")))
        return mis

    def uploadDataByFile(self, tag: str, filepath: str) -> str:
        data = {"gd_tag" : tag}  
        files = {  
            "myfile" : open(filepath, "rb")  
        }
        r = requests.post("http://" + self.ip + ":" + str(self.port) + "/geodata?type=file", data, files=files)
        jsData = json.loads(r.text)
        if jsData["result"] == "suc":
            return CommonMethod.getJsonValue(jsData, "data")
        return ""

    def getDataByID(self, dataid: str) -> Data:
        jsData = HttpHelper.Request_get_sync(self.ip, self.port, "/geodata/json/" + dataid)
        dat = None
        if jsData == "Error":
            return None
        if jsData["result"] == "suc" and jsData["data"] != "":
            jsGData = jsData["data"]
            dat = Data(CommonMethod.getJsonValue(jsGData, "gd_id"), CommonMethod.getJsonValue(jsGData, "gd_tag"), CommonMethod.getJsonValue(jsGData, "gd_type"), int(CommonMethod.getJsonValue(jsGData, "gd_size")), CommonMethod.getJsonValue(jsGData, "gd_value"), CommonMethod.getJsonValue(jsGData, "gd_datetime"), self.ip, self.port)
        return dat

    def createDataConfigurationItem(self, state: str, eventname: str, dataid: str) -> DataConfigrationItem:
        if CommonMethod.IsGUID(state):
            return DataConfigrationItem(state, "", eventname, dataid)
        else :
            return DataConfigrationItem("", state, eventname, dataid)

class Server(Service):
    def __init__(self, ip: str, port: int):
        Service.__init__(self, ip, port)
    
    def getServiceAccess(self) -> ServiceAccess:
        if self.connect() :
            return ServiceAccess(self.ip, self.port)
        return None

    def testAllServices(self, count: int = -1, timeout: int = 7200) -> None:
        success = []
        error = []
        count_done = 0
        currdir = os.path.abspath(os.curdir)
        try:
            if self.connect() : 
                access = self.getServiceAccess()
                if count < 100:
                    list_ms = access.getModelServicesList()
                    for index, item in enumerate(list_ms):
                        print ('Service ID: [' + item.id + '] Name [' + item.name + '] start to test!')
                        time.sleep(5)
                        if item.testify(timeout) == 1:
                            count_done = count_done + 1
                            print ('Service ID: [' + item.id + '] Name [' + item.name + '] test successfully!')
                            success.append(item.id)
                        else:
                            print ('Service ID: [' + item.id + '] Name [' + item.name + '] test fail!')
                            error.append(item.id)
                        print ('[' + str(count_done) + ']/[' + str(count) + ']')
                else:
                    index = int(count / 100)
                    for num in range(0, (index + 1)):
                        list_ms = access.getModelServicesList(num*100, 100)
                        for index, item in enumerate(list_ms):
                            print ('Service ID: [' + item.id + '] Name [' + item.name + '] start to test!')
                            time.sleep(5)
                            if item.testify(timeout) == 1:
                                count_done = count_done + 1
                                print ('Service ID: [' + item.id + '] Name [' + item.name + '] test successfully!')
                                success.append(item.id)
                            else:
                                print ('Service ID: [' + item.id + '] Name [' + item.name + '] test fail!')
                                error.append(item.id)
                            print ('[' + str(count_done) + ']/[' + str(count) + ']')
            else:
                print ("Can not connect!")
        except Exception as e:
            print(e.message)

        logfile = open(currdir + '/TestLog.log', "w")
        logfile.write("Finished : " + str(count_done) + "\n")
        logfile.write("Success : " + str(success) + "\n")
        logfile.write("Error : " + str(error) + "\n")

        logfile.close()