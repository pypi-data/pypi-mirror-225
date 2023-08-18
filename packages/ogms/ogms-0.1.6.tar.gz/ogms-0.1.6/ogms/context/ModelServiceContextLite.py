"""
@Description 封装sdk
@Author : 7bin
@Date : 2023/4/13 15:59
"""
import os
import socket
# from sys import exit
import sys
import threading
import time
import uuid
from enum import Enum
from typing import Optional

from IModelServiceContext import IModelServiceContext, ERequestResponseDataMIME, ExecExtension

# 常量
DEFAULT_STATE_NAME = "RUNSTATE"
DEFAULT_EVENT_NAME = "RUNEVENT"
# socket传输的字节大小
SOCKET_MESSAGE_SIZE = 1024
# socket传输的字符最大长度 1024 / 3
SOCKET_MESSAGE_CHAR_SIZE = 300


class EModelContextStatus(Enum):
    EMCS_INIT_BEGIN = 1
    EMCS_INIT = 2
    EMCS_INIT_END = 3

    EMCS_STATE_ENTER_BEGIN = 4
    EMCS_STATE_ENTER = 5
    EMCS_STATE_ENTER_END = 6

    EMCS_EVENT_BEGIN = 7
    EMCS_EVENT = 8
    EMCS_EVENT_END = 9

    EMCS_REQUEST_BEGIN = 10
    EMCS_REQUEST = 11
    EMCS_REQUEST_END = 12

    EMCS_RESPONSE_BEGIN = 13
    EMCS_RESPONSE = 14
    EMCS_RESPONSE_END = 15

    EMCS_POST_BEGIN = 16
    EMCS_POST = 17
    EMCS_POST_END = 18

    EMCS_STATE_LEAVE_BEGIN = 19
    EMCS_STATE_LEAVE = 20
    EMCS_STATE_LEAVE_END = 21

    EMCS_FINALIZE_BEGIN = 22
    EMCS_FINALIZE = 23
    EMCS_FINALIZE_END = 24

    EMCS_UNKNOWN = 0


class ERequestResponseDataFlag(Enum):
    """
    模型执行步骤状态
    """
    FINISH = 1  # 完成
    NOTREADY = 2  # 未完成
    ERROR = 3  # 失败
    UNKNOWN = 4  # 未知状态


class Interaction(Enum):
    """
    是否需要与用户交互，例如是否需要手动输入参数
    """
    TRUE = "true"  # 例如输入数据
    FALSE = "false"  # 例如输出数据


