# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

__all__ = [
    "DataHandle", "DataBuffer", "Tensor", "Dataset", "mallocHost", "freeHost",
    "mallocDevice", "freeDevice", "mallocModelInOut", "freeModelInOut",
    "memcpy", "getNumpyFromHandle", "getHandleFromNumpy", "createDataBuffer",
    "destroyDataBuffer", "getDataBufferAddr", "getDataBufferSize",
    "getDataBufferDeviceInfo", "updateDataBuffer", "createTensor",
    "destroyTensor", "getTensorDataHandle", "getTensorDeviceInfo",
    "getTensorShape", "getTensorDataType", "getTensorSize", "createDataset",
    "destroyDataset", "addDatasetBuffer", "getDatasetBufferCount",
    "getDatasetBuffer", "addDatasetTensor", "getDatasetTensorCount",
    "getDatasetTensor", "getDatasetMode", "getDatasetUserCtx",
    "setDatasetUserCtx", "clearDataset", "destroyDatasetAll",
    "getDataTypeSize", "getFloatArrayFromHandle"
]

from _vaststream_pybind11 import vacm as _vacm
import numpy as np
from typing import List, Union, Any
from .common import *
from .device import getDevice
from .utils import *


class DataHandle(PointerContainer):
    """DataHandle Container.

    Args:
        size(int): The size of the data handle.
        devType(DEVICE_TYPE): The device type of the data handle.
        ptr(Any): The handle pointer if you have held it.
    
    """
    def __init__(self,
                 size: int,
                 devType: DEVICE_TYPE = DEVICE_TYPE.CPU,
                 ptr=None):
        assert size >= 0, f"The size {size} of the handle should be >= 0."
        # if size == 0 : print(f'[warn]: size of the handle is {size}')        
        self.devInfo = DeviceInfo()
        if devType == DEVICE_TYPE.VACC:
            deviceIdx = getDevice()
            self.devInfo.deviceIdx = deviceIdx
        else:
            self.devInfo.deviceIdx = 0
        self.devInfo.deviceType = devType
        self._size = size
        self._ptr = ptr
        self.create()

    def _check_destroy(self):
        assert self._ptr is not None, "The handle has been destroyed."

    @property
    def devType(self) -> DEVICE_TYPE:
        """The devType of the data handle."""
        self._check_destroy()
        return self.devInfo.deviceType

    @property
    def devId(self) -> int:
        """The devId of the data handle."""
        self._check_destroy()
        return self.devInfo.deviceIdx

    @property
    def size(self) -> int:
        """The size of the data handle."""
        if self._size != 0:
            self._check_destroy()
        return self._size

    @property
    def isAlive(self) -> bool:
        """The live state of the daya handle."""
        return self.ptr is not None

    def create(self) -> None:
        """Create DataHandle."""
        if self._size == 0:
            self._ptr = None
            return
        if self._ptr is None:
            if self.devInfo.deviceType == DEVICE_TYPE.CPU:
                self._ptr = _vacm.mallocHost(self._size)
            else:
                self._ptr = _vacm.malloc(self._size)

    @err_check
    def destroy(self) -> int:
        """Destroy DataHandle."""
        ret = _vacm.ER_SUCCESS
        if self._ptr is not None:
            if self.devType == DEVICE_TYPE.CPU:
                ret = _vacm.freeHost(self.ptr)
            else:
                ret = _vacm.free(self.ptr)
            self._ptr = None
        return ret

    @err_check
    def copyTo(self, handle) -> int:
        """Copy handle mem to another handle.

        Args:
            handle(DataHandle): The dst handle.
        
        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        self._check_destroy()
        assert isinstance(handle, DataHandle)
        return memcpy(self, handle, self.size)

    def to(self, devType: DEVICE_TYPE, destroySelf: bool = False):
        """Tansfer handle to assiged device.
        
        Args:
            devType(devType): The device type to transfer.
            destroySelf(bool): Wether to destroy self after transfer to other device(default False).
        """
        self._check_destroy()
        if self.devType == devType:
            return self
        else:
            dataHandle = DataHandle(self.size, devType)
            self.copyTo(dataHandle)
            if destroySelf: self.destroy()
            return dataHandle


class DataContainer(PointerContainer):
    """Data Container.

    Args:
        handle(DataHandle): The instance of the DataHandle.
        detach(bool): whether the handle will be detached or not. If detached, the data handle object will be released by data container(default False).
        ptr(Any): The data pointer if you have held it.
    """
    def __init__(self, handle: DataHandle, detach: bool = False, ptr=None):
        self._handle = handle
        self._ptr = ptr
        self.detach = detach

    def _check_destroy(self):
        assert self._ptr is not None, "The data container has been destroyed."
        assert self._handle.isAlive, "The handle has been destroyed."

    @property
    def isAlive(self) -> bool:
        """The live state of the data container."""
        return self.ptr is not None

    @property
    def handle(self) -> DataHandle:
        """The handle of the data container."""
        # self._check_destroy()
        return self._handle

    @property
    def size(self) -> int:
        """The size of the data container."""
        self._check_destroy()
        return self.handle.size

    @property
    def devType(self) -> DEVICE_TYPE:
        """The devType of the data container."""
        self._check_destroy()
        return self.handle.devType

    @property
    def devId(self) -> int:
        """The devId of the data container."""
        self._check_destroy()
        return self.handle.devId

    def _destroy_detach(self) -> None:
        if self.detach:
            self.handle.destroy()
            self._handle = None


class DataBuffer(DataContainer):
    """DataBuffer Container.

    Args:
        handle(DataHandle): The instance of the DataHandle.
        detach(bool): whether the handle will be detached or not. If detached, the data handle object will be released by buffer(default False).
        ptr(Any): The buffer pointer if you have held it.
    """
    def __init__(self, handle: DataHandle, detach: bool = False, ptr=None):
        super().__init__(handle, detach, ptr)
        self.detach = detach
        self.create()

    @property
    def size(self) -> int:
        """The size of the data container."""
        self._check_destroy()
        return _vacm.getDataBufferSize(self.ptr)

    @property
    def devInfo(self) -> DeviceInfo:
        """The devInfo of the buffer."""
        self._check_destroy()
        devInfo = DeviceInfo()
        ret = _vacm.getDataBufferDeviceInfo(self.ptr, devInfo)
        if ret != _vacm.ER_SUCCESS:
            raise RuntimeError(f"get tensor device info error, ret: {ret}")
        return devInfo

    @property
    def devType(self) -> DEVICE_TYPE:
        """The devType of the buffer."""
        return self.devInfo.deviceType

    @property
    def devId(self) -> int:
        """The devId of the buffer."""
        return self.devInfo.deviceIdx

    def create(self) -> None:
        """Create data buffer."""
        if self._ptr is None:
            self._ptr = _vacm.createDataBuffer(self._handle.devInfo,
                                               self._handle.ptr,
                                               self._handle.size)

    @err_check
    def update(self, handle: DataHandle) -> int:
        """Update the data buffer.
    
        Args:
            handle(DataHandle): The data handle object that holds a memory.

        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        self._handle = handle
        ret = _vacm.updateDataBuffer(self.ptr, handle.devInfo, handle.ptr,
                                     handle.size)
        return ret

    @err_check
    def destroy(self) -> int:
        """Destroy the data buffer."""
        ret = _vacm.ER_SUCCESS
        if self.ptr is not None:
            ret = _vacm.destroyDataBuffer(self.ptr)
            self._destroy_detach()
            self._ptr = None
        return ret


