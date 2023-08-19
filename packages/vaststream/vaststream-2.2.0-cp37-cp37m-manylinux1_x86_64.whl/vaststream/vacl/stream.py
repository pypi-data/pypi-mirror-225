# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8
__all__ = [
    "createOpGraph", "destroyOpGraph", "createOpStream", "destroyOpStream",
    "subscribeStreamReport", "buildStream", "runStream", "runStreamAsync",
    "synchronizeStream", "synchronizeDevice", "getStreamCacheNumber",
    "requestOutputDataset", "createGraphInputOp", "connectOps",
    "createRunModelOp", "registerGetOutput", "registerGetOutputs", "Graph",
    "Stream"
]

import inspect
from typing import Any, Union, List
from _vaststream_pybind11 import vacl as _vacl
from vaststream.vacm import Dataset, DATASET_MODE, PointerContainer
from vaststream.vace import Op, OpBase, destroyOp
from .utils import *
from .common import *
from .model import Model, ModelDataset

# import abc
# class CallBack(metaclass=abc.ABCMeta):

#     def __init__(self):
#         self.__result_list = None
#         self.__userCtx = None

#     def __call__(self, op: Op, inputDataset: Dataset, outputDataset: Dataset, status: CallBackStatus, userCtx: Any):
#         """
#         The callback function of type vaclStreamReportCallback.
#         Args:
#         op:  a vace operator instance.
#         inputDataset: a vacm input dataset instance.
#         outputDataset: a vacm output dataset instance.
#         status: a vacl callback status.
#         userCtx: the user defined context.
#         """
#         assert status.errorCode == 0

#         if not self.__userCtx:
#             self.__userCtx = userCtx

#         buffer_count = vacm.getDatasetBufferCount(outputDataset)
#         self.__result_list = []
#         for i in range(buffer_count):
#             buffer_device = vacm.getDatasetBuffer(outputDataset, i)
#             handle_device = vacm.getDataBufferAddr(buffer_device)
#             buffer_size = vacm.getDataBufferSize(buffer_device)
#             handle_host = vacm.mallocHost(buffer_size)
#             assert vacm.memcpy(handle_device, handle_host, buffer_size,
#                             vacm.COPY_MEM_TYPE.FROM_DEVICE) == 0
#             list_float16 = vacm.getFloat16Array(handle_host, buffer_size)
#             list_float32 = vacm.float16ToFloat32Array(list_float16)
#             self.__result_list.append(list_float32)
#             assert vacm.freeHost(handle_host) == 0

#         #other process
#         self.process()

#     def get_result(self) -> List[List[float]]:
#         return self.__result_list

#     def get_user_info(self) -> Any:
#         return self.__userCtx

#     @abc.abstractmethod
#     def process(self):
#         pass


