# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

__all__ = [
    "IMAGE_TYPE", "OP_TYPE", "RESIZE_TYPE", "COLOR_CVT_CODE", "COLOR_SPACE",
    "FLIP_TYPE", "PADDING_TYPE", "WARP_AFFINE_MODE", "DATA_TYPE", "PARAM_TYPE",
    "NORM_TYPE", "TENSORIZATION_TYPE", "ImageDesc", "CropRect", "PaddingValues", 
    "PaddingEdges", "AffineMatrix", "Op", "CustomizedOpInfo"
]

from _vaststream_pybind11 import vace as _vace
from vaststream.vacm.common import PointerContainer
from typing import List
from .utils import *


# =========================== ENUM =============================
class IMAGE_TYPE():
    """An enum that defines image type.

    Contains YUV_NV12, YUV_I420, RGB_PLANAR, RGB888, BGR888, GRAY, FORMAT_BUTT.
    """
    YUV_NV12: int = _vace.imageType.vaceIMG_YUV_NV12
    YUV_I420: int = _vace.imageType.vaceIMG_YUV_I420
    RGB_PLANAR: int = _vace.imageType.vaceIMG_RGB_PLANAR
    RGB888: int = _vace.imageType.vaceIMG_RGB888
    BGR888: int = _vace.imageType.vaceIMG_BGR888
    GRAY: int = _vace.imageType.vaceIMG_RGB888
    FORMAT_BUTT: int = _vace.imageType.vaceIMG_FORMAT_BUTT