class Tensor(DataContainer):
    """Tensor Container.
    
    Args:
        handle(DataHandle): The instance of the DataHandle.
        shape(Shape): The shape of the tensor.
        dType(D_TYPE): The data type of the tensor.
        detach(bool): whether the handle will be detached or not. If detached, the data handle object will be released by tensor(default False).
        ptr(Any): The tensor pointer if you have held it.
    """
    def __init__(self,
                 handle: DataHandle,
                 shape: Shape,
                 dType: D_TYPE,
                 detach: bool = False,
                 ptr=None):
        super().__init__(handle, detach, ptr)
        self._shape = shape
        self._dType = dType
        self.detach = detach
        self.create()

    @property
    def size(self) -> int:
        """The size of the tensor."""
        self._check_destroy()
        return _vacm.getTensorSize(self.ptr)

    @property
    def devInfo(self) -> DeviceInfo:
        """The devInfo of the tensor."""
        self._check_destroy()
        devInfo = DeviceInfo()
        ret = _vacm.getTensorDeviceInfo(self.ptr, devInfo)
        if ret != _vacm.ER_SUCCESS:
            raise RuntimeError(f"get tensor device info error, ret: {ret}")
        return devInfo

    @property
    def devType(self) -> DEVICE_TYPE:
        """The devType of the tensor."""
        return self.devInfo.deviceType

    @property
    def devId(self) -> int:
        """The devId of the tensor."""
        return self.devInfo.deviceIdx

    @property
    def shape(self) -> Shape:
        """The shape of the tensor."""
        self._check_destroy()
        shape = Shape()
        ret = _vacm.getTensorShape(self.ptr, shape)
        if ret != _vacm.ER_SUCCESS:
            raise RuntimeError(f"get tensor shape error, ret: {ret}.")
        return shape

    @property
    def dtype(self) -> D_TYPE:
        """The dtype of the tensor."""
        self._check_destroy()
        return _vacm.getTensorDataType(self.ptr)

    def create(self) -> None:
        """Create tensor."""
        if self._ptr is None:
            self._ptr = _vacm.createTensor(self._handle.devInfo, self._shape,
                                           self._dType)
            assert _vacm.getTensorSize(
                self.ptr
            ) == self._handle.size, "The shape of the tensor mismatch the size of the handle."
            ret = _vacm.setTensorDataHandle(self._ptr, self._handle.ptr, False)
            if ret != _vacm.ER_SUCCESS:
                raise RuntimeError(
                    f"set tensor data handle error, ret: {ret}.")

    @err_check
    def destroy(self) -> int:
        """Destroy the tensor."""
        ret = _vacm.ER_SUCCESS
        if self._ptr is not None:
            ret = _vacm.destroyTensor(self.ptr)
            self._destroy_detach()
            self._ptr = None
        return ret


