# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

__all__ = [
    "createOp", "destroyOp", "setOpAttr", "setOpAttrArray", "getOpAttr",
    "getOpAttrArray", "executeOp"
]

from _vaststream_pybind11 import vace as _vace
from typing import Union
from .common import *
from .utils import *
from vaststream.vacm.data import Dataset


# =========================== API =============================
def createOp(opType: OP_TYPE) -> Op:
    """Create a vace Op instance.
    
    Args:
        opType(OP_TYPE): Type of operator
        
    Return: 
        Op: vace Op instance.
    """
    ptr_ = _vace.createOp(opType)
    return Op(ptr_)


@err_check
def destroyOp(op: Op) -> int:
    """Destroy a vaceOp instance.
    
    Args:
        op: Vace Op instance, create by API createOp.
        
    Return:
        int: The return code. 0 for success, False otherwise.
    """
    ptr_ = op.ptr
    return _vace.destroyOp(ptr_)


@err_check
def setOpAttr(op: Op, attrName: str, attrDType: DATA_TYPE,
              attrGType: PARAM_TYPE, value: Union[int, float]) -> int:
    """Set attributes of a specified op.

    Args:
        op(Op): The specified vace op, create by API createOp.
        attrName(str): The attribute name.
        attrDType(DATA_TYPE): Data type of attribute.
        attrGType(PARAM_TYPE): The attribute type (PARAM_ELEMENT | PARAM_ARRAY).
        value(Union[int, float]): The value of attribute.
    
    Return:
        int: The return code. 0 for success, False otherwise.
    """
    ptr_ = op.ptr
    return _vace.setVaceOPAttr(ptr_, attrName, attrDType, attrGType, value)


@err_check
def setOpAttrArray(op: Op, attrName: str, attrDType: DATA_TYPE,
                   attrGType: PARAM_TYPE, value: Union[int, float],
                   index: int) -> int:
    """Set attributes of a specified op.
    
    Args:
        op(Op): The specified vace op, create by API createOp.
        attrName(str) : The attribute name.
        attrDType(DATA_TYPE): Data type of attribute.
        attrGType(PARAM_TYPE): the attribute type (PARAM_ELEMENT | PARAM_ARRAY).
        value(Union[int, float]): the value of attribute.
        index(int): The index of array element.
        
    Return:
        int: The return code. 0 for success, False otherwise.
    """
    _ptr = op.ptr
    return _vace.setVaceOPAttrArray(_ptr, attrName, attrDType, attrGType,
                                    value, index)


def getOpAttr(op: Op, attrName: str,
              attrDType: DATA_TYPE) -> Union[int, float]:
    """Get attributes of a specified op.
    
    Args:
        opPy(Op): The specified vace op, create by API createOp.
        attrName(str): The attribute name.
        attrDType(DATA_TYPE): Data type of attribute.
    
    Return:
        Union[int, float]: The attribute value of the op.
    """
    if attrDType == DATA_TYPE.INT:
        return _vace.getVaceOPAttrInt(op.ptr, attrName, attrDType)

    elif attrDType == DATA_TYPE.UINT_8:
        return _vace.getVaceOPAttrUint8(op.ptr, attrName, attrDType)

    # elif attrDType == DATA_TYPE.UINT_16:
    #     return _vace.getVaceOPAttrUint16(op.ptr, attrName, attrDType)

    # elif attrDType == DATA_TYPE.UINT_32:
    #     return _vace.getVaceOPAttrUint32(op.ptr, attrName, attrDType)

    # elif attrDType == DATA_TYPE.UINT_64:
    #     return _vace.getVaceOPAttrUint64(op.ptr, attrName, attrDType)

    elif attrDType == DATA_TYPE.FLOAT:
        return _vace.getVaceOPAttrFloat(op.ptr, attrName, attrDType)

    # elif attrDType == DATA_TYPE.DOUBLE:
    #     return _vace.getVaceOPAttrDouble(op.ptr, attrName, attrDType)
    else:
        raise RuntimeError(f"Not support format: {attrDType}.")


def getOpAttrArray(op: Op, attrName: str, attrDType: DATA_TYPE,
                   index: int) -> Union[int, float]:
    """Get attributes of a specified op.
    
    Args:
        op(Op): The specified vace op, create by API createOp.
        attrName(str): The attribute name.
        attrDType(str): Data type of attribute.
        attrGType(PARAM_TYPE): the attribute type (PARAM_ELEMENT | PARAM_ARRAY).
        index(int): The index of array element.

    Return: 
        Union[int, float]: The attribute value of the op.
    """
    if attrDType == DATA_TYPE.INT:
        return _vace.getVaceOPAttrArrayInt(op.ptr, attrName, attrDType, index)

    elif attrDType == DATA_TYPE.UINT_8:
        return _vace.getVaceOPAttrArrayUint8(op.ptr, attrName, attrDType,
                                             index)

    # elif attrDType == DATA_TYPE.UINT_16:
    #     return _vace.getVaceOPAttrArrayUint16(op.ptr, attrName, attrDType, index)

    # elif attrDType == DATA_TYPE.UINT_32:
    #     return _vace.getVaceOPAttrArrayUint32(op.ptr, attrName, attrDType, index)

    # elif attrDType == DATA_TYPE.UINT_64:
    #     return _vace.getVaceOPAttrArrayUint64(op.ptr, attrName, attrDType, index)

    elif attrDType == DATA_TYPE.FLOAT:
        return _vace.getVaceOPAttrArrayFloat(op.ptr, attrName, attrDType,
                                             index)

    # elif attrDType == DATA_TYPE.DOUBLE:
    #     return _vace.getVaceOPAttrArrayDouble(op.ptr, attrName, attrDType, index)

    else:
        raise RuntimeError(f"Not support format: {attrDType}.")


@err_check
def executeOp(op: Op, input: Dataset, output: Dataset) -> int:
    """ExecuteOp op with input dataset.
    
    Args:
        op(Op): The specified vace op, create by API createOp.
        input(Dataset): The vacmDataset of input data.
        output(Dataset): The vacmDataset of output data.
    Return:
        int: The return code. 0 for success, False otherwise.
    """
    return _vace.executeOp(op.ptr, input.ptr, output.ptr)