class OP_TYPE():
    """An enum that defines op type, the op name consists of specific functions.
    
    Hint: 
        op YUV_NV12_RESIZE_2RGB_NORM_TENSOR mean the input of YUV NV12 type is resized first, then converted to RGB type image, and finally normal operation is performed. 
    
    Contains MEM_COPY_OP, CUSTOMIZED_OP, RESIZE, CROP, CVT_COLOR, BATCH_CROP_RESIZE, WARP_AFFINE, FLIP, SCALE, 
    COPY_MAKE_BOARDER, YUV_NV12_RESIZE_2RGB_NORM_TENSOR, YUV_NV12_CVTCOLOR_RESIZE_NORM_TENSOR, YUV_NV12_RESIZE_CVTCOLOR_CROP_NORM_TENSOR, 
    YUV_NV12_CROP_CVTCOLOR_RESIZE_NORM_TENSOR, YUV_NV12_CVTCOLOR_RESIZE_CROP_NORM_TENSOR, YUV_NV12_CVTCOLOR_LETTERBOX_NORM_TENSOR, 
    YUV_NV12_LETTERBOX_2RGB_NORM_TENSOR, RGB_CVTCOLOR_NORM_TENSOR, RGB_RESIZE_CVTCOLOR_NORM_TENSOR, RGB_RESIZE_CVTCOLOR_CROP_NORM_TENSOR, 
    RGB_CROP_RESIZE_CVTCOLOR_NORM_TENSOR, RGB_LETTERBOX_CVTCOLOR_NORM_TENSOR, MAX_NUM.
    """
    MEM_COPY_OP: int = _vace.opType.vaceOP_MEM_COPY_OP
    CUSTOMIZED_OP: int = _vace.opType.vaceOP_CUSTOMIZED_OP
    BERT_EMBEDDING_OP: int = _vace.opType.vaceOP_BERT_EMBEDDING_OP
    RESIZE: int = _vace.opType.vaceOP_RESIZE
    CROP: int = _vace.opType.vaceOP_CROP
    CVT_COLOR: int = _vace.opType.vaceOP_CVT_COLOR
    BATCH_CROP_RESIZE: int = _vace.opType.vaceOP_BATCH_CROP_RESIZE
    WARP_AFFINE: int = _vace.opType.vaceOP_WARP_AFFINE
    FLIP: int = _vace.opType.vaceOP_FLIP
    SCALE: int = _vace.opType.vaceOP_SCALE
    COPY_MAKE_BORDER: int = _vace.opType.vaceOP_COPY_MAKE_BORDER
    YUV_NV12_RESIZE_2RGB_NORM_TENSOR: int = _vace.opType.vaceOP_FUSION_OP_YUV_NV12_RESIZE_2RGB_NORM_TENSOR
    YUV_NV12_CVTCOLOR_RESIZE_NORM_TENSOR: int = _vace.opType.vaceOP_FUSION_OP_YUV_NV12_CVTCOLOR_RESIZE_NORM_TENSOR
    YUV_NV12_RESIZE_CVTCOLOR_CROP_NORM_TENSOR: int = _vace.opType.vaceOP_FUSION_OP_YUV_NV12_RESIZE_CVTCOLOR_CROP_NORM_TENSOR
    YUV_NV12_CROP_CVTCOLOR_RESIZE_NORM_TENSOR: int = _vace.opType.vaceOP_FUSION_OP_YUV_NV12_CROP_CVTCOLOR_RESIZE_NORM_TENSOR
    YUV_NV12_CVTCOLOR_RESIZE_CROP_NORM_TENSOR: int = _vace.opType.vaceOP_FUSION_OP_YUV_NV12_CVTCOLOR_RESIZE_CROP_NORM_TENSOR
    YUV_NV12_CVTCOLOR_LETTERBOX_NORM_TENSOR: int = _vace.opType.vaceOP_FUSION_OP_YUV_NV12_CVTCOLOR_LETTERBOX_NORM_TENSOR
    YUV_NV12_LETTERBOX_2RGB_NORM_TENSOR: int = _vace.opType.vaceOP_FUSION_OP_YUV_NV12_LETTERBOX_2RGB_NORM_TENSOR
    RGB_CVTCOLOR_NORM_TENSOR: int = _vace.opType.vaceOP_FUSION_OP_RGB_CVTCOLOR_NORM_TENSOR
    RGB_RESIZE_CVTCOLOR_NORM_TENSOR: int = _vace.opType.vaceOP_FUSION_OP_RGB_RESIZE_CVTCOLOR_NORM_TENSOR
    RGB_RESIZE_CVTCOLOR_CROP_NORM_TENSOR: int = _vace.opType.vaceOP_FUSION_OP_RGB_RESIZE_CVTCOLOR_CROP_NORM_TENSOR
    RGB_CROP_RESIZE_CVTCOLOR_NORM_TENSOR: int = _vace.opType.vaceOP_FUSION_OP_RGB_CROP_RESIZE_CVTCOLOR_NORM_TENSOR
    RGB_LETTERBOX_CVTCOLOR_NORM_TENSOR: int = _vace.opType.vaceOP_FUSION_OP_RGB_LETTERBOX_CVTCOLOR_NORM_TENSOR
    MAX_NUM: int = _vace.opType.vaceOP_FUSION_OP_MAX_NUM


class RESIZE_TYPE():
    """An enum that defines resize type.

    Contains NO_RESIZE, BILINEAR, NEAREST, BICUBIC, LANCOZ, BILINEAR_PILLOW, BILINEAR_CV, LANCZOS_PILLOW, 
    LANCZOS_CV, BOX_PILLOW, HAMMING_PILLOW, BICUBIC_PILLOW, BUTT.
    """
    NO_RESIZE: int = _vace.resizeType.vaceRESIZE_NO_RESIZE
    BILINEAR: int = _vace.resizeType.vaceRESIZE_BILINEAR
    NEAREST: int = _vace.resizeType.vaceRESIZE_NEAREST
    BICUBIC: int = _vace.resizeType.vaceRESIZE_BICUBIC
    LANCZOS: int = _vace.resizeType.vaceRESIZE_LANCZOS
    BILINEAR_PILLOW: int = _vace.resizeType.vaceRESIZE_BILINEAR_PILLOW
    BILINEAR_CV: int = _vace.resizeType.vaceRESIZE_BILINEAR_CV
    LANCZOS_PILLOW: int = _vace.resizeType.vaceRESIZE_LANCZOS_PILLOW
    LANCZOS_CV: int = _vace.resizeType.vaceRESIZE_LANCZOS_CV
    BOX_PILLOW: int = _vace.resizeType.vaceRESIZE_BOX_PILLOW
    HAMMING_PILLOW: int = _vace.resizeType.vaceRESIZE_HAMMING_PILLOW
    BICUBIC_PILLOW: int = _vace.resizeType.vaceRESIZE_BICUBIC_PILLOW
    NEAREST_CV: int = _vace.resizeType.vaceRESIZE_NEAREST_CV
    BUTT: int = _vace.resizeType.vaceRESIZE_BUTT