class Dataset(PointerContainer):
    """Dataset Container.

    Args:
        mode(DATASET_MODE): The dataset mode, including TENSOR and BUFFER.
        detach(bool): whether the data will be detached or not. If detached, all the object will be released by dataset(default False).
        ptr(Any): The dataset pointer if you have held it.
    """
    def __init__(self, mode: DATASET_MODE, detach: bool = False, ptr=None):
        self._mode = mode
        self._ptr = ptr
        self._ctx = None
        self.detach = detach
        self.create()

    @property
    def mode(self) -> DATASET_MODE:
        """The mode of the dataset."""
        return self._mode

    @property
    def size(self) -> int:
        """The size of the dataset."""
        if self.mode == DATASET_MODE.BUFFER:
            return _vacm.getDatasetBufferCount(self.ptr)
        else:
            return _vacm.getDatasetTensorCount(self.ptr)

    def _check_destroy(self):
        assert self._ptr is not None, "The dataset has been destroyed."

    def create(self) -> None:
        """Create dataste."""
        if self._ptr is None:
            self._ptr = _vacm.createDataset(self.mode)

    @err_check
    def destroy(self) -> int:
        """Destroy the dataset."""
        ret = _vacm.ER_SUCCESS
        if self._ptr is not None:
            if self.detach:
                # 所有python对象清空
                for i in range(self.size):
                    data = self.getData(i)
                    data._handle = None
                    data._ptr = None
                ret = _vacm.destroyDatasetAll(self.ptr)
            else:
                ret = _vacm.destroyDataset(self.ptr)
            self._ptr = None
            self._ctx = None
        return ret

    @err_check
    def addData(self, data: Union[DataBuffer, Tensor]) -> int:
        """Add data to the dataset.
        
        Args:
            data(Union[DataBuffer, Tensor]): The data  The data  to be added.
        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        self._check_destroy()
        if isinstance(data, DataBuffer):
            assert self.mode == DATASET_MODE.BUFFER, "This dataset mode only support buffer."
            return _vacm.addDatasetBuffer(self.ptr, data.ptr)
        elif isinstance(data, Tensor):
            assert self.mode == DATASET_MODE.TENSOR, "This dataset mode only support tendor."
            return _vacm.addDatasetTensor(self.ptr, data.ptr)
        else:
            raise RuntimeError("Unsupported data type.")

    def getData(self, index: int) -> Union[DataBuffer, Tensor]:
        """Get data in the dataset.

        Args:
            index(int): The index of data buffer in dataset object.

        Returns:
            Union[DataBuffer, Tensor]: The data of the specified index in dataset object.
        """
        self._check_destroy()
        if index < 0 or index >= self.size:
            raise RuntimeError(
                f"index out of range, dataset support 0 <= index < {self.size}"
            )
        if self.mode == DATASET_MODE.BUFFER:
            buffer_ptr = _vacm.getDatasetBuffer(self.ptr, index)
            buffer_size = _vacm.getDataBufferSize(buffer_ptr)
            buffer_devInfo = DeviceInfo()
            ret = _vacm.getDataBufferDeviceInfo(buffer_ptr, buffer_devInfo)
            if ret != _vacm.ER_SUCCESS:
                raise RuntimeError(f"get tensor device info error, ret: {ret}")
            handle_ptr = _vacm.getDataBufferAddr(buffer_ptr)
            handle = DataHandle(buffer_size, buffer_devInfo.deviceType,
                                handle_ptr)
            handle.devInfo = buffer_devInfo
            buffer = DataBuffer(handle, ptr=buffer_ptr)
            return buffer
        elif self.mode == DATASET_MODE.TENSOR:
            tensor_ptr = _vacm.getDatasetTensor(self.ptr, index)
            tensor_size = _vacm.getTensorSize(tensor_ptr)
            tensor_dtype = _vacm.getTensorDataType(tensor_ptr)
            tensor_shape = Shape()
            ret = _vacm.getTensorShape(tensor_ptr, tensor_shape)
            if ret != _vacm.ER_SUCCESS:
                raise RuntimeError(f"get tensor shape error, ret: {ret}")
            tensor_devInfo = DeviceInfo()
            ret = _vacm.getTensorDeviceInfo(tensor_ptr, tensor_devInfo)
            if ret != _vacm.ER_SUCCESS:
                raise RuntimeError(f"get tensor device info error, ret: {ret}")
            handle_ptr = _vacm.getTensorDataHandle(tensor_ptr)
            handle = DataHandle(tensor_size, tensor_devInfo.deviceType,
                                handle_ptr)
            handle.devInfo = tensor_devInfo
            tensor = Tensor(handle, tensor_shape, tensor_dtype, ptr=tensor_ptr)
            return tensor
        else:
            raise RuntimeError("Unsupported data type.")

    @err_check
    def clear(self) -> int:
        """Clear the dataset.
    
        Hint:
            This function is that only clear tensors and buffers in the dataset.
        
        Args:
            dataset(Dataset): The dataset object.
            
        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        self._check_destroy()
        self._ctx = None
        return _vacm.clearDataset(self.ptr)

    @err_check
    def setUserCtx(self, userCtx: DataHandle) -> int:
        """Set the user context data for a dataset.
    
        Args:
            userCtx(DataHandle): The data handle object of user data waited to be set.

        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        self._check_destroy()
        self._ctx = userCtx
        return _vacm.setDatasetUserCtx(self.ptr, userCtx.ptr)

    def getUserCtx(self) -> DataHandle:
        """Get the user context data for a dataset.
        
        Returns:    
            DataHandle: The data handle object of the user data.
        """
        self._check_destroy()
        return self._ctx


# ================================================ Handle ======================================================


def mallocHost(memSize: int) -> DataHandle:
    """Allocate memory from host.

    Args:
        memSize(int): The size of memory in bytes.
        
    Returns:
        DataHandle: The data handle object that holds the memory in host.
    """
    return DataHandle(memSize)


def freeHost(handle: DataHandle) -> int:
    """Free a memory in host.

    Args:
        handle(DataHandle): The data handle object that holds a memory in host.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return handle.destroy()


