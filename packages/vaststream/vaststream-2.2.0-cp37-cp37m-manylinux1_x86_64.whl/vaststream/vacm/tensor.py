"""
Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
The information contained herein is confidential property of the company.
The user, copying, transfer or disclosure of such information is prohibited
except by express written agreement with VASTAI Technologies Co., Ltd.
"""
# coding: utf-8


from typing import Any, List
from _vaststream_pybind11 import vacm as _vacm
import numpy as np
from .databuffer import DeviceInfo
from .common import *


# =========================== STRUCT =============================
class Shape(_vacm.shape):
    ndims: int
    shapes: List[int]


# =========================== API =============================

def createTensor(devInfo: DeviceInfo, shape: Shape, dType: D_TYPE) -> Any:
    """
    Create a tensor for a device with specific shapes and data type.\n
    ------------\n
    devInfo [in]: Device information for the tensor.\n
    shape [in]: shape of the tensor.\n
    dType [in]: data type of the tensor.\n
    """
    return _vacm.createTensor(devInfo, shape, dType)

def createTensorWithDataHandle(devInfo: DeviceInfo, shape: Shape, dType: D_TYPE, handle: Any, detach: bool) -> Any:
    """
    Create a tensor with data handle for a device with specific shapes and data type.\n
    ------------\n
    devInfo [in]: Device information for the tensor.\n
    shape [in]: shape of the tensor.\n
    dType [in]: data type of the tensor.\n
    handle [in]: a vacmDataHandle with the data handle.\n
    detach [in] whether the handle will be detached or not. If detached, the handle will be released by tensor.\n
    """
    return _vacm.createTensorWithDataHandle(devInfo, shape, dType, handle, detach)

@err_check
def destroyTensor(tensor: Any) -> int:
    """
    Destroy a tensor.\n
    ------------\n
    tensor [in]: the tensor instance.
    """
    return _vacm.destroyTensor(tensor)

def getTensorDataHandle(tensor: Any) -> Any:
    """
    Get the data handle of a tensor.\n
    ------------\n
    tensor [in]: the tensor instance.
    """
    return _vacm.getTensorDataHandle(tensor)

@err_check
def setTensorDataHandle(tensor: Any, handle: Any, detach: bool) -> int:
    """
    Set the data handle for a tensor.\n
    ------------\n
    tensor [in]: the tensor instance.\n
    handle [in]: a vacmDataHandle with the data handle to the tensor.\n
    detach [in] whether the handle will be detached or not. If detached, the handle will be released by tensor.\n
    """
    return _vacm.setTensorDataHandle(tensor, handle, detach)

def getTensorDeviceInfo(tensor: Any) -> DeviceInfo:
    """
    Get the device information of a tensor.\n
    ------------\n
    tensor [in]: the tensor instance.\n
    """
    deviceInfo = _vacm.deviceInfo()
    ret = _vacm.getTensorDeviceInfo(tensor, deviceInfo)
    if ret != _vacm.vacmER_SUCCESS:
        raise Exception(f"getTensorDeviceInfo return error {ret}.")
    return deviceInfo

def getTensorShape(tensor: Any) -> Shape:
    """
    Get the data shape of a tensor.\n
    ------------\n
    tensor [in]: the tensor instance.\n
    """
    shape = _vacm.shape()
    ret = _vacm.getTensorShape(tensor, shape)
    if ret != _vacm.vacmER_SUCCESS:
        raise Exception(f"getTensorShape return error {ret}.")
    return shape

@err_check
def setTensorShape(tensor: Any, shape: Shape) -> int:
    """
    Set the data shape of a tensor.\n
    ------------\n
    tensor [in]: the tensor instance.\n
    shape [in]: a Shape to with the data shape.\n
    """
    return _vacm.setTensorShape(tensor, shape)

def getTensorDataType(tensor: Any) -> D_TYPE:
    """
    Get the data type of a tensor.\n
    ------------\n
    tensor [in]: the tensor instance.\n
    """
    return _vacm.getTensorDataType(tensor)

@err_check
def setTensorDataType(tensor: Any, dType: D_TYPE) -> int:
    """
    Set the data type of a tensor.\n
    ------------\n
    tensor [in]: the tensor instance.\n
    dType [in]: Data type to set.\n
    """
    return _vacm.setTensorDataType(tensor, dType)

def getTensorSize(tensor: Any) -> int:
    """
    Get the size of a tensor.\n
    ------------\n
    tensor [in]: the tensor instance.\n
    """
    return _vacm.getTensorSize(tensor)