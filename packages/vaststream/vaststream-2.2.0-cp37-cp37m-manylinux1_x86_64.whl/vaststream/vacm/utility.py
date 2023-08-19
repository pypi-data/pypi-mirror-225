"""
Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
The information contained herein is confidential property of the compAny.
The user, copying, transfer or disclosure of such information is prohibited
except by express written agreement with VASTAI Technologies Co., Ltd.
"""
# coding: utf-8
from typing import List, Any
from _vaststream_pybind11 import vacm as _vacm
from .common import *


def getDataTypeSize(dType: D_TYPE) -> int:
    """
    Get the size for a data type .\n
    ----------\n
    dType [in]: Data type.\n
    size [out]: Pointer to a uint32_t to receive the size for the data type.\n
    """
    return _vacm.getDataTypeSize(dType)


def float16ToFloat32(valIn: int) -> float:
    """
    Convert a float16 number to float32 number .\n
    ----------\n
    valIn [in]: The float16 number.\n
    [out]: Pointer to a Float32 to receive the float32 value.\n
    """
    return _vacm.float16ToFloat32(valIn)


def float32ToFloat16(valIn: float) -> int:
    """
    Convert a float32 number to float16 number .\n
    ----------\n
    valIn [in]: The float32 number.\n
    valOut [out]: Pointer to a Float16 to receive the float16 value.\n
    """
    return _vacm.float32ToFloat16(valIn)


def float16ToFloat32Array(array: List[float]) -> List[float]:
    """
    Convert an array of float16 number to the array of float32 number .\n
    ----------\n
    valIn [in]: The array of float16 number.\n
    valOut [out]: Pointer to a Float32 array to receive the array of float32 value. The count of
                  this array must be equal or larger than count.\n
    """
    return _vacm.float16ToFloat32Array(array)


def float32ToFloat16Array(array: List[float]) -> List[float]:
    """
    Convert an array of float32 number to the array of float16 number .\n
    ----------\n
    valIn [in]: The array of float32 number.\n
    valOut [out]: Pointer to a Float16 array to receive the array of float16 value. The count of
                       this array must be equal or larger than count..\n
    """
    return _vacm.float32ToFloat16Array(array)

def getFloat16Array(handle: Any, outputSize: int) -> List[float]:
    """
    get the array of float16 number \n
    ----------\n
    handle [in]: the head address of a contiguous memory.\n
    outputSize [in]: the bytes size of the contiguous memory.\n
    """
    return _vacm.getFloat16Array(handle, outputSize)

@err_check
def destroyDatasetAll(dataset: Any) -> int:
    """
    Destroy all data in a dataset including itself. .\n
    ----------\n
    dataset [in]: Pointer to a dataset instance.\n
    """
    return _vacm.destroyDatasetAll(dataset)


def mallocHost(memSize: int) -> Any:
    """
    Allocate memory from host.\n
    ----------\n
    memSize [in]: Size of memory in bytes.\n
    handle [out]: Pointer to the address of data handle to receive the memory address.
    """
    return _vacm.mallocHost(memSize)


@err_check
def freeHost(handle: Any) -> int:
    """
    Free a memory in host.\n
    ----------\n
    handle [in]: data handle with the memory information.\n
    """
    return _vacm.freeHost(handle)



#工具函数
def getFloat32Array(handle: Any, outputSize: int) -> List[float]:
    """
    get the array of float32 number \n
    ----------\n
    handle [in]: the head address of a contiguous memory.\n
    outputSize [in]: the bytes size of the contiguous memory.\n
    """
    float16Array = getFloat16Array(handle, outputSize)
    return float16ToFloat32Array(float16Array)