def mallocDevice(memSize: int) -> DataHandle:
    """Allocate memory from device.

    Args:
        memSize(int): The size of memory in bytes.

    Returns:
        DataHandle: The data handle object that holds the memory in device.
    """
    return DataHandle(memSize, DEVICE_TYPE.VACC)


def freeDevice(handle: DataHandle) -> int:
    """Free a memory in device.
    
    Args:
        handle(DataHandle): The data handle object that holds the memory in device.
        
    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return handle.destroy()


def mallocModelInOut(memSize: int) -> DataHandle:
    """Allocate memory for model input or output from device.
    
    Args:
        memSize(int): The size of memory in bytes.
    
    Returns:
        DataHandle: The data handle object that holds the memory in device.
    """
    return DataHandle(memSize, DEVICE_TYPE.VACC)


def freeModelInOut(handle: DataHandle) -> int:
    """Free a model input or output memory in device.
    
    Args:
        handle(DataHandle): The data handle object that holds the memory in device.
    
    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return handle.destroy()


@err_check
def memcpy(handleSrc: DataHandle,
           handleDst: DataHandle,
           memSize: int = -1) -> int:
    """Copy a memory between host and device according to copy type. Synchronous interface.

    Args:
        handleSrc(DataHandle): The data handle object that holds the source memory.
        handleDst(DataHandle): The data handle object that holds the destination memory.
        memSize(int): The size of memory in bytes to copy(default -1, eq handleSrc's size).

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    if memSize > 0:
        assert handleSrc.size >= memSize and handleDst.size >= memSize, "The size of the handle(src and dst) need to greater than memSize."
    else:
        memSize = handleSrc.size
    if handleSrc.devType == DEVICE_TYPE.CPU and handleDst.devType == DEVICE_TYPE.VACC:
        cmType = COPY_MEM_TYPE.TO_DEVICE
    elif handleSrc.devType == DEVICE_TYPE.VACC and handleDst.devType == DEVICE_TYPE.CPU:
        cmType = COPY_MEM_TYPE.FROM_DEVICE
    elif handleSrc.devType == DEVICE_TYPE.VACC and handleDst.devType == DEVICE_TYPE.VACC:
        cmType = COPY_MEM_TYPE.DEVICE_TO_DEVICE
        if handleSrc.devId == handleDst.devId:
            raise RuntimeError("Not implement.")
        return _vacm.memcpyDevices(handleSrc.ptr, handleSrc.devId,
                                   handleDst.ptr, handleDst.devId, memSize)
    else:
        raise RuntimeError("Can not support copy mem from host to host.")
    return _vacm.memcpy(handleSrc.ptr, handleDst.ptr, memSize, cmType)


def getNumpyFromHandle(handle: DataHandle,
                       dtype: np.dtype = np.uint8) -> np.ndarray:
    """Get the numpy array from data handle object.
    
    Args:
        dataHandle(DataHandle): The data handle object that holds the memory.
        dtype(np.dtype): The dtype of the numpy.
        
    Returns:
        numpy.ndarray: The numpy array.
    """
    if handle.devType == DEVICE_TYPE.VACC:
        hostHandle = handle.to(DEVICE_TYPE.CPU)
        numpyData = _vacm.getNumpyFromHandle(hostHandle.ptr, hostHandle.size)
        hostHandle.destroy()
    else:
        numpyData = _vacm.getNumpyFromHandle(handle.ptr, handle.size)
    if dtype != np.uint8:
        dataBytes = numpyData.tobytes()
        numpyData = np.frombuffer(dataBytes, dtype)
    return numpyData


def getHandleFromNumpy(numpyData: np.ndarray) -> DataHandle:
    """Get data handle from the numpy array.
    
    Args:
        numpyData(numpy.ndarray): The numpy array waited to get data handle object.
    
    Returns:
        DataHandle: The host data handle object that holds the numpy array.
    """
    numpyData = np.ascontiguousarray(numpyData)
    if numpyData.dtype != np.uint8:
        dataBytes = numpyData.tobytes()
        numpyData = np.frombuffer(dataBytes, np.uint8)
    devInfo = DeviceInfo()
    devInfo.deviceIdx = 0
    devInfo.deviceType = DEVICE_TYPE.CPU
    return DataHandle(numpyData.size, DEVICE_TYPE.CPU,
                      _vacm.getHandleFromNumpy(numpyData))


# @err_check
# def memcpyAsync(handleSrc: DataHandle, handleDst: DataHandle, memSize: int, cmType: COPY_MEM_TYPE, evt: Any) -> int:
#     """Copy a memory between host and device according to copy type. Asynchronous interface.

