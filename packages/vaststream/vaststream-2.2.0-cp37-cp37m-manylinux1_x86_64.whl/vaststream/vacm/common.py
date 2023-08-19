# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

__all__ = [
    "D_TYPE", "DEVICE_TYPE", "DATASET_MODE", "COPY_MEM_TYPE", "LOG_CHANNEL",
    "LOG_LEVEL", "Context", "PointerContainer", "Shape", "DeviceInfo",
    "SUCCESS", "NOT_IMPLEMENT", "initialize", "uninitialize", "getErrDesc",
    "initLogger", "logMessage"
]

from _vaststream_pybind11 import vacm as _vacm
from typing import List, Any
from .utils import convert_capsule_to_int, err_check

# =========================== ENUM =============================


class D_TYPE():
    """An enum that defines data type.
    
    Contains UINT8, INT8, UINT16, INT16, UINT32, INT32, FLOAT16, FLOAT32, 
    BFLOAT, ANY.
    """
    UINT8: int = _vacm.dType.vacmDT_UINT8
    INT8: int = _vacm.dType.vacmDT_INT8
    UINT16: int = _vacm.dType.vacmDT_UINT16
    INT16: int = _vacm.dType.vacmDT_INT16
    UINT32: int = _vacm.dType.vacmDT_UINT32
    INT32: int = _vacm.dType.vacmDT_INT32
    FLOAT16: int = _vacm.dType.vacmDT_FLOAT16
    FLOAT32: int = _vacm.dType.vacmDT_FLOAT32
    BFLOAT: int = _vacm.dType.vacmDT_BFLOAT
    ANY: int = _vacm.dType.vacmDT_ANY


class DEVICE_TYPE():
    """An enum that defines device type.
    
    Contains CPU, VACC.
    """
    CPU: int = _vacm.deviceType.vacmDE_CPU
    VACC: int = _vacm.deviceType.vacmDE_VACC


class DATASET_MODE():
    """An enum that defines dataset mode.
    
    Contains BUFFER, TENSOR.
    """
    BUFFER: int = _vacm.datasetMode.vacmDM_BUFFER
    TENSOR: int = _vacm.datasetMode.vacmDM_TENSOR


class COPY_MEM_TYPE():
    """An enum that defines copy memory type.
    
    Contains FROM_DEVICE, TO_DEVICE, DEVICE_TO_DEVICE
    """
    FROM_DEVICE: int = _vacm.copyMemType.vacmCT_COPY_FROM_DEVICE
    TO_DEVICE: int = _vacm.copyMemType.vacmCT_COPY_TO_DEVICE
    DEVICE_TO_DEVICE: int = _vacm.copyMemType.vacmCT_COPY_DEVICE_TO_DEVICE


class LOG_CHANNEL():
    """An enum that defines log channel of different library.
    
    Contains APP, CM, CE, CL, ME, ML, RT, NN, TM.
    """
    APP: int = _vacm.logChannel.vacmLC_APP
    CM: int = _vacm.logChannel.vacmLC_CM
    CE: int = _vacm.logChannel.vacmLC_CE
    CL: int = _vacm.logChannel.vacmLC_CL
    ME: int = _vacm.logChannel.vacmLC_ME
    ML: int = _vacm.logChannel.vacmLC_ML
    RT: int = _vacm.logChannel.vacmLC_RT
    NN: int = _vacm.logChannel.vacmLC_NN
    TM: int = _vacm.logChannel.vacmLC_TM


class LOG_LEVEL():
    """An enum that defines log level.
    
    Contains TRACE, DEBUG, INFO, WARN, ERROR, ALARM, FATAL.
    """
    TRACE: int = _vacm.logLevel.vacmLL_TRACE
    DEBUG: int = _vacm.logLevel.vacmLL_DEBUG
    INFO: int = _vacm.logLevel.vacmLL_INFO
    WARN: int = _vacm.logLevel.vacmLL_WARN
    ERROR: int = _vacm.logLevel.vacmLL_ERROR
    ALARM: int = _vacm.logLevel.vacmLL_ALARM
    FATAL: int = _vacm.logLevel.vacmLL_FATAL


# =========================== STRUCT =============================


class DeviceInfo(_vacm.deviceInfo):
    """A struct that defines device information.
    
    Attributes:
        deviceType(DEVICE_TYPE): The device type, includes host and device.
        deviceIdx(int): The index of device.
    """
    deviceType: DEVICE_TYPE
    deviceIdx: int


class Shape(_vacm.shape):
    """A struct that defines the shape of tensor.
    
    Attributes:
        ndims(int): The dims of the tensor.
        shapes(List[int]): The size of each dim.
    """
    ndims: int
    shapes: List[int]


class PointerContainer():
    """
    Pointer Container
    """

    def __init__(self, _ptr: Any = None):
        self._ptr = _ptr

    def __eq__(self, other) -> bool:
        if isinstance(other, PointerContainer):
            return self.id == other.id
        return False

    @property
    def id(self):
        assert self.ptr != None
        return convert_capsule_to_int(self.ptr)

    @property
    def ptr(self):
        return self._ptr


class Context(PointerContainer):
    """
    Context Container
    """
    pass


# =========================== DEFINE =============================
SUCCESS = _vacm.ER_SUCCESS
NOT_IMPLEMENT = _vacm.ER_NOT_IMPLEMENT


# =========================== API =============================
@err_check
def initialize() -> int:
    """Initialize the vacm system.
    
    Hint:
        Please initialize before using vacm.
    
    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vacm.initialize()


@err_check
def uninitialize() -> int:
    """Uninitialize the vacm system.
    
    Hint:
        Please uninitialize after using vacm.
    
    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vacm.uninitialize()


# def getVersion() -> str:
#     """Get the VACM API version information.

#     Returns:
#         str: vacm version string.
#     """
#     return _vacm.getVersion()


def getErrDesc(errCode: int) -> str:
    """Get the description for an error code.
    
    Args:
        errCode(int): The error code.
    
    Returns:
        str: The description of error code.
    """
    return _vacm.getErrDesc(errCode)


@err_check
def initLogger() -> int:
    """Initialize logger system for message logging.
    
    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vacm.initLogger()


@err_check
def logMessage(logChannel: LOG_CHANNEL, logLevel: LOG_LEVEL, fmt: str) -> int:
    """Write a message to the log file.
    
    Args:
        logChannel(LOG_CHANNEL): The log channel of different library.
        logLevel(LOG_LEVEL): The log level of log message.
        fmt(str): The string format.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vacm.logMessage(logChannel, logLevel, fmt)
