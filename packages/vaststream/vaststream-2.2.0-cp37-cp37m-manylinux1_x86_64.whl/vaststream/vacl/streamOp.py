import numpy as np
# from vaststream import vacl,vacm,vace
from typing import Any
from _vaststream_pybind11 import  vacl,vacm,vace

# 返回值校验
def err_checker(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if ret != vacl.vaclER_SUCCESS:
            raise Exception(f"{func.__name__} return error.")
    return wrapper

def createGraphInputOp(graph: Any, inputCnt: int) -> Any:
    """
    create the vacl input op
    * \param graph [in]: Pointer to a graph instance.
    * \param inputCnt [in]: input number of a stream per batch .
    """
    return vacl.createGraphInputOp(graph, inputCnt)

@err_checker
def connectOps(parent:Any, child:Any) -> int:
    """
    connect the vacl op
    * \param parent [in]: Pointer to the operator instance to be connected as parent node.
    * \param child [in]: Pointer to the operator instance to be connected as child node.
    """
    return vacl.connectOps(parent, child)

def createRunModelOp(model: Any) -> Any:
    """
    create the vacl run model op
     * \param model [in]: Pointer to model instance.
    """
    return vacl.createRunModelOp(model)


@err_checker
def registerGetOutput(stream: Any, op: Any) -> int:
    """
    Register a stream operator to the stream in order to get its output after model running.
    * \param stream [in]: Pointer to a stream instance.
    * \param op [in]: Pointer to a vace operator instance whose outputs is that user want to get.
    """
    return vacl.registerGetOutput(stream, op)

@err_checker
def registerGetOutputs(stream: Any, ops: Any, opCount:int) -> int:
    """
     Register a stream operators to the stream in order to get its output after model running.
    * \param stream [in]: Pointer to a stream instance.
    * \param ops [in]: Pointer to a vace operator array whose outputs is that user want to get.
    * \param opCount [in]: the size of the vace operator array.
    """
    return vacl.registerGetOutput(stream, ops, opCount)