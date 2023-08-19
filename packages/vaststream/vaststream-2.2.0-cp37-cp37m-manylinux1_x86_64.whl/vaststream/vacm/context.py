# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8
__all__ = [
    "createContext", "destroyContext", "setCurrentContext", "getCurrentContext"
]

from _vaststream_pybind11 import vacm as _vacm
from .common import *
from .utils import *


def createContext(devIdx: int) -> Context:
    """Create a context in assigned device.
    
    Args:
        devIdx(int): The device index in which the context will be created.
        
    Returns:
        Context: The context object in assigned device.
    """
    if devIdx < 0:
        raise RuntimeError("device index must be greater than or equal to 0!")
    return Context(_vacm.createContext(devIdx))


@err_check
def destroyContext(ctx: Context) -> int:
    """Destroy the context in the device.
    
    Args:
        ctx(Context): The context object waited to be destroyed. 
    
    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vacm.destroyContext(ctx.ptr)


@err_check
def setCurrentContext(ctx: Context) -> int:
    """Set the context for the current calling thread.
    
    Args:
        ctx(Context): The context object waited to be set in the current thread.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vacm.setCurrentContext(ctx.ptr)


def getCurrentContext() -> Context:
    """Get the context for the current calling thread.
    
    Returns:
        Context: The context object.
    """
    return Context(_vacm.getCurrentContext())
