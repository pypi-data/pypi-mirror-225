"""
Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
The information contained herein is confidential property of the company.
The user, copying, transfer or disclosure of such information is prohibited
except by express written agreement with VASTAI Technologies Co., Ltd.
"""
# coding: utf-8

from typing import Any
from _vaststream_pybind11 import vacm as _vacm
from .tensor import *
from .common import *

# =========================== ENUM =============================
class DATASET_MODE():
    """
    vacm dataset mode.\n
    ----------\n
    @enum DM_BUFFER: buffer dataset mode.\n
    @enum DM_TENSOR: tensor dataset mode.\n
    """
    DM_BUFFER: int = _vacm.datasetMode.vacmDM_BUFFER
    DM_TENSOR: int = _vacm.datasetMode.vacmDM_TENSOR


# =========================== API =============================
def createDataset(mode: DATASET_MODE) -> Any:
    """
    Create a dataset.\n
    ------------\n
    mode [in]: dataset mode.\n
    """
    return _vacm.createDataset(mode)

@err_check
def destroyDataset(dataset: Any) -> int:
    """
    Destroy a dataset.\n
    ------------\n
    dataset [in]: a dataset instance.\n
    """
    return _vacm.destroyDataset(dataset)

@err_check
def addDatasetBuffer(dataset: Any, buffer: Any) -> int:
    """
    Add a dataset buffer.\n
    ------------\n
    dataset [in]: a dataset instance.\n
    buffer [in]: the data buffer instance to be added.\n 
    """
    return _vacm.addDatasetBuffer(dataset, buffer)

def getDatasetBufferCount(dataset: Any) -> int:
    """
    Get the data buffer count for a dataset.\n
    ------------\n
    dataset [in]: a dataset instance.\n
    """
    return _vacm.getDatasetBufferCount(dataset)

def getDatasetBuffer(dataset: Any, index: int) -> Any:
    """
    Get the data buffer by index for a dataset.\n
    ------------\n
    dataset [in]: a dataset instance.\n
    index [in]: Index of data buffer.\n
    """
    return _vacm.getDatasetBuffer(dataset, index)

@err_check
def addDatasetTensor(dataset: Any, tensor: Any) -> int:
    """
    Add a tensor into a dataset.\n
    ------------\n
    dataset [in]: a dataset instance.\n
    tensor [in]: the tensor instance to be added.\n
    """
    return _vacm.addDatasetTensor(dataset, tensor)

def getDatasetTensorCount(dataset: Any) -> int:
    """
    Get the tensor count for a dataset.\n
    ------------\n
    dataset [in]: a dataset instance.\n
    """
    return _vacm.getDatasetTensorCount(dataset)

def getDatasetTensor(dataset: Any, index: int) -> Any:
    """
    Get the tensor by index for a dataset.\n
    ------------\n
    dataset [in]: a dataset instance.\n
    index [in]: Index of the tensor.\n
    """
    return _vacm.getDatasetTensor(dataset, index)

def getDatasetMode(dataset: Any) -> DATASET_MODE:
    """
    Get the mode for a dataset.\n
    ------------\n
    dataset [in]: a dataset instance.\n
    """
    return _vacm.getDatasetMode(dataset)

def getDatasetUserCtx(dataset: Any) -> Any:
    """
    Get the user context data for a dataset.\n
    ------------\n
    dataset [in]: a dataset instance.\n
    """
    return _vacm.getDatasetUserCtx(dataset)

@err_check
def setDatasetUserCtx(dataset: Any, userCtx: Any) -> int:
    """
    Set the user context data for a dataset.\n
    ------------\n
    dataset [in]: a dataset instance.\n
    userCtx [in]: User defined context data for the dataset.\n
    """
    return _vacm.setDatasetUserCtx(dataset, userCtx)

@err_check
def clearDataset(dataset: Any) -> int:
    """
    Clear a dataset.\n
    ------------\n
    dataset [in]: a dataset instance.\n
    """
    return _vacm.clearDataset(dataset)