#     Args:
#         handleSrc(DataHandle): The data handle object that holds the source memory.
#         handleDst(DataHandle): The data handle object that holds the destination memory.
#         memSize(int): The size of memory in bytes to copy.
#         cmType(COPY_MEM_TYPE): The type of copying.
#         evt()

#     Returns:
#         int: The return code. 0 for success, False otherwise.
#     """
#     return _vacm.memcpyAsync(handleSrc.ptr, handleDst.ptr, memSize, cmType, evt)

# @err_check
# def memcpyDevices(handleSrc: DataHandle, handleDst: DataHandle, memSize: int) -> int:
#     """Copy a memory between two devices. Synchronous interface.

#     Args:
#         handleSrc(DataHandle): The data handle object that holds the source memory in device.
#         devIdxSrc(int): The index of the source device.
#         handleDst(DataHandle): The data handle object that holds the destination memory in device.
#         devIdxDst(int): The index of the destination device.
#         memSize(int): The size of memory in bytes to copy.

#     Returns:
#         int: The return code. 0 for success, False otherwise.
#     """
#     assert handleSrc.size >= memSize and handleDst >= memSize, "The size of the handle(src and dst) need to greater than memSize."
#     assert handleSrc.devInfo.deviceType == DEVICE_TYPE.CPU, "The device type of the src should be VACC."
#     assert handleDst.devInfo.deviceType == DEVICE_TYPE.CPU, "The device type of the dst should be VACC."
#     if handleSrc.devInfo.deviceIdx == handleDst.devInfo.deviceIdx:
#             raise RuntimeError("Not implement.")
#     return _vacm.memcpyDevices(handleSrc.ptr, handleSrc.devInfo.deviceIdx, handleDst.ptr, handleDst.devInfo.deviceIdx, memSize)

