# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

__all__ = [
    "ImgDesc", "CvtColorDesc", "NormalDesc", "ScaleDesc", "PaddingDesc",
    "ResizeDesc", "TensorDesc", "CropDesc"
]

from .common import *
from typing import List


class ImgDesc(ImageDesc):
    """A struct that defines image descrption.

    Args:
        imgShape(in): image shape, shoule be [w, h] or [w, h, w_pitch, h_pitch].
        format(in): image format(default vace.IMAGE_TYPE.YUV_NV12).
    """

    def __init__(self,
                 imgShape: List[int],
                 format: IMAGE_TYPE = IMAGE_TYPE.YUV_NV12):
        super().__init__()
        if len(imgShape) == 2:
            self.width = self.widthPitch = imgShape[0]
            self.height = self.heightPitch = imgShape[1]
        elif len(imgShape) == 4:
            self.width, self.height, self.widthPitch, self.heightPitch = imgShape
        else:
            raise RuntimeError(
                "imgShape should be [w, h] or [w, h, w_pitch, h_pitch].")
        self.format = format


class CvtColorDesc():
    """A struct that defines color space descrption.
    
    Args:
        color_cvt_code(COLOR_CVT_CODE): coloe cvt code.
        format(COLOR_SPACE): color space.
    """

    def __init__(self, color_cvt_code: COLOR_CVT_CODE,
                 color_space: COLOR_SPACE):
        self.color_cvt_code = color_cvt_code
        self.color_space = color_space


class ResizeDesc():
    """A struct that defines resize descrption.
    
    Hint:
        In partial fusion operators, the size of reisze is calculated by other operator attributes, 
        so it is possible not to set the dsize value.

    Args:
        type(RESIZE_TYPE): resize type.
        dsize(List[int]): reisze dst shape, should be [w, h], default None.
    """

    def __init__(self, type: RESIZE_TYPE, dsize: List[int] = None):
        self.width, self.height = [0, 0]
        if dsize is not None:
            assert len(dsize) == 2, "dsize should be [w, h]."
            self.width, self.height = dsize
        self.type = type


class NormalDesc():
    """A struct that defines normal descrption.
    
    Args:
        mean(List[float]):mean values, should be [mean0, mean1, mean2].
        std(List[float]):std values, should be [std0, std1, std2].
        type(NORM_TYPE): normal type(default vace.NORM_TYPE.DIV255).
    """

    def __init__(self,
                 mean: List[float],
                 std: List[float],
                 type: NORM_TYPE = NORM_TYPE.DIV255):
        assert len(mean) == len(
            std) == 3, "input should have 3 channels's value"
        self.mean = mean
        self.std = std
        self.type = type


class ScaleDesc():
    """A struct that defines scale descrption.
    
    Args:
        scale(List[float]):scale values, should be [scale0, scale1, scale2].
    """

    def __init__(self, scale: List[float]):
        assert len(scale) == 3, "scale should have 3 channels's value"
        self.scale = scale


class PaddingDesc():
    """A struct that defines padding descrption.
    
    Args:
        padding(List[int]):padding values, should be [padding0, padding1, padding2].
        type(PADDING_TYPE):padding type(default vace.NORM_TYPE.DIV255).
    """

    def __init__(self,
                 padding: List[int],
                 type: PADDING_TYPE = PADDING_TYPE.CONSTANT):
        assert len(
            padding) == 3, "padding_values should have 3 channels's value"
        self.padding = padding
        self.type = type


class TensorDesc():
    """A struct that defines tensor descrption.
    
    Args:
        type(TENSORIZATION_TYPE):tensor type.
    """

    def __init__(self, type: TENSORIZATION_TYPE):
        self.type = type


class CropDesc(CropRect):
    """A struct that defines crop descrption.

    Hint:
        In some fusion operators, the width and height of the crop are calculated through other operator attributes, 
        so it is possible not to set the width and height values

    Args:
        start_x(int):Image Crop start x, should be int value.
        start_y(int):Image Crop start y, should be int value.
        width(int):Image Crop width, should be int value(default None).
        height(int):Image Crop height , should be int value(default None).
    """

    def __init__(self,
                 start_x: int,
                 start_y: int,
                 width: int = None,
                 height: int = None):
        super().__init__()
        self.start_x = start_x
        self.start_y = start_y
        self.width, self.height = [0, 0]
        if width is not None and height is not None:
            self.width = width
            self.height = height