class Graph(PointerContainer):
    """Graph tool class.

    This class contains all operations on the graph.

    Args:
        bindOp (bool): If bindOp is True, all the ops will destroy while destroy the graph(default True).
    
    Examples:
        >>> graph = vacl.Graph()
        >>> inputOp = graph.createInputOp(1)
        >>> runModelOp = graph.createRunModelOp(model)
        >>> graph.connectOps(inputOp, preProcessOp)
        >>> graph.connectOps(preProcessOp, runModelOp)
    """

    def __init__(self, bindOp: bool = True) -> None:
        self.bindOp = bindOp
        # 记录图信息，处理资源释放问题
        self._stream_records = []
        self._op_records = []
        self._model_records = []
        self._ptr = None
        self.create()

    def __del__(self):
        self.destroy()

    def __eq__(self, other) -> bool:
        if isinstance(other, Graph):
            return self.id == other.id
        return False

    def _check_destroy(self):
        assert self._ptr is not None, "graph has been destroyed."

    def create(self) -> None:
        """Create the graph."""
        if self._ptr is None:
            self._ptr = _vacl.createOpGraph()

    @err_check
    def destroy(self) -> int:
        """Destroy the graph."""
        ret = _vacl.vaclER_SUCCESS
        if self._ptr is not None:
            # destroy all op in op_records
            if self.bindOp:
                for op in self._op_records:
                    if isinstance(op, OpBase):
                        op.destroy()
                    elif isinstance(op, Op):
                        destroyOp(op)
                for op in self._model_records:
                    op.destroy()
            # stream是建立在graph之上的，所有需要优先释放
            for stream in self._stream_records:
                stream.destroy()
            ret = _vacl.destroyOpGraph(self.ptr)
            self._graph = None
            self._op_records.clear()
            self._model_records.clear()
            self._stream_records.clear()
        return ret

    def createInputOp(self, inputCnt: int = 1) -> Op:
        """Create the stream input op.
     
        Args:
            inputCnt (int): Input number of a stream per batch(default 1).
        
        Returns:
            Op: VaceOp with input.
        """
        self._check_destroy()
        op = Op(_vacl.createGraphInputOp(self.ptr, inputCnt))
        if op not in self._op_records: self._op_records.append(op)
        return op

    @err_check
    def connectOps(self, parent: Union[Op, OpBase],
                   child: Union[Op, OpBase]) -> int:
        """Connect a vace operator to other. 
        
        This is to build the operator execution sequence (in DAG).
         
        Args:
            parent (Union[Op, OpBase]):  The operator instance to be connected as parent node.
            child (Union[Op, OpBase]):  The operator instance to be connected as child node.
        
        Returns:
            int: The return code. 0 for success, False otherwise.            
        """
        self._check_destroy()
        if parent not in self._op_records: self._op_records.append(parent)
        if child not in self._op_records: self._op_records.append(child)
        if isinstance(parent, OpBase): parent = parent.op
        if isinstance(child, OpBase): child = child.op
        return _vacl.connectOps(parent.ptr, child.ptr)

    def createRunModelOp(self, model: Model) -> Op:
        """Create the run model op.
     
        Args:
            model (Model): The Model instance.
        
        Returns:
            Op: VaceOp with input.
        """
        self._check_destroy()
        if model not in self._model_records:
            self._model_records.append(model)
        return Op(_vacl.createRunModelOp(model.ptr))


