
"""
Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
The information contained herein is confidential property of the company.
The user, copying, transfer or disclosure of such information is prohibited
except by express written agreement with VASTAI Technologies Co., Ltd.
"""
# coding: utf-8
from typing import Any
from _vaststream_pybind11 import vace

# ================================ API ============================
def readImageFile(imageFile:str, 
                  imageWidth:int, 
                  imageHeight:int,
                  memSize:int) -> Any:
    """
    Read image file to buffer.\n
    """
    return vace.readImageFile(imageFile, imageWidth, imageHeight, memSize)