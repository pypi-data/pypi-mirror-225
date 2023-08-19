#Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

from _vaststream_pybind11 import vacl as _vacl
from functools import wraps

__all__ = ["err_check"]


# 返回值校验
def err_check(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if ret != _vacl.vaclER_SUCCESS:
            raise RuntimeError(f"{func.__name__} error, ret: {ret}.")
        return ret

    return wrapper
