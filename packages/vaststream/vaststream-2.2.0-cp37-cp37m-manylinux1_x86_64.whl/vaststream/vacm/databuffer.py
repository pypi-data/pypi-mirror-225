"""
Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
The information contained herein is confidential property of the company.
The user, copying, transfer or disclosure of such information is prohibited
except by express written agreement with VASTAI Technologies Co., Ltd.
"""
# coding: utf-8

from typing import Any
from _vaststream_pybind11 import vacm as _vacm
from .common import *


# =========================== ENUM =============================
class DEVICE_TYPE():
    """
    vacm device type.\n
    ----------\n
    @enum DE_CPU: in CPU.\n
    @enum DE_VACC: in VACC\n
    """
    DE_CPU: int = _vacm.deviceType.vacmDE_CPU
    DE_VACC: int = _vacm.deviceType.vacmDE_VACC

# =========================== STRUCT =============================

class DeviceInfo(_vacm.deviceInfo):
    """
    device information
    """
    deviceType: DEVICE_TYPE
    deviceIdx: int

# =========================== API =============================
def createDataBuffer(devInfo: DeviceInfo, handle: Any, size: int) -> Any:
    """
    Create a data buffer.\n
    ------------\n
    devInfo [in]: device information.\n
    handle [in]: handle of data buffer.\n
    size [in]: buffer size.\n
    """
    return _vacm.createDataBuffer(devInfo, handle, size)

def createDataBufferFromContext(devType: DEVICE_TYPE, handle: Any, size: int) -> Any:
    """
    Create a data buffer from device context.\n
    ------------\n
    devType [in]: device type.\n
    handle [in]: handle of data buffer.\n
    size [in]: buffer size.\n
    """
    return _vacm.createDataBufferFromContext(devType, handle, size)

@err_check
def destroyDataBuffer(buffer: Any) -> int:
    """
    Destroy a data buffer.\n
    ------------\n
    buffer [in]: data buffer.\n
    """
    return _vacm.destroyDataBuffer(buffer)

def getDataBufferAddr(buffer: Any) -> Any:
    """
    Get the buffer address for a data buffer.\n
    ------------\n
    buffer [in]: data buffer.\n
    """ 
    return _vacm.getDataBufferAddr(buffer)

def getDataBufferSize(buffer: Any) -> int:
    """
    Get the buffer size for a data buffer.\n
    ------------\n
    buffer [in]: data buffer.\n
    """ 
    return _vacm.getDataBufferSize(buffer)

def getDataBufferDeviceInfo(buffer: Any) -> DeviceInfo:
    """
    Get the device information for a data buffer.\n
    ------------\n
    buffer [in]: data buffer.\n
    """ 
    deviceInfo = _vacm.deviceInfo()
    ret = _vacm.getDataBufferDeviceInfo(buffer, deviceInfo)
    if ret != _vacm.vacmER_SUCCESS:
        raise Exception(f"getDataBufferDeviceInfo return error {ret}.")
    return deviceInfo

@err_check
def updateDataBuffer(buffer: Any, devInfo: DeviceInfo, handle: Any, size: int) -> int:
    """
    Update a data buffer.\n
    ------------\n
    buffer [in]: data buffer.\n
    devInfo [in]: device information.\n
    handle [in]: handle of data buffer.\n
    size [in]: data buffer size.\n
    """ 
    return _vacm.updateDataBuffer(buffer, devInfo, handle, size)