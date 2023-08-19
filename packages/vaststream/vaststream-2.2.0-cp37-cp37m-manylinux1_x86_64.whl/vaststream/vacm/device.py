# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

__all__ = ["getDevice", "setDevice", "resetDevice", "getDeviceIdInfo"]

from _vaststream_pybind11 import vacm as _vacm
from typing import List
from .common import *
from .utils import *


def getDevice() -> int:
    """Get current device index.
    
    Returns:
        int: The index of current device.
    """
    return _vacm.getDevice()


@err_check
def setDevice(devIdx: int) -> int:
    """Set the device to be used in the process.
        
    Args:
        devIdx(int): The device index to be set.
    
    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    if devIdx < 0:
        raise RuntimeError("device index must be greater than or equal to 0!")
    return _vacm.setDevice(devIdx)


@err_check
def resetDevice(devIdx: int) -> int:
    """Reset the device used in the process.
        
    Args:
        devIdx(int): The device index to be reset.
    
    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    if devIdx < 0:
        raise RuntimeError("device index must be greater than or equal to 0!")
    return _vacm.resetDevice(devIdx)


def getDeviceIdInfo(devIdx: int) -> List[int]:
    """Get the mapping device index, render device index, video device index in the host.
    
    Args:
        devIdx(int): The device index to be get the mapping device information about host.

    Returns:
        List[int]: The mapping device index, render device index, video device index in the host.
    """
    if devIdx < 0:
        raise RuntimeError("device index must be greater than or equal to 0!")
    return _vacm.getDeviceIdInfo(devIdx)