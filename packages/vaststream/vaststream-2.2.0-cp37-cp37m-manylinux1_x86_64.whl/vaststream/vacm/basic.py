"""
Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
The information contained herein is confidential property of the company.
The user, copying, transfer or disclosure of such information is prohibited
except by express written agreement with VASTAI Technologies Co., Ltd.
"""
# coding: utf-8
from _vaststream_pybind11 import vacm as _vacm
from .common import *
"""_summary_
    """


def getVersion() -> str:
    """
    Get the VAME API version information.\n
    ------------\n
    str [out]: The string that represents version.\n
    """
    return _vacm.getVersion()


def getErrDesc(errCode: int) -> str:
    """
    Get the description for an error code.\n
    ------------\n
    errCode [in]: The error code.
    str [out]:description of errCode
    """
    return _vacm.getErrDesc(errCode)