# @err_check
# def memcpyDevicesAsync(handleSrc: DataHandle, devIdxSrc: int, handleDst: DataHandle, devIdxDst: int, memSize: int, evt: Any) -> int:
#     """Copy a memory between two devices. Asynchronous interface.

#     Args:
#         handleSrc(DataHandle): The data handle object that holds the source memory in device.
#         devIdxSrc(int): The index of the source device.
#         handleDst(DataHandle): The data handle object that holds the destination memory in device.
#         devIdxDst(int): The index of the destination device.
#         memSize(int): The size of memory in bytes to copy.
#         evt()

#     Returns:
#         int: The return code. 0 for success, False otherwise.
#     """
#     return _vacm.memcpyDevicesAsync(handleSrc.ptr, devIdxSrc, handleDst.ptr, devIdxDst, memSize, evt)

# @err_check
# def memset(handle: DataHandle, value: int, count: int) -> int:
#     """Set a memory block with a specific value. Synchronous interface.

#     Args:
#         handle(DataHandle): The data handle object that holds the memory.
#         value(int): The value to be set.
#         count(int): The size of memory to be set.

#     Returns:
#         int: The return code. 0 for success, False otherwise.
#     """
#     return _vacm.memset(handle.ptr, value, count)

# @err_check
# def memsetAsync(handle: DataHandle, value: int, count: int, evt: Any) -> int:
#     """Set a memory block with a specific value. Asynchronous interface.

#     Args:
#         handle(DataHandle): The data handle object that holds the memory.
#         value(int): The value to be set.
#         count(int): The size of memory to be set.
#         evt()

#     Returns:
#         int: The return code. 0 for success, False otherwise.
#     """
#     return _vacm.memsetAsync(handle.ptr, value, count, evt)

# ================================================ Buffer ======================================================


def createDataBuffer(handle: DataHandle, detach: bool = False) -> DataBuffer:
    """Create a data buffer.
    
    Args:
        handle(DataHandle): The data handle object that holds a data memory.
        detach(bool): whether the handle will be detached or not. If detached, the data handle object will be released by tensor(default False).
    
    Returns:
        DataBuffer: The data buffer object.
    """
    return DataBuffer(handle, detach)


# def createDataBufferFromContext(handle: DataHandle,
#                                 detach: bool = True) -> DataBuffer:
#     """Create a data buffer from device context.

#     Args:
#         handle(DataHandle): The data handle object that holds a data memory.
#         detach(bool): whether the handle will be detached or not. If detached, the data handle object will be released by tensor(default True).

#     Returns:
#         DataBuffer: The data buffer object.
#     """
#     return DataBuffer(handle, detach)


def destroyDataBuffer(buffer: DataBuffer) -> int:
    """Destroy a data buffer.

    Args:
        buffer(DataBuffer): The data buffer object.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return buffer.destroy()


def getDataBufferAddr(buffer: DataBuffer) -> DataHandle:
    """Get the data handle object about a data buffer.

    Args:
        buffer(DataBuffer): The data buffer object.
        
    Returns:
        DataHandle: The data handle object that holds a memory.
    """
    return buffer.handle


def getDataBufferSize(buffer: DataBuffer) -> int:
    """Get the buffer size for a data buffer.
    
    Args:
        buffer(DataBuffer): The data buffer object.
        
    Returns:
        int: The size of data buffer.
    """
    return buffer.size


def getDataBufferDeviceInfo(buffer: DataBuffer) -> DeviceInfo:
    """Get the device information for a data buffer.
    
    Args:
        buffer(DataBuffer): The data buffer object.
        
    Returns:
        DeviceInfo: The device information of the data buffer object.
    """
    deviceInfo = DeviceInfo()
    deviceInfo.deviceIdx = buffer.devId
    deviceInfo.deviceType = buffer.devType
    return deviceInfo


@err_check
def updateDataBuffer(buffer: DataBuffer, handle: DataHandle) -> int:
    """Update a data buffer.
    
    Args:
        buffer(DataBuffer): The data buffer object.
        handle(DataHandle): The data handle object that holds a memory.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return buffer.update(handle)


# ================================================ Tensor ======================================================


