#Data : 2020-5-30
#Author : Fengyuan Zhang (Franklin)
#Email : franklinzhang@foxmail.com
#Description : The OGMSService is used to invoke OpenGMS services. This component is the portal for all services, to create Server, TaskServer, DataExchangeServer and DataServiceServer

from .server import Server
from .data import DataConfigrationItem
from .geotaskserver import GeoTaskServer
from .geodataexserver import GeoDataExServer
from .geodatacontainerserver import GeoDataServiceServer

class ServiceCollection:
    @staticmethod
    def CreateServer(ip: str, port: int) -> Server:
        return Server(ip, port)

    @staticmethod
    def CreateTaskServer(ip: str, port: int) -> GeoTaskServer:
        taskServer = GeoTaskServer(ip, port)
        if taskServer.connect():
            return taskServer
        return None
    @staticmethod
    def CreateDataExchangeServer(ip: str, port: int) -> GeoDataExServer:
        dataExchangeServer = GeoDataExServer(ip, port)
        if dataExchangeServer.connect():
            return dataExchangeServer
        return None
    @staticmethod
    def CreateDataServiceServer(ip: str, port: int, userName: str) -> GeoDataServiceServer:
        dataServiceServer = GeoDataServiceServer(ip, port, userName)
        if dataServiceServer.connect():
            return dataServiceServer
        return None