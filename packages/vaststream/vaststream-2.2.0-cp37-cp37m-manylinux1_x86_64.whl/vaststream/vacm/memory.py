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
class COPY_MEM_TYPE():
    """
    vacm copy memory type.\n
    -----------\n
    @enum CT_COPY_FROM_DEVICE: copy memory from device\n
    @enum CT_COPY_TO_DEVICE: copy memory to device\n
    @enum CT_COPY_DEVICE_TO_DEVICE: copy memory from device to device\n
    """
    CT_COPY_FROM_DEVICE: int = _vacm.copyMemType.vacmCT_COPY_FROM_DEVICE
    CT_COPY_TO_DEVICE: int = _vacm.copyMemType.vacmCT_COPY_TO_DEVICE
    CT_COPY_DEVICE_TO_DEVICE: int = _vacm.copyMemType.vacmCT_COPY_DEVICE_TO_DEVICE


# =========================== API =============================
def mallocDevice(memSize: int) -> Any:
    """
    Allocate memory from device.\n
    ------------\n
    memSize [in]: Size of memory in bytes.\n
    """
    return _vacm.malloc(memSize)

@err_check
def freeDevice(handle: Any) -> int:
    """
    Free a memory in device.\n
    ------------\n
    handle [in]: the data handle with the memory information.\n
    """
    return _vacm.free(handle)

def mallocModelInOut(memSize: int) -> Any:
    """
    Allocate memory for model input or output from device.\n
    ------------\n
    memSize [in]: Size of memory in bytes.\n
    """
    return _vacm.mallocModelInOut(memSize)

@err_check
def freeModelInOut(handle: Any) -> int:
    """
    Free a model input or output memory in device.\n
    ------------\n
    handle [in]: the data handle with the memory information.\n
    """
    return _vacm.freeModelInOut(handle)

@err_check
def memcpy(handleSrc: Any, handleDst: Any, memSize: int, cmType: COPY_MEM_TYPE) -> int:
    """
    Copy a memory between host and device according to copy type. Synchronous interface.\n
    ------------\n
    handleSrc [in]: the data handle with the source memory.\n
    handleDst [in]: the data handle with the destination memory.\n
    memSize [in]: Size of memory in bytes to copy.\n
    cmType [in]: Type of copy.\n
    """
    return _vacm.memcpy(handleSrc, handleDst, memSize, cmType)

# @err_check
# def memcpyAsync(handleSrc: Any, handleDst: Any, memSize: Any, cmType: COPY_MEM_TYPE, evt: Any) -> int:
#     """
#     Copy a memory between host and device according to copy type. Asynchronous interface.\n
#     ------------\n
#     handleSrc [in]: the data handle with the source memory.\n
#     handleDst [in]: the data handle with the destination memory.\n
#     memSize [in]: Size of memory in bytes to copy.\n
#     cmType [in]: Type of copy.\n
#     evt [in]: a vacmEvent object which can be waited for operation to complete.\n
#     """
#     return _vacm.memcpyAsync(handleSrc, handleDst, memSize, cmType, evt)

@err_check
def memcpyDevices(handleSrc: Any, devIdxSrc: int, handleDst: Any, devIdxDst: int, memSize: int) -> int:
    """
    Copy a memory between two devices. Synchronous interface.\n
    ------------\n
    handleSrc [in]: the data handle with the source memory.\n
    devIdxSrc [in]: Device index for the source memory.\n
    handleDst [in]: the data handle with the destination memory.\n
    devIdxDst [in]: Device index for the destination memory.\n
    memSize [in]: Size of memory in bytes to copy.\n
    """
    return _vacm.memcpyDevices(handleSrc, devIdxSrc, handleDst, devIdxDst, memSize)

# @err_check
# def memcpyDevicesAsync(handleSrc: Any, devIdxSrc: int, handleDst: Any, devIdxDst: int, memSize: int, evt: Any) -> int:
#     """
#     Copy a memory between two devices. Asynchronous interface.\n
#     ------------\n
#     handleSrc [in]: the data handle with the source memory.\n
#     devIdxSrc [in]: Device index for the source memory.\n
#     handleDst [in]: the data handle with the destination memory.\n
#     devIdxDst [in]: Device index for the destination memory.\n
#     memSize [in]: Size of memory in bytes to copy.\n
#     evt [in]: a vacmEvent object which can be waited for operation to complete.\n
#     """
#     return _vacm.memcpyDevicesAsync(handleSrc, devIdxSrc, handleDst, devIdxDst, memSize, evt)

# @err_check
# def memset(handle: Any, value: int, count: int) -> int:
#     """
#     Set a memory block with a specific value. Synchronous interface.\n
#     ------------\n
#     handle [in]: the data handle with the memory.\n
#     value [in]: Value to be set.\n
#     count [in]: Count of memory size to be set.\n
#     """
#     return _vacm.memset(handle, value, count)

# @err_check
# def memsetAsync(handle: Any, value: int, count: int, evt: Any) -> int:
#     """
#     Set a memory block with a specific value. Asynchronous interface.\n
#     ------------\n
#     handle [in]: the data handle with the memory.\n
#     value [in]: Value to be set.\n
#     count [in]: Count of memory size to be set.\n
#     evt [in]: a vacmEvent object which can be waited for operation to complete.\n
#     """
#     return _vacm.memsetAsync(handle, value, count, evt)
