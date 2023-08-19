# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8
__all__ = [
    "BALANCE_MODE", "MODEL_DATASET_TYPE", "CallBackStatus",
    "WARN_WAIT_MORE_INPUT"
]

from _vaststream_pybind11 import vacl as _vacl

# =========================== ENUM =============================


class BALANCE_MODE():
    """
    An enum that defines balance mode.

    Contains ONCE, RUN.
    """
    ONCE: int = _vacl.balance_mode.vaclBM_ONCE
    RUN: int = _vacl.balance_mode.vaclBM_RUN


class MODEL_DATASET_TYPE():
    """An enum that defines modeldataset type.
    
    Contains INPUT, OUTPUT.
    """
    INPUT: str = "input"
    OUTPUT: str = "output"


# =========================== STRUCT =============================


class CallBackStatus(_vacl.callBackStatus):
    """A struct that defines call back status.

    Attributes:
        errorCode(int): The data contained in the Stream.
        isStreamEnd(bool): The stream's presentation time stamp.
    """
    errorCode: int
    isStreamEnd: bool


# =========================== DEFINE =============================

WARN_WAIT_MORE_INPUT = _vacl.vaclER_WAIT_MORE_INPUT

# =========================== API =============================

# def getVersion() -> str:
#     """Get the VACL API version information.

#     Returns:
#         str: vacl version string.
#     """
#     return _vacl.getVersion()