class COLOR_CVT_CODE():
    """An enum that defines color space type code.

    Contains YUV2RGB_NV12, YUV2BGR_NV12, NO_CHANGE, BGR2RGB, RGB2BGR, BGR2RGB_INTERLEAVE2PLANAR, RGB2BGR_INTERLEAVE2PLANAR,
    BGR2BGR_INTERLEAVE2PLANAR, RGB2RGB_INTERLEAVE2PLANAR, YUV2GRAY_NV12, BGR2GRAY_INTERLEAVE, BGR2GRAY_PLANAR, RGB2GRAY_INTERLEAVE,
    RGB2GRAY_PLANAR, RGB2YUV_NV12_PLANAR, BGR2YUV_NV12_PLANAR, CVT_CODE_BUTT.
    """
    YUV2RGB_NV12: int = _vace.colorCvtCode.vaceCOLOR_YUV2RGB_NV12
    YUV2BGR_NV12: int = _vace.colorCvtCode.vaceCOLOR_YUV2BGR_NV12
    NO_CHANGE: int = _vace.colorCvtCode.vaceCOLOR_NO_CHANGE
    BGR2RGB: int = _vace.colorCvtCode.vaceCOLOR_BGR2RGB
    RGB2BGR: int = _vace.colorCvtCode.vaceCOLOR_RGB2BGR
    BGR2RGB_INTERLEAVE2PLANAR: int = _vace.colorCvtCode.vaceCOLOR_BGR2RGB_INTERLEAVE2PLANAR
    RGB2BGR_INTERLEAVE2PLANAR: int = _vace.colorCvtCode.vaceCOLOR_RGB2BGR_INTERLEAVE2PLANAR
    BGR2BGR_INTERLEAVE2PLANAR: int = _vace.colorCvtCode.vaceCOLOR_BGR2BGR_INTERLEAVE2PLANAR
    RGB2RGB_INTERLEAVE2PLANAR: int = _vace.colorCvtCode.vaceCOLOR_RGB2RGB_INTERLEAVE2PLANAR
    YUV2GRAY_NV12: int = _vace.colorCvtCode.vaceCOLOR_YUV2GRAY_NV12
    BGR2GRAY_INTERLEAVE: int = _vace.colorCvtCode.vaceCOLOR_BGR2GRAY_INTERLEAVE
    BGR2GRAY_PLANAR: int = _vace.colorCvtCode.vaceCOLOR_BGR2GRAY_PLANAR
    RGB2GRAY_INTERLEAVE: int = _vace.colorCvtCode.vaceCOLOR_RGB2GRAY_INTERLEAVE
    RGB2GRAY_PLANAR: int = _vace.colorCvtCode.vaceCOLOR_RGB2GRAY_PLANAR
    RGB2YUV_NV12_PLANAR: int = _vace.colorCvtCode.vaceCOLOR_RGB2YUV_NV12_PLANAR
    BGR2YUV_NV12_PLANAR: int = _vace.colorCvtCode.vaceCOLOR_BGR2YUV_NV12_PLANAR
    CVT_CODE_BUTT: int = _vace.colorCvtCode.vaceCOLOR_CVT_CODE_BUTT


