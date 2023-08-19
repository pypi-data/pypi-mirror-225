"""
Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
The information contained herein is confidential property of the company.
The user, copying, transfer or disclosure of such information is prohibited
except by express written agreement with VASTAI Technologies Co., Ltd.
"""
# coding: utf-8
from _vaststream_pybind11 import vacm as _vacm
from .common import *
from typing import Optional


@err_check
def initialize(config: Optional[str] = None) -> int:
    """
    Initialize the environment for VACM API. This is the first API need to call.\n
    ----------\n
    config [in]: Config file will be loaded for initialization. If NULL, default config will be used.\n
    """
    return _vacm.initialize(config)


@err_check
def uninitialize() -> int:
    """
    Release the environment for VACM API. This is the last API need to call.\n
    """
    return _vacm.uninitialize()
