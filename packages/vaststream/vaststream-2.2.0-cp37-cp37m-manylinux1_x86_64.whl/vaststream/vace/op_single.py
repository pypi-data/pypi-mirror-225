# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

__all__ = [
    "resize", "crop", "yuvFlip", "warpAffine", "cvtColor",
    "resizeCopyMakeBorder", "batchCropResize", "scale"
]

from _vaststream_pybind11 import vace as _vace
from typing import List
from .common import *
from .utils import *
from vaststream.vacm.data import DataHandle

# =========================== API =============================


@err_check
def resize(resizeType: RESIZE_TYPE, inputImageDesc: ImageDesc,
           inputHandle: DataHandle, outputImageDesc: ImageDesc,
           outputHandle: DataHandle) -> int:
    """Resize the input image to the output image size.
    
    Args:
        resizeType(RESIZE_TYPE): Resize type.
        inputImageDesc(ImageDesc): The description of input image.
        inputHandle(DataHandle): Data handle of the input image.
        outputImageDesc(ImageDesc): The description of output image.
        outputHandle(DataHandle): Data handle of the output image.
        
    Return:
        int: The return code. 0 for success, False otherwise.
    """
    input_ptr_ = inputHandle.ptr
    output_ptr_ = outputHandle.ptr
    return _vace.resize(resizeType, inputImageDesc, input_ptr_,
                        outputImageDesc, output_ptr_)


@err_check
def crop(cropRect: CropRect, inputImageDesc: ImageDesc,
         inputHandle: DataHandle, outputImageDesc: ImageDesc,
         outputHandle: DataHandle) -> int:
    """Crop from the input image to get the output image.
    
    Args:
        cropRect(CropRect): Crop rectangle.
        inputImageDesc(ImageDesc): The description of input image.
        inputHandle(DataHandle): Data handle of the input image.
        outputImageDesc(ImageDesc): The description of output image.
        outputHandle(DataHandle): Data handle of the output image.
        
    Return:
        int: The return code. 0 for success, False otherwise.
    """
    input_ptr_ = inputHandle.ptr
    output_ptr_ = outputHandle.ptr
    return _vace.crop(cropRect, inputImageDesc, input_ptr_, outputImageDesc,
                      output_ptr_)


@err_check
def yuvFlip(flipType: FLIP_TYPE, inputImageDesc: ImageDesc,
            inputHandle: DataHandle, outputImageDesc: ImageDesc,
            outputHandle: DataHandle) -> int:
    """Flip the input image.
    
    Args:
        flipType(FLIP_TYPE): Flip type.
        inputImageDesc(ImageDesc): The description of input image.
        inputHandle(DataHandle): Data handle of the input image.
        outputImageDesc(ImageDesc): The description of output image.
        outputHandle(DataHandle): Data handle of the output image.
        
    Return:
        int: The return code. 0 for success, False otherwise.
    """
    input_ptr_ = inputHandle.ptr
    output_ptr_ = outputHandle.ptr
    return _vace.yuvFlip(flipType, inputImageDesc, input_ptr_, outputImageDesc,
                         output_ptr_)


@err_check
def warpAffine(affineMatrixPy: AffineMatrix, warpAffineMode: WARP_AFFINE_MODE,
               borderMode: PADDING_TYPE, borderValuesPy: PaddingValues,
               inputImageDesc: ImageDesc, inputHandle: DataHandle,
               outputImageDesc: ImageDesc, outputHandle: DataHandle) -> int:
    """Affine transformation of the input image.
    
    Args:
        affineMatrixPy(AffineMatrix): affine transformation matrix.
        warpAffineMode(WARP_AFFINE_MODE): warp affine mode.
        borderMode(PADDING_TYPE): border value.
        borderValuesPy(PaddingValues): the description of input image.
        inputImageDesc(ImageDesc): The description of input image.
        inputHandle(DataHandle): Data handle of the input image.
        outputImageDesc(ImageDesc): The description of output image.
        outputHandle(DataHandle): Data handle of the output image.
        
    Return:
        int: The return code. 0 for success, False otherwise.
    """
    input_ptr_ = inputHandle.ptr
    output_ptr_ = outputHandle.ptr
    return _vace.warpAffine(affineMatrixPy, warpAffineMode, borderMode,
                            borderValuesPy, inputImageDesc, input_ptr_,
                            outputImageDesc, output_ptr_)