class Stream(PointerContainer):
    """Stream tool class.

    This class contains all operations on the stream.

    Args:
        graph (Union[OpGraph, Graph]): The graph instance.
        mode (BALANCE_MODE): Mode of stream to communicate with backend(default vacl.BALANCE_MODE.ONCE).
    
    Examples:
        >>> stream = vacl.Stream(graph)
        >>> stream.registerGetOutput(copyMemOp)
        >>> stream.subscribeStreamReport(callback, userCtx)
        >>> stream.build()
        >>> stream.runStreamAsync(datasetIn, datasetOut)
        >>> stream.synchronize()
    """

    def __init__(self, graph: Graph, mode: BALANCE_MODE = BALANCE_MODE.ONCE):

        self.graph = graph
        self.mode = mode
        self._ptr = None
        self.create()

    def __enter__(self):
        # self.create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.destroy()

    def __del__(self):
        self.destroy()

    def __eq__(self, other) -> bool:
        if isinstance(other, Stream):
            return self.id == other.id
        return False

    def _check_destroy(self):
        assert self._ptr is not None, "stream has been destroyed."

    @property
    def cacheNum(self) -> int:
        """The cache number of the stream."""
        return self.getCacheNumber()

    def create(self) -> None:
        """Create the stream."""
        if self._ptr is None:
            self._ptr = _vacl.createOpStream(self.graph.ptr, self.mode)

    @err_check
    def destroy(self) -> int:
        """Destroy the stream."""
        ret = _vacl.vaclER_SUCCESS
        if self._ptr is not None:
            ret = _vacl.destroyOpStream(self.ptr)
            self._ptr = None
        return ret

    @err_check
    def build(self) -> int:
        """Build the stream."""
        self._check_destroy()
        return _vacl.buildStream(self.ptr)

    @err_check
    def registerGetOutput(self, op: Op) -> int:
        """Register a stream operator to the stream in order to get its output after model running.

        Hint:
            If the stream operator is fused into a new stream operator, it will be not available to get the output.
        
        Args:
            op (Union[Op, OpBase]): Vace operator instance whose outputs is that user want to get.
        
        Returns:
            int: The return code. 0 for success, False otherwise. 
        """
        self._check_destroy()
        if isinstance(op, OpBase): op = op.op
        return _vacl.registerGetOutput(self.ptr, op.ptr)

    def registerGetOutputs(
            self, ops: Union[Union[Op, List[Op]], Union[OpBase,
                                                        List[OpBase]]]) -> int:
        """Register a stream operators to the stream in order to get its output after model running.

        Hint:
            If the stream operator is fused into a new stream operator, it will be not available to get the output.
        
        Args:
            ops (Union[Union[Op, List[Op]], Union[OpBase, List[OpBase]]]):  Vace operator array whose outputs is that user want to get.
        
        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        self._check_destroy()
        if not isinstance(ops, list): ops = [ops]
        ops = [op.op.ptr if isinstance(op, OpBase) else op.ptr for op in ops]
        return _vacl.registerGetOutputs(self.ptr, ops)

    def requestOutputDataset(self) -> ModelDataset:
        """Request the output dataset.
     
        Args:
            stream (Stream): The stream instance.
        
        Returns:
            ModelDataset: Dataset with output.
        """
        self._check_destroy()
        return ModelDataset(Dataset(DATASET_MODE.BUFFER,
                                    ptr=_vacl.requestOutputDataset(self.ptr)),
                            type=MODEL_DATASET_TYPE.OUTPUT)

    @err_check
    def subscribeReport(self, callback: Any, userCtx: Any) -> int:
        """Subscribe a callback function.
    
        The callback function receive the result report when a specific stream operator execution is completed.
        The function must conform to our protocol, and ``userCtx`` will transmit to the callback function.

        Important:
            The callback function must conform to our protocol, please add args's annotation, it will be checked.

        Example:
            >>> def callback(op: vace.Op, inputDataset: vacl.ModelDataset, outputDataset: vacl.ModelDataset, status: vacl.CallBackStatus, userCtx: Any):
            >>>     pass
            >>> stream.subscribeStreamReport(callback, userCtx)
            
        Args:
            callback(function): The callback function.
            userCtx (Any): The user context to be passed into the callback function.
        
        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        self._check_destroy()
        # 校验回调函数参数
        sig = inspect.signature(callback)
        params = sig.parameters
        try:
            assert len(params) == 5
            for i, (_, v) in enumerate(params.items()):
                if i == 0: assert v.annotation == Op
                elif i == 1: assert v.annotation == ModelDataset
                elif i == 2: assert v.annotation == ModelDataset
                elif i == 3: assert v.annotation == CallBackStatus
        except:
            tips = """
            Please check your callback, it should be like this(add args's annotation):
            def callback(op: vace.Op, inputDataset: vacl.ModelDataset, outputDataset: vacl.ModelDataset, status: vacl.CallBackStatus, userCtx):
                # your callback code
                pass
            """
            raise RuntimeError(tips)

        def _callback(op: Any, inputDataset: Any, outputDataset: Any,
                      status: CallBackStatus, userCtx: Any):
            _input = ModelDataset(Dataset(DATASET_MODE.BUFFER,
                                          ptr=inputDataset),
                                  type=MODEL_DATASET_TYPE.INPUT)
            _output = ModelDataset(Dataset(DATASET_MODE.BUFFER,
                                           ptr=outputDataset),
                                   type=MODEL_DATASET_TYPE.OUTPUT)
            _op = Op(op)
            callback(_op, _input, _output, status, userCtx)

        return _vacl.subscribeStreamReport(self.ptr, _callback, userCtx)

    def run(self,
            datasetIn: Dataset,
            datasetOut: Dataset,
            timeout: int = 100) -> int:
        """Run the stream in synchronous mode.
     
        Args:
            datasetIn (Dataset): Dataset with input.
            datasetOut (Dataset): Dataset with output instance. 
            timeout (int): Timeout value(default 100ms).
        
        Returns:
            int: The return code. 0 for success, False otherwise.   
        """
        self._check_destroy()
        return _vacl.runStream(self.ptr, datasetIn.ptr, datasetOut.ptr,
                               timeout)

    def runAsync(self, datasetIn: Dataset, datasetOut: Dataset) -> int:
        """Run the stream in asynchronous mode.
     
        Args:
            input (Dataset): Dataset with input instance.
            output (Dataset): Dataset with output instance.

        Returns:
            int: The return code. 0 for success, False otherwise.   
        """
        self._check_destroy()
        return _vacl.runStreamAsync(self.ptr, datasetIn.ptr, datasetOut.ptr)

    def getCacheNumber(self) -> int:
        """Get the cache number of a stream.
        
        Returns:
            int: The cache number of the stream.   
        """
        self._check_destroy()
        return _vacl.getStreamCacheNumber(self.ptr)

    @err_check
    def synchronize(self, timeout: int = 100) -> int:
        """Synchronize the running of a stream. 
    
        This will block the thread running until completion or timeout expired.
        
        Args:
            timeout (int): Timeout value(default 100ms). Value -1 means never timeout.
       
        Returns:
            int: The return code. 0 for success, False otherwise.   
        """
        self._check_destroy()
        return _vacl.synchronizeStream(self.ptr, timeout)