class COLOR_SPACE():
    """An enum that defines color space type.

    Contains BT709, BT601, BUTT.
    """
    BT709: int = _vace.colorSpace.vaceCOLOR_SPACE_BT709
    BT601: int = _vace.colorSpace.vaceCOLOR_SPACE_BT601
    BUTT: int = _vace.colorSpace.vaceCOLOR_SPACE_BUTT


class FLIP_TYPE():
    """An enum that defines flip type.

    Contains X_AXIS, Y_AXIS, BOTH_AXES.
    """
    X_AXIS: int = _vace.flipType.vaceFLIP_X_AXIS
    Y_AXIS: int = _vace.flipType.vaceFLIP_Y_AXIS
    BOTH_AXES: int = _vace.flipType.vaceFLIP_BOTH_AXES


class PADDING_TYPE():
    """An enum that defines padding type.

    Contains CONSTANT, REPLICATE, REFLECT, BUTT.
    """
    CONSTANT: int = _vace.paddingType.vaceEDGE_PADDING_TYPE_CONSTANT
    REPLICATE: int = _vace.paddingType.vaceEDGE_PADDING_REPLICATE
    REFLECT: int = _vace.paddingType.vaceEDGE_PADDING_TYPE_REFLECT
    BUTT: int = _vace.paddingType.vaceEDGE_PADDING_TYPE_BUTT


class WARP_AFFINE_MODE():
    """An enum that defines warp affine mode.

    Contains NEAREST, BILINEAR, BUTT.
    """
    NEAREST: int = _vace.warpAffineMode.vaceWARP_AFFINE_MODE_NEAREST
    BILINEAR: int = _vace.warpAffineMode.vaceWARP_AFFINE_MODE_BILINEAR
    BUTT: int = _vace.warpAffineMode.vaceWARP_AFFINE_MODE_BUTT


class DATA_TYPE():
    """An enum that defines data type.

    Contains INT, UINT_8, UINT_16, UINT_32, UINT_64, FLOAT, FLOAT_16, DOUBLE.
    """
    INT: int = _vace.dataType.vaceDT_INT
    UINT_8: int = _vace.dataType.vaceDT_UINT_8
    UINT_16: int = _vace.dataType.vaceDT_UINT_16
    UINT_32: int = _vace.dataType.vaceDT_UINT_32
    UINT_64: int = _vace.dataType.vaceDT_UINT_64
    FLOAT: int = _vace.dataType.vaceDT_FLOAT
    FLOAT_16: int = _vace.dataType.vaceDT_FLOAT_16
    DOUBLE: int = _vace.dataType.vaceDT_DOUBLE


class PARAM_TYPE():
    """An enum that defines param type.

    Contains ELEMENT, ARRAY, TENSOR.
    """
    ELEMENT: int = _vace.paramType.vacePARAM_ELEMENT
    ARRAY: int = _vace.paramType.vacePARAM_ARRAY
    TENSOR: int = _vace.paramType.vacePARAM_TENSOR


class NORM_TYPE():
    """An enum that defines normal type.

    Contains NORMALIZATION_NONE, EQUAL, MINUSMEAN, MINUSMEAN_DIVSTD, DIV255_MINUSMEAN_DIVSTD, 
    DIV1275_MINUSONE, DIV255, NORMALIZATION_NONE_BUTT.
    """
    NORMALIZATION_NONE: int = _vace.normType.vaceNORM_NORMALIZATION_NONE
    EQUAL: int = _vace.normType.vaceNORM_EQUAL
    MINUSMEAN: int = _vace.normType.vaceNORM_MINUSMEAN
    MINUSMEAN_DIVSTD: int = _vace.normType.vaceNORM_MINUSMEAN_DIVSTD
    DIV255_MINUSMEAN_DIVSTD: int = _vace.normType.vaceNORM_DIV255_MINUSMEAN_DIVSTD
    DIV1275_MINUSONE: int = _vace.normType.vaceNORM_DIV1275_MINUSONE
    DIV255: int = _vace.normType.vaceNORM_DIV255
    NORMALIZATION_NONE_BUTT: int = _vace.normType.vaceNORM_NORMALIZATION_NONE_BUTT