@err_check
def cvtColor(cvtType: COLOR_CVT_CODE, cvtColorSpace: COLOR_SPACE,
             inputImageDesc: ImageDesc, inputHandle: DataHandle,
             outputImageDesc: ImageDesc, outputHandle: DataHandle) -> int:
    """Covert input image color according to cvt color config.
    
    Args:
        cvtType(COLOR_CVT_CODE0): Color code type.
        cvtColorSpace (COLOR_SPACE): Convert color space.
        inputImageDesc(ImageDesc): The description of input image.
        inputHandle(DataHandle): Data handle of the input image.
        outputImageDesc(ImageDesc): The description of output image.
        outputHandle(DataHandle): Data handle of the output image.
    
    Return:
        int: The return code. 0 for success, False otherwise.
    """
    input_ptr_ = inputHandle.ptr
    output_ptr_ = outputHandle.ptr
    return _vace.cvtColor(cvtType, cvtColorSpace, inputImageDesc, input_ptr_,
                          outputImageDesc, output_ptr_)


@err_check
def resizeCopyMakeBorder(resizeType: RESIZE_TYPE, paddingType: PADDING_TYPE,
                         paddingValues: List[int], paddingEdges: PaddingEdges,
                         inputImageDesc: ImageDesc, inputHandle: DataHandle,
                         outputImageDesc: ImageDesc,
                         outputHandle: DataHandle) -> int:
    """Resize and make border to the input image.
    
    Args:
        resizeType(RESIZE_TYPE): Resize type.
        paddingType(PADDING_TYPE): Padding type.
	    paddingValues(List[int]): Padding values.
        paddingEdges(PaddingEdges): Padding edges: left, right, top, bottom.
        inputImageDesc(ImageDesc): The description of input image.
        inputHandle(DataHandle): Data handle of the input image.
        outputImageDesc(ImageDesc): The description of output image.
        outputHandle(DataHandle): Data handle of the output image.
    
    Return:
        int: The return code. 0 for success, False otherwise.
    """
    input_ptr_ = inputHandle.ptr
    output_ptr_ = outputHandle.ptr
    return _vace.resizeCopyMakeBorder(resizeType, paddingType, paddingValues,
                                      paddingEdges, inputImageDesc, input_ptr_,
                                      outputImageDesc, output_ptr_)


@err_check
def batchCropResize(cropRects: List[CropRect], resizeType: RESIZE_TYPE,
                    inputImageDesc: ImageDesc, inputHandle: DataHandle,
                    outputImageDesc: ImageDesc,
                    outputHandle: List[DataHandle]) -> int:
    """Batch crop the input image using cropRects settings, then all resize to the output image size.
    
    Args:
        cropRects(List[CropRect]): list of crop rectangles. size is cropNum.
        resizeType(RESIZE_TYPE): resize type.\n
        inputImageDesc(ImageDesc): The description of input image.
        inputHandle(DataHandle): Data handle of the input image.
        outputImageDesc(ImageDesc): The description of output image.
        outputHandle(DataHandle): Data handle of the output image.
    
    Return:
        int: The return code. 0 for success, False otherwise.
    """
    input_ptr_ = inputHandle.ptr
    output_ptr_list_ = [output_ptr_.ptr for output_ptr_ in outputHandle]
    return _vace.batchCropResize(cropRects, resizeType, inputImageDesc,
                                 input_ptr_, outputImageDesc, output_ptr_list_)


@err_check
def scale(resizeType: RESIZE_TYPE, inputImageDesc: List[ImageDesc],
          inputHandle: DataHandle, outputImageDesc: ImageDesc,
          outputHandle: List[DataHandle]) -> int:
    """Scale the input image to output images. Only YUV images are supported at now.
    
    Args:
        resizeType(RESIZE_TYPE): resize type. only vace_RESIZE_BILINEAR is supported at now.\n
        outputCount(List[ImageDesc]): output count. Maximum output is 16.\n
        inputImageDesc(ImageDesc): The description of input image.
        inputHandle(DataHandle): Data handle of the input image.
        outputImageDesc(ImageDesc): The description of output image.
        outputHandle(DataHandle): Data handle of the output image.
    
    Return:
        int: The return code. 0 for success, False otherwise.
    """
    input_ptr_ = inputHandle.ptr
    output_ptr_list_ = [output_ptr_.ptr for output_ptr_ in outputHandle]
    return _vace.scale(resizeType, inputImageDesc, input_ptr_, outputImageDesc,
                       output_ptr_list_)