def createOpGraph() -> Graph:
    """Create an empty operator graph in the VACL environment.
    
    Returns:
        graph (OpGraph):A graph instance.
    """
    return Graph()


def destroyOpGraph(graph: Graph) -> int:
    """Destroy the graph.
    
    Args:
        graph (OpGraph): A graph instance.
    
    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return graph.destroy()


def createGraphInputOp(graph: Graph, inputCnt: int = 1) -> Op:
    """Create the stream input op.
     
    Args:
        graph (OpGraph): The graph instance.
        inputCnt (int): Input number of a stream per batch(default 1).
    
    Returns:
        Op: VaceOp with input.
    """
    return graph.createInputOp(inputCnt)


def connectOps(graph: Graph, parent: Union[Op, OpBase],
               child: Union[Op, OpBase]) -> int:
    """Connect a vace operator to other. 
    
    This is to build the operator execution sequence (in DAG).
     
    Args:
        graph (OpGraph): The graph instance.
        parent (Union[Op, OpBase]):  The operator instance to be connected as parent node.
        child (Union[Op, OpBase]):  The operator instance to be connected as child node.
    
    Returns:
        int: The return code. 0 for success, False otherwise.       
    """
    return graph.connectOps(parent, child)


def createRunModelOp(graph: Graph, model: Model) -> Op:
    """Create the run model op.
     
    Args:
        graph (OpGraph): The graph instance.
        model (Model): The Model instance.
    
    Returns:
        Op: VaceOp with input.
    """
    return graph.createRunModelOp(model)


def createOpStream(graph: Graph,
                   mode: BALANCE_MODE = BALANCE_MODE.ONCE) -> Stream:
    """Create the stream.
     
    Args:
        graph (OpGraph): A graph instance.
        mode (BALANCE_MODE): Mode of stream to communicate with backend(default vacl.BALANCE_MODE.ONCE).
    
    Returns:     
        stream (Stream): A stream instance.
    """
    return Stream(graph, mode)


def destroyOpStream(stream: Stream) -> int:
    """Destroy the stream.
     
    Args:
        stream (Stream): The stream instance.
    
    Returns:
        int: The return code. 0 for success, False otherwise.    
    """
    return stream.destroy()


def subscribeStreamReport(stream: Stream, callback: Any, userCtx: Any) -> int:
    """Subscribe a callback function.
    
    The callback function receive the result report when a specific stream operator execution is completed.
    The function must conform to our protocol, and ``userCtx`` will transmit to the callback function.

    Important:
        The callback function must conform to our protocol, please add args's annotation, it will be checked.

    Example:
        >>> def callback(op: vace.Op, inputDataset: vacl.ModelDataset, outputDataset: vacl.ModelDataset, status: vacl.CallBackStatus, userCtx: Any):
        >>>     pass
        >>> stream.subscribeStreamReport(callback, userCtx)
         
    Args:
        stream (Stream): The stream instance.
        callback(function): The callback function.
        userCtx (Any): The user context to be passed into the callback function.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return stream.subscribeReport(callback, userCtx)