def createTensor(handle: DataHandle,
                 shape: Shape,
                 dType: D_TYPE,
                 detach: bool = False) -> Tensor:
    """Create a tensor for device with specific shapes and data type.
    
    Args:
        handle(DataHandle): The data handle object that holds a memory.
        shape(Shape): The shape of the tensor.
        dType(D_TYPE): The data type of the tensor.
        detach(bool): whether the handle will be detached or not. If detached, the data handle object will be released by tensor(default False).
    Returns:
        Tensor: The tensor object.
    """
    return Tensor(handle, shape, dType, detach)


def destroyTensor(tensor: Tensor) -> int:
    """Destroy a tensor.

    Args:
        tensor(Tensor): The tensor object.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return tensor.destroy()


def getTensorDataHandle(tensor: Tensor) -> DataHandle:
    """Get the data handle object of a tensor.

    Args:
        tensor(Tensor): The tensor object.
    
    Returns:    
        DataHandle: The data handle object that holds a memory.
    """
    return tensor.handle


def getTensorDeviceInfo(tensor: Tensor) -> DeviceInfo:
    """Get the device information of a tensor.

    Args:
        tensor(Tensor): The tensor object.
    
    Returns:
        DeviceInfo: The device information of the tensor.
    """
    deviceInfo = DeviceInfo()
    deviceInfo.deviceIdx = tensor.devId
    deviceInfo.deviceType = tensor.devType
    return deviceInfo


def getTensorShape(tensor: Tensor) -> Shape:
    """Get the data shape of a tensor.

    Args:
        tensor(Tensor): The tensor object.
        
    Returns:
        Shape: The shape of the tensor.
    """
    return tensor.shape


def getTensorDataType(tensor: Tensor) -> D_TYPE:
    """Get the data type of a tensor.
    
    Args:
        tensor(Tensor): The tensor object.
        
    Returns:
        D_TYPE: The data type of the tensor object.
    """
    return tensor.dtype


def getTensorSize(tensor: Tensor) -> int:
    """Get the size of a tensor.
    
    Args:
        tensor(Tensor): The tensor object.
    
    Returns:
        int: The size of tensor.
    """
    return tensor.size


# ================================================ Buffer ======================================================


def createDataset(mode: DATASET_MODE) -> Dataset:
    """Create a dataset.
    
    Args:   
        mode(DATASET_MODE): The dataset mode, including TENSOR and BUFFER.
    
    Returns:
         Dataset: The dataset object.
    """
    return Dataset(mode)


def destroyDataset(dataset: Dataset) -> int:
    """Destroy a dataset.
    
    Args:
        dataset(Dataset): The dataset object.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return dataset.destroy()


def destroyDatasetAll(dataset: Dataset) -> int:
    """Destroy all data in the dataset.

    Args:
        dataset(Dataset): The dataset object.
    """
    dataset.detach = True
    return dataset.destroy()


@err_check
def addDatasetBuffer(dataset: Dataset, buffer: DataBuffer) -> int:
    """Add a dataset buffer.
    
    Args:
        dataset(Dataset): The dataset object.
        buffer(DataBuffer): The data buffer object waited to be added.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return dataset.addData(buffer)


def getDatasetBufferCount(dataset: Dataset) -> int:
    """Get the data buffer count for a dataset.

    Args:
        dataset(Dataset): The dataset object.
        
    Returns:
        int: The buffer count of the dataset holding.
    """
    return dataset.size


def getDatasetBuffer(dataset: Dataset, index: int) -> DataBuffer:
    """Get the data buffer by index for a dataset.
    
    Args:
        dataset(Dataset): The dataset object that holds data buffer.
        index(int): The index of data buffer in dataset object.

    Returns:
        DataBuffer: The data buffer of the specified index in dataset object
    """
    return dataset.getData(index)


@err_check
def addDatasetTensor(dataset: Dataset, tensor: Tensor) -> int:
    """Add a tensor into a dataset.
    
    Args:
        dataset(Dataset): The dataset object.
        tensor(Tensor): The tensor object waited to be added.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return dataset.addData(tensor)


def getDatasetTensorCount(dataset: Dataset) -> int:
    """Get the tensor count for a dataset.
    
    Args:
        dataset(Dataset): The dataset object.
    
    Returns:
        int: The tensor count of the dataset holding.
    """
    return dataset.size


def getDatasetTensor(dataset: Dataset, index: int) -> Tensor:
    """Get the tensor by index for a dataset.
    
    Args:
        dataset(Dataset): The dataset object.
        index(int): The index of tensor in dataset object.

    Returns:
        Tensor: The tensor of the specified index in dataset object.
    """
    return dataset.getData(index)