class TENSORIZATION_TYPE():
    """An enum that defines tensorization type.

    Contains NONE, UINT8, UINT8_INTERLEAVE, FP16, FP16_INTERLEAVE, FP16_INTERLEAVE_RGB, BUTT.
    """

    NONE: int = _vace.tensorizationType.vaceTENSORIZATION_NONE
    UINT8: int = _vace.tensorizationType.vaceTENSORIZATION_UINT8
    UINT8_INTERLEAVE: int = _vace.tensorizationType.vaceTENSORIZATION_UINT8_INTERLEAVE
    FP16: int = _vace.tensorizationType.vaceTENSORIZATION_FP16
    FP16_INTERLEAVE: int = _vace.tensorizationType.vaceTENSORIZATION_FP16_INTERLEAVE
    FP16_INTERLEAVE_RGB: int = _vace.tensorizationType.vaceTENSORIZATION_FP16_INTERLEAVE_RGB
    BUTT: int = _vace.tensorizationType.vaceTENSORIZATION_TYPE_BUTT


# ================================ STRUCT ============================
class Op(PointerContainer):
    """A struct that defines vace Op Container.
    """
    pass


class CustomizedOpInfo(PointerContainer):
    """A struct that defines customized Op Container.
    """
    pass


class ImageDesc(_vace.imageDesc):
    """A struct that defines image descrption.

    Attributes:
        width(int): The image width.
        height(int): The image height.
        widthPitch(int): The image widthPitch, TODO Detailed explanation.
        heightPitch(int): The image heightPitch, TODO Detailed explanation.
        format(IMAGE_TYPE): The image format type.
    """
    width: int
    height: int
    widthPitch: int
    heightPitch: int
    format: IMAGE_TYPE


class CropRect(_vace.cropRect):
    """A struct that defines crop parameter.

    Attributes:
        start_x(int): The crop coordinate x of upper left corner.
        start_y(int): The crop coordinate x of upper right corner.
        width(int): The crop size width.
        height(int): The crop size height.
    """
    start_x: int
    start_y: int
    width: int
    height: int


class PaddingValues(_vace.paddingValuesPy):
    """A struct that defines padding values.

    Attributes:
        value(List[int]): The value of padding is composed of the padding values of the three RGB channels.

    Examples:
        >>> # padding the three channels of RGB with 114 115 116 respectively
        >>> padding_values = PaddingValues():
        >>> padding_values.value = [114, 115, 116]        
    """
    value: List[int]


class PaddingEdges(_vace.paddingEdges):
    """A struct that defines padding edges.

    Attributes:
        top(int): The height of the padding at the right edge of the image.
        bottom(int): The thickness of the padding at the right edge of the image.
        left(int): The width of the padding at the left edge of the image.
        right(int): The width of the padding at the right edge of the image.
        
    Examples:
        >>> # 10 pixels wide padding on the left and right side of the image, and 20 pixels high padding above and below
        >>> padding_edge = PaddingEdges():
        >>> padding_edge.top = 20
        >>> padding_edge.bottom = 20
        >>> padding_edge.left = 10
        >>> padding_edge.right = 10
    """
    top: int
    bottom: int
    left: int
    right: int


class AffineMatrix(_vace.affineMatrixPy):
    """A struct that defines affine matrix.

    Attributes:
        matrix(List[float]): The value of affine matrix. 
    """
    matrix: List[float]


# ================================ API ============================
# def getVersion() -> str:
#     """ Get the VAME API version information.

#     Returns:
#         str: vace version.
#     """
#     return _vace.getVersion()