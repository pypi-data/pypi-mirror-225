# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8
__all__ = ["err_check"]

import ctypes
from _vaststream_pybind11 import vacm as _vacm
from functools import wraps


def err_check(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if ret != _vacm.ER_SUCCESS:
            raise RuntimeError(f"{func.__name__} error, ret: {ret}.")
        return ret

    return wrapper


def convert_capsule_to_int(capsule):
    """Get the memory pointing of capsule instance,
        note that is not the memory address of the instance itself.
       
    Args:
        capsule: The PyCapsule object.
    
    Returns:
        The c_void_p object.
    """
    ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
    ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [
        ctypes.py_object, ctypes.c_char_p
    ]
    return ctypes.pythonapi.PyCapsule_GetPointer(capsule, None)