def getDatasetMode(dataset: Dataset) -> DATASET_MODE:
    """Get the mode for a dataset, including TENSOR and BUFFER.
    
    Args:
        dataset(Dataset): The dataset object.
    
    Returns:
        DATASET_MODE: The data mode of the dataset object holding.
    """
    return dataset.mode


def getDatasetUserCtx(dataset: Dataset) -> DataHandle:
    """Get the user context data for a dataset.
    
    Args:
        dataset(Dataset): The dataset object.
    
    Returns:    
        DataHandle: The data handle object of the user data.
    """
    return dataset.getUserCtx()


@err_check
def setDatasetUserCtx(dataset: Dataset, userCtx: DataHandle) -> int:
    """Set the user context data for a dataset.
    
    Args:
        dataset(Dataset): The dataset object.
        userCtx(DataHandle): The data handle object of user data waited to be set.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return dataset.setUserCtx(userCtx)


@err_check
def clearDataset(dataset: Dataset) -> int:
    """Clear a dataset.
    
    Hint:
        This function is that only clear tensors and buffers in the dataset.
    
    Args:
        dataset(Dataset): The dataset object.
        
    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return dataset.clear()


# ================================================ Utils ======================================================


def getDataTypeSize(dType: D_TYPE) -> int:
    """Get the byte size for a data type.

    Args:
        dType(D_TYPE): The data type.

    Returns:
        int: The size of the data type in bytes.
    """
    return _vacm.getDataTypeSize(dType)


def getFloatArrayFromHandle(handle: DataHandle) -> List[float]:
    """Get float array from handle.
    
    Hint:
        If the type of your data on the device is fp16, 
        this function transfer fp16 data to float array.

    Args:
        handle(DataHandle): The data handle object that holds a data memory.
    
    Returns:
        List[float]: The array of float value.
    """
    if handle.devInfo.deviceType == DEVICE_TYPE.VACC:
        hostHandle = mallocHost(handle.size)
        memcpy(handle, hostHandle, handle.size)
        float16Array = _vacm.getFloat16Array(hostHandle.ptr, hostHandle.size)
        float32Array = _vacm.float16ToFloat32Array(float16Array)
        freeHost(hostHandle)
    else:
        float16Array = _vacm.getFloat16Array(handle.ptr, handle.size)
        float32Array = _vacm.float16ToFloat32Array(float16Array)
    return float32Array


# def float16ToFloat32(valIn: int) -> float:
#     """Convert a float16 value to float value.

#     Hint:
#         The float16 value is a int(uint16) in python.

#     Args:
#         valIn(int): The float16 value waited to be converted.

#     Returns:
#         float: The float value.
#     """
#     return _vacm.float16ToFloat32(valIn)

# def float32ToFloat16(valIn: float) -> int:
#     """Convert a float value to float16 value.

#     Hint:
#         The float16 value is a int(uint16) in python.

#     Args:
#         valIn(float): The float value waited to be converted.

#     Returns:
#         int: The float16 value.
#     """
#     return _vacm.float32ToFloat16(valIn)

# def float16ToFloat32Array(array: List[float]) -> List[float]:
#     """Convert an array of float16 value to the array of float32 value.

#     Hint:
#         The float16 value is a int(uint16) in python.

#     Args:
#         array(List[float]): The array of float16 value.

#     Returns:
#         List[float]: The converted array of float32 value.
#     """
#     return _vacm.float16ToFloat32Array(array)

# def float32ToFloat16Array(array: List[float]) -> List[float]:
#     """Convert an array of float32 value to the array of float16 value.

#     Hint:
#         The float16 value is a int(uint16) in python.

#     Args:
#         array(List[float]): The array of float32 value.

#     Returns:
#         List[float]: The converted array of float16 value.
#     """
#     return _vacm.float32ToFloat16Array(array)

# def getFloat16Array(handle: DataHandle, outputSize: int) -> List[float]:
#     """Get the array of float16 value.

#     Hint:
#         The float16 value is a int(uint16) in python.

#     Args:
#         handle(DataHandle): The data handle object that holds a data memory.
#         outputSize(int): The size of the memory.

#     Returns:
#         List[float]: The array of float16 value.
#     """
#     return _vacm.getFloat16Array(handle.ptr, outputSize)

# def getFloat32Array(handle: DataHandle, outputSize: int) -> List[float]:
#     """Get the array of float32 value.

#     Args:
#         handle(DataHandle): The data handle object that holds a data memory.
#         outputSize(int): The size of the memory.

#     Returns:
#         List[float]: The array of float32 value.
#     """
#     float16Array = getFloat16Array(handle, outputSize)
#     return float16ToFloat32Array(float16Array)