class ModelServiceContext(IModelServiceContext):

    def __init__(self):
        self._mHost = "127.0.0.1"
        self._mPort = 6001
        self._mInstanceID = None
        self._mClientSocket = None
        self._mMornitoringThread = None

        self._modelName = ""
        self._description = ""

        self._mStatus = EModelContextStatus.EMCS_UNKNOWN
        self._mData = ''
        self._mInstanceDir = ''
        self._mCurrentState = ''
        self._mCurrentEvent = ''
        self._mMappingLibDir = ''

        self._mRequestDataFlag = ERequestResponseDataFlag.UNKNOWN
        self._mRequestDataBody = ''
        self._mRequestDataMIME = ERequestResponseDataMIME.UNKNOWN

        self._mResponseDataFlag = ERequestResponseDataFlag.UNKNOWN
        self._mResponseDataBody = ''
        self._mResponseDataMIME = ERequestResponseDataMIME.UNKNOWN

    def _bindSocket(self) -> int:
        self._mClientSocket = socket.socket()
        # self._mHost = "172.21.212.240"  # 获取本地主机名
        # print("_mHost:" + self._mHost)
        try:
            self._mClientSocket.connect((self._mHost, self._mPort))
        except Exception as ex:
            return -1
        return 1

    def setModelName(self, modelName: str) -> None:
        self._modelName = modelName

    def setDescription(self, description: str = "") -> None:
        self._description = description

    def invoke(self, ext: ExecExtension = ExecExtension.PY) -> None:
        cmd = 'ls'
        res = os.popen(cmd)
        output_str = res.read()  # 获得输出字符串
        print(output_str)

    # def onInitialize(self, host: str = "127.0.0.1", port: str = "6001", instanceID: str = str(uuid.uuid4())) -> None:
    def onInitialize(self, host: str = "127.0.0.1", port: int = 6001, instanceID: str = None) -> None:
        # print(os.path.normpath(self._modelName + ".mdl"))
        # if not os.path.exists(os.path.normpath(self._modelName + ".mdl")):
        #     print("please generate mdl: [" + self._modelName + ".mdl] " + "first!")
        #     self.exitWithCodeMinus1()

        # 对读取到的命令行参数做判断
        if len(sys.argv) == 2:
            self._mHost = sys.argv[1]
            self._mInstanceID = str(uuid.uuid4())
        elif len(sys.argv) == 3:
            self._mHost = sys.argv[1]
            self._mPort = int(sys.argv[2])
            self._mInstanceID = str(uuid.uuid4())
        elif len(sys.argv) == 4:
            self._mHost = sys.argv[1]
            self._mPort = int(sys.argv[2])
            self._mInstanceID = sys.argv[3]
        else:
            self._mInstanceID = str(uuid.uuid4())

        # self._mHost = host
        # self._mPort = int(port)
        # self._mInstanceID = instanceID
        # self._mInstanceID = "webstorm"

        if self._bindSocket() == 1:
            # start monitoring thread
            self._mMornitoringThread = threading.Thread(target=ModelServiceContext._Monitoring_thread,
                                                        name='Monitoring',
                                                        args=(self,))
            if self._mMornitoringThread == None:
                print('error in create thread!')
                return self._exitWithCodeMinus1()
            self._mMornitoringThread.start()
            self._sendMessage('{init}' + self._mInstanceID)
            self._wait4Status(EModelContextStatus.EMCS_INIT_END)
            startPos = self._mData.index('[')
            endPos = self._mData.index(']')
            self._mMappingLibDir = self._mData[startPos + 1: endPos]
            self._mData = self._mData[endPos + 1:]
            startPos = self._mData.index('[')
            endPos = self._mData.index(']')
            self._mInstanceDir = self._mData[startPos + 1: endPos]
        else:
            print('Init Failed! Cannot Connect Model Service Container')
            return self._exitWithCodeMinus1()

    def onEnterState(self, stateName: str = DEFAULT_STATE_NAME, description: str = "") -> None:
        self._mStatus = EModelContextStatus.EMCS_STATE_ENTER_BEGIN
        self._mCurrentState = stateName
        self._sendMessage('{onEnterState}' + self._mInstanceID + '&' + stateName)
        self._mStatus = EModelContextStatus.EMCS_STATE_ENTER
        self._wait4Status(EModelContextStatus.EMCS_STATE_ENTER_END)

    def onFireEvent(self, eventName: str = DEFAULT_EVENT_NAME, interaction: bool = False, required: bool = True,
                    description: str = "") -> None:
        self._mStatus = EModelContextStatus.EMCS_EVENT_BEGIN
        self._mCurrentEvent = eventName
        self._sendMessage('{onFireEvent}' + self._mInstanceID + "&" + self._mCurrentState + "&" + eventName)
        self._mStatus = EModelContextStatus.EMCS_EVENT
        self._wait4Status(EModelContextStatus.EMCS_EVENT_END)

    def onRequestData(self, dataMIME: ERequestResponseDataMIME, name: str = "", description: str = "") -> Optional[str]:
        self._resetRequestDataInfo()
        if self._mCurrentState == '' or self._mCurrentEvent == '':
            self._onRequestDataPostProcess(successFlag=False)
            return
        self._mStatus = EModelContextStatus.EMCS_REQUEST_BEGIN
        self._sendMessage('{onRequestData}' + self._mInstanceID + '&' + self._mCurrentState + '&' + self._mCurrentEvent
                          + "&[" + dataMIME.name + "]")
        self._wait4Status(EModelContextStatus.EMCS_REQUEST_END)

        posBegin = self._mData.index('[')
        posEnd = self._mData.index(']')
        dataFlag = self._mData[posBegin + 1: posEnd - posBegin]
        dataRemained = self._mData[posEnd + 1:]

        if dataFlag == ERequestResponseDataFlag.FINISH.name:
            self._mRequestDataFlag = ERequestResponseDataFlag.FINISH
        else:
            self._mRequestDataFlag = ERequestResponseDataFlag.ERROR
            self._mRequestDataMIME = ERequestResponseDataMIME.UNKNOWN
            self._onRequestDataPostProcess(successFlag=False)
            return

        posBegin = dataRemained.index('[')
        posEnd = dataRemained.index(']')
        mime = dataRemained[posBegin + 1: posEnd - posBegin]

        if mime == ERequestResponseDataMIME.TEXT.name:
            self._mRequestDataMIME = ERequestResponseDataMIME.TEXT
        elif mime == ERequestResponseDataMIME.FILE.name:
            self._mRequestDataMIME = ERequestResponseDataMIME.FILE
        else:
            self._mRequestDataMIME = ERequestResponseDataMIME.UNKNOWN

        self._mRequestDataBody = dataRemained[posEnd + 1:]
        return self._onRequestDataPostProcess(dataMIME=dataMIME, successFlag=True)
        # return

    def _onRequestDataPostProcess(self, dataMIME: ERequestResponseDataMIME = ERequestResponseDataMIME.UNKNOWN,
                                  successFlag: bool = True) -> Optional[str]:
        """
        onRequestData 方法的后处理
        Args:
            dataMIME: 数据类型
            successFlag: 数据是否请求成功

        Returns:

        """

        if not successFlag:
            self.onPostErrorInfo("[" + self._mCurrentEvent + "]" + " 流程出错")
            self.onFinalize()
            return

        if self._getRequestDataFlag() == ERequestResponseDataFlag.FINISH:
            if self._getRequestDataMIME() == dataMIME:
                return self._getRequestDataBody()
            else:
                self.onPostErrorInfo("[" + self._mCurrentEvent + "]" + " 参数类型不正确")
                self.onFinalize()
        else:
            self.onFinalize()

    def _onResponseDataPreProcess(self, dataMIME: ERequestResponseDataMIME = ERequestResponseDataMIME.UNKNOWN,
                                  data: str = ""):
        self._setResponseDataFlag(ERequestResponseDataFlag.FINISH)
        self._setResponseDataMIME(dataMIME)
        self._setResponseDataBody(data)

    def onResponseData(self, dataMIME: ERequestResponseDataMIME, data: str = "", description: str = "") -> None:
        # 响应数据前处理
        self._onResponseDataPreProcess(dataMIME, data)

        self._mStatus = EModelContextStatus.EMCS_RESPONSE_BEGIN
        if self._mResponseDataFlag == ERequestResponseDataFlag.FINISH:
            mime = ''
            if self._mResponseDataMIME == ERequestResponseDataMIME.TEXT:
                mime = '[TEXT]'
            elif self._mResponseDataMIME == ERequestResponseDataMIME.FILE:
                mime = '[FILE]'
            else:
                mime = '[UNKNOWN]'

            self._sendMessage(
                '{onResponseData}' + self._mInstanceID + '&' + self._mCurrentState
                + '&' + self._mCurrentEvent + '&' + '[' + ERequestResponseDataFlag.FINISH.name + ']'
                + mime + self._mResponseDataBody)
            self._mStatus = EModelContextStatus.EMCS_RESPONSE
            self._wait4Status(EModelContextStatus.EMCS_RESPONSE_END)
        elif self._mResponseDataFlag == ERequestResponseDataFlag.ERROR:
            self._sendMessage(
                '{onResponseData}' + self._mInstanceID + '&' + self._mCurrentState
                + '&' + self._mCurrentEvent + '&[' + ERequestResponseDataFlag.ERROR.name + ']')
            self._mStatus = EModelContextStatus.EMCS_RESPONSE
            self._wait4Status(EModelContextStatus.EMCS_RESPONSE_END)
        elif self._mResponseDataFlag == ERequestResponseDataFlag.NOTREADY:
            self._sendMessage(
                '{onResponseData}' + self._mInstanceID + '&' + self._mCurrentState
                + '&' + self._mCurrentEvent + '&[' + ERequestResponseDataFlag.NOTREADY.name + ']')
            self._mStatus = EModelContextStatus.EMCS_RESPONSE
            self._wait4Status(EModelContextStatus.EMCS_RESPONSE_END)

        self._resetResponseDataInfo()

    def onPostErrorInfo(self, errInfo: str) -> None:
        self._mStatus = EModelContextStatus.EMCS_POST_BEGIN
        self._sendMessage('{onPostErrorInfo}' + self._mInstanceID + '&' + errInfo)
        self._mStatus = EModelContextStatus.EMCS_POST
        self._wait4Status(EModelContextStatus.EMCS_POST_END)
        self._exitWithCodeMinus1()

    def onPostWarningInfo(self, warningInfo: str) -> None:
        self._mStatus = EModelContextStatus.EMCS_POST_BEGIN
        self._sendMessage('{onPostWarningInfo}' + self._mInstanceID + '&' + warningInfo)
        self._mStatus = EModelContextStatus.EMCS_POST
        self._wait4Status(EModelContextStatus.EMCS_POST_END)

    def onPostMessageInfo(self, messageInfo: str) -> None:
        self._mStatus = EModelContextStatus.EMCS_POST_BEGIN
        self._sendMessage('{onPostMessageInfo}' + self._mInstanceID + '&' + messageInfo)
        self._mStatus = EModelContextStatus.EMCS_POST
        self._wait4Status(EModelContextStatus.EMCS_POST_END)

    def onLeaveState(self) -> None:
        self._mStatus = EModelContextStatus.EMCS_STATE_LEAVE_BEGIN
        self._sendMessage('{onLeaveState}' + self._mInstanceID + '&' + self._mCurrentState)
        self._mStatus = EModelContextStatus.EMCS_STATE_LEAVE
        self._wait4Status(EModelContextStatus.EMCS_STATE_LEAVE_END)

    def onFinalize(self) -> None:
        self._mStatus = EModelContextStatus.EMCS_FINALIZE_BEGIN
        self._sendMessage('{onFinalize}' + self._mInstanceID)
        self._mStatus = EModelContextStatus.EMCS_FINALIZE
        self._wait4Status(EModelContextStatus.EMCS_FINALIZE_END)
        # self._mMornitoringThread.join()
        # self.exitProgram()

    def onGetModelAssembly(self, methodName: str) -> str:
        pass

    def getMappingLibraryDirectory(self) -> str:
        # if self._mMappingLibDir[:-1] != '\\':
        #     self._mMappingLibDir = self._mMappingLibDir + '\\'
        return self._mMappingLibDir

    def getModelInstanceDirectory(self) -> str:
        # if self._mInstanceDir[:-1] != '\\':
        #     self._mInstanceDir = self._mInstanceDir + '\\'
        return self._mInstanceDir

    def _sendMessage(self, message: str) -> None:
        # 超过 SOCKET_MESSAGE_CHAR_SIZE 的部分转化为 ...
        trim_str = message[:SOCKET_MESSAGE_CHAR_SIZE] + (message[SOCKET_MESSAGE_CHAR_SIZE:] and '...')
        self._mClientSocket.sendall(bytes(trim_str, encoding="utf-8"))

    def _receiveMessage(self) -> str:
        try:
            msg = str(self._mClientSocket.recv(SOCKET_MESSAGE_SIZE), encoding="utf-8")
            return msg
        except Exception as ex:
            if "关闭" in str(ex):
                print("远程主机强迫关闭了一个现有的连接")
                # 远程链接断了强制退出脚本
                self._exitWithCodeMinus1()
                # return sys.exit()
            else:
                print(ex)

    def _wait4Status(self, status: EModelContextStatus, timeout=72000) -> int:
        time_end = time.time() + timeout
        # MODIFY BY 7BIN
        while True:
            time.sleep(1)
            if self._mStatus == status:
                return 1
            elif time.time() > time_end:
                self._exitWithCodeMinus1()
                # return sys.exit()

        # return -1
        # os._exit(0)

    def _resetRequestDataInfo(self) -> None:
        self._mRequestDataBody = ''
        self._mRequestDataFlag = ERequestResponseDataFlag.UNKNOWN
        self._mRequestDataMIME = ERequestResponseDataMIME.UNKNOWN

    def _resetResponseDataInfo(self) -> None:
        self._mRequestDataBody = ''
        self._mRequestDataFlag = ERequestResponseDataFlag.UNKNOWN
        self._mRequestDataMIME = ERequestResponseDataMIME.UNKNOWN

    def _getRequestDataFlag(self) -> ERequestResponseDataFlag:
        return self._mRequestDataFlag

    def _getRequestDataMIME(self) -> ERequestResponseDataMIME:
        return self._mRequestDataMIME

    def _getRequestDataBody(self) -> str:
        return self._mRequestDataBody

    def _setResponseDataFlag(self, flag: ERequestResponseDataFlag) -> None:
        self._mResponseDataFlag = flag

    def _setResponseDataMIME(self, MIME: ERequestResponseDataMIME) -> None:
        self._mResponseDataMIME = MIME

    def _setResponseDataBody(self, body: str) -> None:
        self._mResponseDataBody = body

    def _getResponseDataFlag(self) -> ERequestResponseDataFlag:
        return self._mResponseDataFlag

    def _getResponseDataMIME(self) -> ERequestResponseDataMIME:
        return self._mResponseDataMIME

    def _getResponseDataDody(self) -> str:
        return self._mResponseDataBody

    def _getCurrentStatus(self) -> EModelContextStatus:
        return self._mStatus

    # @staticmethod
    def _Monitoring_thread(self):
        # print("Monitoring_thread")
        # time_end = time.time() + 5
        while True:
            data = self._receiveMessage()
            # print("_receiveMessage: " + data)
            if data == "":
                print('Unknown Command!')
                pass
            header = data[data.index('{'): data.index('}') + 1]
            self._mData = data[data.index('}') + 1:]
            if header == '{Initialized}':
                self._mStatus = EModelContextStatus.EMCS_INIT_END
            elif header == '{Enter State Notified}':
                self._mStatus = EModelContextStatus.EMCS_STATE_ENTER_END
            elif header == '{Fire Event Notified}':
                self._mStatus = EModelContextStatus.EMCS_EVENT_END
            elif header == '{Request Data Notified}':
                self._mStatus = EModelContextStatus.EMCS_REQUEST_END
            elif header == '{Response Data Notified}':
                self._mStatus = EModelContextStatus.EMCS_RESPONSE_END
            elif header == '{Response Data Received}':
                self._mStatus = EModelContextStatus.EMCS_RESPONSE_END
            elif header == '{Post Error Info Notified}':
                self._mStatus = EModelContextStatus.EMCS_POST_END
            elif header == '{Post Warning Info Notified}':
                self._mStatus = EModelContextStatus.EMCS_POST_END
            elif header == '{Post Message Info Notified}':
                self._mStatus = EModelContextStatus.EMCS_POST_END
            elif header == '{Leave State Notified}':
                self._mStatus = EModelContextStatus.EMCS_STATE_LEAVE_END
            elif header == '{Finalize Notified}':
                self._mStatus = EModelContextStatus.EMCS_FINALIZE_END
                return
            elif header == '{kill}':
                print("{kill} : " + self._mData)
                self._exitWithCodeMinus1()
                # sys.exit()

            else:
                print('Unknown Command!')
                pass

    def _exitWithCodeMinus1(self):
        os._exit(-1)