def buildStream(stream: Stream) -> int:
    """Build the stream for running.
     
    Args:
        stream (Stream): A stream instance.
    
    Returns:
        int: The return code. 0 for success, False otherwise.  
    """
    return stream.build()


def runStream(stream: Stream,
              datasetIn: Dataset,
              datasetOut: Dataset,
              timeout: int = 100) -> int:
    """Run the stream in synchronous mode.
     
    Args:
        stream (Stream): The stream instance. 
        datasetIn (Dataset): Dataset with input.
        datasetOut (Dataset): Dataset with output instance. 
        timeout (int): Timeout value(default 100ms).
   
    Returns:
        int: The return code. 0 for success, False otherwise.      
    """
    return stream.run(datasetIn, datasetOut, timeout)


def runStreamAsync(stream: Stream, datasetIn: Dataset,
                   datasetOut: Dataset) -> int:
    """Run the stream in asynchronous mode.
     
    Args:
        stream (Stream): A stream instance.
        input (Dataset): Dataset with input instance.
        output (Dataset): Dataset with output instance.
    
    Returns:
        int: The return code. 0 for success, False otherwise.       
    """
    return stream.runAsync(datasetIn, datasetOut)


def synchronizeStream(stream: Stream, timeout: int = 100) -> int:
    """Synchronize the running of a stream. 
    
    This will block the thread running until completion or timeout expired.
     
    Args:
        stream (Stream): The stream instance.
        timeout (int): Timeout value(default 100ms). Value -1 means never timeout.
    
    Returns:
        int: The return code. 0 for success, False otherwise.   
    """
    return stream.synchronize(timeout)


def synchronizeDevice(devId: int, timeout: int = 100) -> int:
    """Synchronize the running of all stream of a device.
    
    This will block the current thread running until completionor timeout expired.
     
    Args:
        devId (int): Device index which maps to one die on a card. 
        timeout (int): Timeout value(default 100ms). Value -1 means never timeout.
    
    Returns:
        int: The return code. 0 for success, False otherwise.   
    """
    return _vacl.synchronizeDevice(devId, timeout)


def getStreamCacheNumber(stream: Stream) -> int:
    """Get the cache number of a stream.
     
    Args:
        stream (Stream): The stream instance.
    
    Returns:
        int: The return code. 0 for success, False otherwise.   
    """
    return stream.cacheNum


def requestOutputDataset(stream: Stream) -> ModelDataset:
    """Request the output dataset.
     
    Args:
        stream (Stream): The stream instance.
    
    Returns:
        ModelDataset: ModelDataset with output.
    """
    return stream.requestOutputDataset()


def registerGetOutput(stream: Stream, op: Union[Op, OpBase]) -> int:
    """Register a stream operator to the stream in order to get its output after model running.

    Hint:
        If the stream operator is fused into a new stream operator, it will be not available to get the output.
     
    Args:
        stream (Stream): The stream instance.
        op (Union[Op, OpBase]): Vace operator instance whose outputs is that user want to get.
    
    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return stream.registerGetOutput(op)


def registerGetOutputs(
        stream: Stream, ops: Union[Union[Op, List[Op]],
                                   Union[OpBase, List[OpBase]]]) -> int:
    """Register a stream operators to the stream in order to get its output after model running.

    Hint:
        If the stream operator is fused into a new stream operator, it will be not available to get the output.
     
    Args:
        stream (Stream): Stream instance.
        ops (Union[Union[Op, List[Op]], Union[OpBase, List[OpBase]]]):  Vace operator array whose outputs is that user want to get.
    
    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return stream.registerGetOutputs(ops)