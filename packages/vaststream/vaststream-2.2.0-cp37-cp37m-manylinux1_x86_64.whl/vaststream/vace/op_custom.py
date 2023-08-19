# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

__all__ = [
    "loadCustomizedOp", "destroyCustomizedOpInfo", "unloadCustomizedOps",
    "getCustomizedOpCount", "getCustomizedOpName", "createCustomizedOp"
]

from _vaststream_pybind11 import vace as _vace
from .common import *
from .utils import *


# =========================== API =============================
def loadCustomizedOp(elfFilePath: str) -> CustomizedOpInfo:
    """Load Elf file which contain one or more customized op informations.and upload all op configs to specificed.

    Args:
        elfFilePath(str):Path of the elf file.
    
    Returns:
        CustomizedOpInfo:An object that contains elf file information.
    """

    return CustomizedOpInfo(_vace.loadCustomizedOp(elfFilePath))


@err_check
def destroyCustomizedOpInfo(opInfo: CustomizedOpInfo) -> int:
    """Release the loaded customized elf information.

    Args:
        opInfo(CustomizedOpInfo):CustomizedOpInfo object, created by loadCustomizedOp.
    
    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    _ptr = opInfo.ptr
    return _vace.destroyCustomizedOpInfo(_ptr)


@err_check
def unloadCustomizedOps(opInfo: CustomizedOpInfo) -> int:
    """Release the loaded customized elf information.

    Args:
        opInfo(CustomizedOpInfo):CustomizedOpInfo object, created by loadCustomizedOp.
    
    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    _ptr = opInfo.ptr
    return _vace.unloadCustomizedOps(_ptr)


def getCustomizedOpCount(opInfo: CustomizedOpInfo) -> int:
    """Get op count from CustomizedOpInfo object.

    Args:
        opInfo(CustomizedOpInfo):CustomizedOpInfo object, created by loadCustomizedOp.
    
    Returns:
        int: output op count.
    """
    _ptr = opInfo.ptr
    return _vace.getCustomizedOpCount(_ptr)


def getCustomizedOpName(opInfo: CustomizedOpInfo, index: int) -> str:
    """Get customized op name.

    Args:
        opInfo(CustomizedOpInfo):CustomizedOpInfo object, created by loadCustomizedOp.
        index(int):Get the op name at the index position.
    Returns:
        str: opname at the index position.
    """
    
    _ptr = opInfo.ptr
    return _vace.getCustomizedOpName(_ptr, index)


def createCustomizedOp(opInfo: CustomizedOpInfo, opname: str) -> Op:
    """Create customzied op based opname from eflInfo.

    Args:
        opInfo(CustomizedOpInfo):CustomizedOpInfo object, created by loadCustomizedOp.
        opname(str):op name in opInfo.
    Returns:
        Op:An object of vaceOp.
    """

    op_info_ptr_ = opInfo.ptr
    op_ptr_ = _vace.createCustomizedOp(op_info_ptr_, opname)
    return Op(op_ptr_)
