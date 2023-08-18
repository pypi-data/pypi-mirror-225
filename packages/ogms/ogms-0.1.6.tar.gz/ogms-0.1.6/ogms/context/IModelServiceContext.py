"""
@Description 模型封装接口
@Author : 7bin
@Date : 2022/10/14 16:55
"""
from abc import abstractmethod, ABCMeta
from enum import Enum
from typing import Optional

# 常量
DEFAULT_STATE_NAME = "RUNSTATE"
DEFAULT_EVENT_NAME = "RUNEVENT"


class ERequestResponseDataMIME(Enum):
    """
    数据类型
    """
    TEXT = "text"  # 文本类型
    FILE = "file"  # 文件类型
    UNKNOWN = "unknown"  # 未知类型


class ExecExtension(Enum):
    """
    可执行程序扩展后缀
    """
    EXE = 1  # C等语言
    JAR = 2  # Java
    SH = 3  # Linux
    PY = 4  # Python


class IModelServiceContext(metaclass=ABCMeta):
    """
    模型行为标准化封装方法

    行为接口：
    string onInitialize(string host, int port, string insID)  初始化模型
    void onEnterState(string stateName)	进入状态
    void onFireEvent(string eventName)	激发事件
    void onLeaveState(string stateName)	退出状态
    void onFinalize()	结束运行并释放资源

    数据接口：
    void onRequestData()	拉取当前数据
    void onResponseData()	提交当前数据

    调用接口：
    void invoke(ExecExtension ext)  调用可执行程序

    日志接口：
    void onPostMessageInfo(string msg)	派送一般消息
    void onPostWarningInfo(string msg)	派送警告消息
    void onPostErrorInfo(string msg)	派送错误消息
    """

    @abstractmethod
    def setModelName(self, modelName: str) -> None:
        pass

    @abstractmethod
    def setDescription(self, description: str = "") -> None:
        pass

    @abstractmethod
    def invoke(self, ext: ExecExtension = ExecExtension.PY) -> None:
        pass

    @abstractmethod
    def onInitialize(self, host: str = "127.0.0.1", port: int = 6001, instanceID: str = None) -> None:
        pass

    @abstractmethod
    def onEnterState(self, stateName: str = DEFAULT_STATE_NAME, description: str = "") -> None:
        pass

    @abstractmethod
    def onFireEvent(self, eventName: str = DEFAULT_EVENT_NAME, interaction: bool = False, required: bool = True,
                    description: str = "") -> None:
        pass

    @abstractmethod
    def onRequestData(self, dataMIME: ERequestResponseDataMIME, name: str = "", description: str = "") -> Optional[str]:
        pass

    @abstractmethod
    def onResponseData(self, dataMIME: ERequestResponseDataMIME, data: str = "", description: str = "") -> None:
        pass

    @abstractmethod
    def onPostErrorInfo(self, errInfo: str) -> None:
        pass

    @abstractmethod
    def onPostWarningInfo(self, warningInfo: str) -> None:
        pass

    @abstractmethod
    def onPostMessageInfo(self, messageInfo: str) -> None:
        pass

    @abstractmethod
    def onLeaveState(self) -> None:
        pass

    @abstractmethod
    def onFinalize(self) -> None:
        pass

    @abstractmethod
    def onGetModelAssembly(self, methodName: str) -> str:
        pass

    @abstractmethod
    def getMappingLibraryDirectory(self) -> str:
        pass

    @abstractmethod
    def getModelInstanceDirectory(self) -> str:
        pass
