import numpy as np
# from vaststream import vacl,vacm
from typing import Any
from _vaststream_pybind11 import  vacl,vacm,vace

# class callBackStatus():
#     errorCode: int = vacl.callBackeStatusPy.errorCode
#     isStreamEnd: int = vacl.callBackeStatusPy.isStreamEnd

def LoadTestImage(imageFile:str, imageWidth:int, imageHeight:int) -> Any:
    
    return vacl.LoadTestImage(imageFile, imageWidth, imageHeight)

# def HandleOutputDataAsyn(outputHandle:Any, outputSize:int) -> int:
    
#     return vacl.HandleResNet18ResultAsyn(outputHandle, outputSize)
