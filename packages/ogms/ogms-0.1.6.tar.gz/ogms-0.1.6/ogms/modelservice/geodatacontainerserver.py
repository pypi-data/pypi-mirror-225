#Data : 2020-5-30
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : Provide data services in data service container and data service container

import json
import urllib3
import os

from .base import Service
from .utils import HttpHelper


class DCData(Service):
    def __init__(self, ip: str, port: int, id: str):
        Service.__init__(self, ip, port)
        self.id = id

    def getURL(self) -> str:
        dataid = self.id
        url = "http://" + self.ip + ":" + str(self.port) + "/dataResource/getResource?sourceStoreId=" + dataid
        return str(url)

    def download(self, path: str) -> None:
        filepath = path
        url = self.getURL()
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        with open(filepath, 'wb') as f:
            f.write(response.data)


class GeoDataServiceServer(Service):
    def __init__(self, ip: str, port: int, userName: str):
        Service.__init__(ip, port)
        self.userName = userName

    def connect(self) -> bool:
        jsData = HttpHelper.Request_get_sync(self.ip, self.port, "/ping")
        if (jsData['data'] == 'OK'):
            return True
        else:
            return False

    def upload(self, datapath: str, tag: str = "") -> DCData:
        (filepath, tempfilename) = os.path.split(datapath)
        (filename, extension) = os.path.splitext(tempfilename)
        extension = extension[1:len(extension)]
        files = {
            "file" : open(datapath, "rb")
        }
        path = "/file/upload/store_dataResource_files"
        data = None
        jsData = HttpHelper.Request_post_sync(self.ip, self.port, path, None, files)
        if jsData['code'] == 0:
            if jsData['data'] != '':
                dataId = jsData['data']
                formData = {
                    "author": self.userName,
                    "fileName": filename,
                    "sourceStoreId": dataId,
                    "suffix": extension,
                    "type": "OTHER"
                }
                dataUrl = "/dataResource"
                jsresult = HttpHelper.Request_post_sync(self.ip, self.port, dataUrl, formData)
                if jsresult['code'] == 0:
                    data = DCData(self.ip, self.port, dataId)
        return data

