# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

__all__ = [
    "YuvNv12Shape", "CustomCfgExample", "setCustomizedOpConfigExample",
    "setCustomizedOpCfgCallbackExample"
]

from _vaststream_pybind11 import vace as _vace
from typing import List
from .common import *
from .utils import *


# =========================== CUSTOM DEFINE STRUCT =============================
class YuvNv12Shape(_vace.yuvNv12Shape):
    height: int
    width: int
    h_pitch: int
    w_pitch: int


class CustomCfgExample(_vace.customCfgExample):
    iimage_shape: YuvNv12Shape
    oimage_shape: List[YuvNv12Shape]
    scale: float


# =========================== CUSTOM DEFINE API =============================
def setCustomizedOpConfigExample(op: Op, config: CustomCfgExample) -> int:
    """
    setCustomizedOpConfigExample.\n
    ----------\n
    op [in]: customized op to set config\n
    config [in]: customized config.\n
    """
    ptr_ = op.ptr
    return _vace.setCustomizedOpConfigExample(ptr_, config)


def setCustomizedOpCfgCallbackExample(op: Op) -> int:
    """
    setCustomizedOpCfgCallbackExample.\n
    ----------\n
    op [in]: customized op to set callback function.\n
    """
    ptr_ = op.ptr
    return _vace.setCustomizedOpCfgCallbackExample(ptr_)