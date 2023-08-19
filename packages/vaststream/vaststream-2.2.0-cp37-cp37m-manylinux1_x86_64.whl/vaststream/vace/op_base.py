# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

__all__ = ["OpBase"]

from abc import ABCMeta, abstractmethod
from .common import *
from .op_attr_desc import *
from .op_fusion import *
from typing import Union
from vaststream.vacm.data import Dataset


class OpBase(metaclass=ABCMeta):
    """Op base class.
    
    The is a base class for fusion operator. 
    The class include creating and destroying operators, setting operator attributes, and running operators.
        
    Args:        
        iimage_desc(ImageDesc): Input image descrition.
        oimage_desc(ImageDesc): Output image descrition.
        cvt_color_desc(CvtColorDesc): Color space descrption.
        normal_desc(NormalDesc): Normal descrption.
        scale_desc(ScaleDesc): Scale descrption.
        padding_desc(PaddingDesc): Padding descrption.
        resize_desc(ResizeDesc): Resize descrition.
        tensor_desc(TensorDesc): Tensor descrption.
        crop_desc(CropDesc): Crop descrition.
    """

    def __init__(
        self,
        iimage_desc: ImageDesc = None,
        oimage_desc: ImageDesc = None,
        cvt_color_desc: CvtColorDesc = None,
        normal_desc: NormalDesc = None,
        scale_desc: ScaleDesc = None,
        padding_desc: PaddingDesc = None,
        resize_desc: ResizeDesc = None,
        tensor_desc: TensorDesc = None,
        crop_desc: CropDesc = None,
    ):
        self.iimage_desc = iimage_desc
        self.oimage_desc = oimage_desc
        self.cvt_color_desc = cvt_color_desc
        self.normal_desc = normal_desc
        self.scale_desc = scale_desc
        self.padding_desc = padding_desc
        self.resize_desc = resize_desc
        self.tensor_desc = tensor_desc
        self.crop_desc = crop_desc

        self._op = None
        self.create()

    def __del__(self):
        self.destroy()

    @abstractmethod
    def type(self) -> OP_TYPE:
        """The type of the Op."""
        pass

    def _requires_inputFormat(self) -> bool:
        return False

    @property
    def op(self):
        """Get the Op instance."""
        if self._op is None:
            self.create()
        return self._op

    def create(self) -> None:
        """Create the Op instance.
        """
        if self._op is None:
            self._op = createOp(self.type())
            self._setOpAttr()

    def destroy(self) -> None:
        """Destroy a vaceOp instance.
        """
        if self._op is not None:
            destroyOp(self._op)
            self._op = None

    def _setOpAttr(self) -> None:
        """Set vaceOp Attributes.
        """
        assert self._op is not None, "Please create op."
        if self.iimage_desc:
            assert setOpAttr(self._op, "iimage_width", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT, self.iimage_desc.width) == 0
            assert setOpAttr(self._op, "iimage_height", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT, self.iimage_desc.height) == 0
            assert setOpAttr(self._op, "iimage_width_pitch", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT,
                             self.iimage_desc.widthPitch) == 0
            assert setOpAttr(self._op, "iimage_height_pitch", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT,
                             self.iimage_desc.heightPitch) == 0
            if self._requires_inputFormat():
                assert setOpAttr(self._op, "iimage_format", DATA_TYPE.INT,
                                 PARAM_TYPE.ELEMENT,
                                 self.iimage_desc.format) == 0

        if self.oimage_desc:
            assert setOpAttr(self._op, "oimage_width", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT, self.oimage_desc.width) == 0
            assert setOpAttr(self._op, "oimage_height", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT, self.oimage_desc.height) == 0

        if self.cvt_color_desc:
            assert setOpAttr(self._op, "color_cvt_code", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT,
                             self.cvt_color_desc.color_cvt_code) == 0
            assert setOpAttr(self._op, "color_space", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT,
                             self.cvt_color_desc.color_space) == 0

        if self.resize_desc:
            assert setOpAttr(self._op, "resize_type", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT, self.resize_desc.type) == 0
            if self.resize_desc.width and self.resize_desc.height:
                assert setOpAttr(self._op, "resize_width", DATA_TYPE.INT,
                                 PARAM_TYPE.ELEMENT,
                                 self.resize_desc.width) == 0
                assert setOpAttr(self._op, "resize_height", DATA_TYPE.INT,
                                 PARAM_TYPE.ELEMENT,
                                 self.resize_desc.height) == 0

        if self.padding_desc:
            assert setOpAttr(self._op, "padding0", DATA_TYPE.UINT_8,
                             PARAM_TYPE.ELEMENT,
                             self.padding_desc.padding[0]) == 0
            assert setOpAttr(self._op, "padding1", DATA_TYPE.UINT_8,
                             PARAM_TYPE.ELEMENT,
                             self.padding_desc.padding[1]) == 0
            assert setOpAttr(self._op, "padding2", DATA_TYPE.UINT_8,
                             PARAM_TYPE.ELEMENT,
                             self.padding_desc.padding[2]) == 0
            assert setOpAttr(self._op, "edge_padding_type", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT, self.padding_desc.type) == 0

        if self.normal_desc:
            assert setOpAttr(self._op, "mean0", DATA_TYPE.FLOAT,
                             PARAM_TYPE.ELEMENT, self.normal_desc.mean[0]) == 0
            assert setOpAttr(self._op, "mean1", DATA_TYPE.FLOAT,
                             PARAM_TYPE.ELEMENT, self.normal_desc.mean[1]) == 0
            assert setOpAttr(self._op, "mean2", DATA_TYPE.FLOAT,
                             PARAM_TYPE.ELEMENT, self.normal_desc.mean[2]) == 0
            assert setOpAttr(self._op, "std0", DATA_TYPE.FLOAT,
                             PARAM_TYPE.ELEMENT, self.normal_desc.std[0]) == 0
            assert setOpAttr(self._op, "std1", DATA_TYPE.FLOAT,
                             PARAM_TYPE.ELEMENT, self.normal_desc.std[1]) == 0
            assert setOpAttr(self._op, "std2", DATA_TYPE.FLOAT,
                             PARAM_TYPE.ELEMENT, self.normal_desc.std[2]) == 0
            assert setOpAttr(self._op, "norma_type", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT, self.normal_desc.type) == 0

        if self.scale_desc:
            assert setOpAttr(self._op, "scale0", DATA_TYPE.FLOAT,
                             PARAM_TYPE.ELEMENT, self.scale_desc.scale[0]) == 0
            assert setOpAttr(self._op, "scale1", DATA_TYPE.FLOAT,
                             PARAM_TYPE.ELEMENT, self.scale_desc.scale[1]) == 0
            assert setOpAttr(self._op, "scale2", DATA_TYPE.FLOAT,
                             PARAM_TYPE.ELEMENT, self.scale_desc.scale[2]) == 0

        if self.crop_desc:
            assert setOpAttr(self._op, "crop_x", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT, self.crop_desc.start_x) == 0
            assert setOpAttr(self._op, "crop_y", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT, self.crop_desc.start_y) == 0
            if self.crop_desc.width and self.crop_desc.height:
                assert setOpAttr(self._op, "crop_width", DATA_TYPE.INT,
                                 PARAM_TYPE.ELEMENT, self.crop_desc.width) == 0
                assert setOpAttr(self._op, "crop_height", DATA_TYPE.INT,
                                 PARAM_TYPE.ELEMENT,
                                 self.crop_desc.height) == 0

        if self.tensor_desc:
            assert setOpAttr(self._op, "tensor_type0", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT, self.tensor_desc.type) == 0

    def setAttr(self, attrName: str, attrDType: DATA_TYPE,
                attrGType: PARAM_TYPE, value: Union[int, float]) -> int:
        """Set attributes of a specified op.
    
        Args:
            attrName(str): the attribute name.
            attrDType(DATA_TYPE): data type of attribute.
            attrGType(PARAM_TYPE): the attribute type (PARAM_ELEMENT | PARAM_ARRAY).
            value(Union[int, float]): the value of attribute.
        
        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        assert self._op is not None, "Please create op."
        return setOpAttr(self._op, attrName, attrDType, attrGType, value)

    def setAttrArray(self, attrName: str, attrDType: DATA_TYPE,
                     attrGType: PARAM_TYPE, value: Union[int, float],
                     index: int) -> int:
        """Set attributes of a specified op.\n

        Args:
            op(Op): The specified vace op, create by API createOp.
            attrName(str): The attribute name.
            attrDType(DATA_TYPE): Data type of attribute.
            attrGType(PARAM_TYPE): The attribute type (PARAM_ELEMENT | PARAM_ARRAY).
            value(Union[int, float]): The value of attribute.
        
        Return:
            int: The return code. 0 for success, False otherwise.
        """
        assert self._op is not None, "Please create op."
        return setOpAttrArray(self._op, attrName, attrDType, attrGType, value,
                              index)

    def getAttr(self, attrName: str,
                attrDType: DATA_TYPE) -> Union[int, float]:
        """Set attributes of a specified op.
        
        Args:
            attrName(str): The attribute name.
            attrDType(DATA_TYPE): Data type of attribute.
    
        Returns:
            Union[int, float]: Op attribute.
        """
        assert self._op is not None, "Please create op."
        return getOpAttr(self._op, attrName, attrDType)

    def getAttrArray(self, attrName: str, attrDType: DATA_TYPE,
                     index: int) -> Union[int, float]:
        """Get attributes of a specified op.
        
        Args:
            op(Op): The specified vace op, create by API createOp.
            attrName(str): The attribute name.
            attrDType(str): Data type of attribute.
            attrGType(PARAM_TYPE): the attribute type (PARAM_ELEMENT | PARAM_ARRAY).
            index(int): The index of array element.

        Return: 
            Union[int, float]: the value of attribute.
        """
        assert self._op is not None, "Please create op."
        return getOpAttrArray(self._op, attrName, attrDType, index)

    def execute(self, input: Dataset, output: Dataset) -> int:
        """ExecuteOp op with input dataset.

        Args:
            input(Dataset): vacmDataset of input data.
            output(Dataset): vacmDataset of output data.

        Return:
            int: The return code. 0 for success, False otherwise.
        """
        assert self._op is not None, "Please create op."
        return executeOp(self._op, input, output)

    def resetInImageDesc(self, iimage_desc: ImageDesc) -> None:
        """Reset Input ImageDesc.
        
        Args:
            iimage_desc(ImageDesc): New ImageDesc.
        """
        assert self._op is not None, "Please create op."
        assert setOpAttr(self._op, "iimage_width", DATA_TYPE.INT,
                         PARAM_TYPE.ELEMENT, iimage_desc.width) == 0
        assert setOpAttr(self._op, "iimage_height", DATA_TYPE.INT,
                         PARAM_TYPE.ELEMENT, iimage_desc.height) == 0
        assert setOpAttr(self._op, "iimage_width_pitch", DATA_TYPE.INT,
                         PARAM_TYPE.ELEMENT, iimage_desc.widthPitch) == 0
        assert setOpAttr(self._op, "iimage_height_pitch", DATA_TYPE.INT,
                         PARAM_TYPE.ELEMENT, iimage_desc.heightPitch) == 0

    def resetOutImageDesc(self, oimage_desc: ImageDesc) -> None:
        """Reset Output ImageDesc.
        
        Args:
            oimage_desc(ImageDesc): New ImageDesc.
        """
        assert self._op is not None, "Please create op."

        assert setOpAttr(self._op, "oimage_width", DATA_TYPE.INT,
                         PARAM_TYPE.ELEMENT, oimage_desc.width) == 0
        assert setOpAttr(self._op, "oimage_height", DATA_TYPE.INT,
                         PARAM_TYPE.ELEMENT, oimage_desc.height) == 0

    def resetCvtColor(self, cvt_color_desc: CvtColorDesc) -> None:
        """Reset CvtColorDesc.
        
        Args:
            cvt_color_desc(CvtColorDesc): New CvtColorDesc.
        """
        assert self._op is not None, "Please create op."
        assert self.cvt_color_desc is not None, "Op not have attribute cvtColor."
        assert setOpAttr(self._op, "color_cvt_code", DATA_TYPE.INT,
                         PARAM_TYPE.ELEMENT,
                         cvt_color_desc.color_cvt_code) == 0
        assert setOpAttr(self._op, "color_space", DATA_TYPE.INT,
                         PARAM_TYPE.ELEMENT, cvt_color_desc.color_space) == 0

    def resetNormalDesc(self, normal_desc: NormalDesc) -> None:
        """Reset NormalDesc.
        
        Args:
            normal_desc(NormalDesc): New NormalDesc.
        """
        assert self._op is not None, "Please create op."
        assert setOpAttr(self._op, "mean0", DATA_TYPE.FLOAT,
                         PARAM_TYPE.ELEMENT, normal_desc.mean[0]) == 0
        assert setOpAttr(self._op, "mean1", DATA_TYPE.FLOAT,
                         PARAM_TYPE.ELEMENT, normal_desc.mean[1]) == 0
        assert setOpAttr(self._op, "mean2", DATA_TYPE.FLOAT,
                         PARAM_TYPE.ELEMENT, normal_desc.mean[2]) == 0
        assert setOpAttr(self._op, "std0", DATA_TYPE.FLOAT, PARAM_TYPE.ELEMENT,
                         normal_desc.std[0]) == 0
        assert setOpAttr(self._op, "std1", DATA_TYPE.FLOAT, PARAM_TYPE.ELEMENT,
                         normal_desc.std[1]) == 0
        assert setOpAttr(self._op, "std2", DATA_TYPE.FLOAT, PARAM_TYPE.ELEMENT,
                         normal_desc.std[2]) == 0
        assert setOpAttr(self._op, "norma_type", DATA_TYPE.INT,
                         PARAM_TYPE.ELEMENT, normal_desc.type) == 0

    def resetScaleDesc(self, scale_desc: ScaleDesc) -> None:
        """Reset ScaleDesc.
        
        Args:
            scale_desc(ScaleDesc): New ScaleDesc.
        """
        assert self._op is not None, "Please create op."
        assert setOpAttr(self._op, "scale0", DATA_TYPE.FLOAT,
                         PARAM_TYPE.ELEMENT, scale_desc.scale[0]) == 0
        assert setOpAttr(self._op, "scale1", DATA_TYPE.FLOAT,
                         PARAM_TYPE.ELEMENT, scale_desc.scale[1]) == 0
        assert setOpAttr(self._op, "scale2", DATA_TYPE.FLOAT,
                         PARAM_TYPE.ELEMENT, scale_desc.scale[2]) == 0

    def resetPaddingDesc(self, padding_desc: PaddingDesc) -> None:
        """Reset PaddingDesc.
        
        Args:
            padding_desc(PaddingDesc): New PaddingDesc.
        """
        assert self._op is not None, "Please create op."
        assert self.padding_desc is not None, "Op not have attribute padding."
        assert setOpAttr(self._op, "padding0", DATA_TYPE.UINT_8,
                         PARAM_TYPE.ELEMENT, padding_desc.padding[0]) == 0
        assert setOpAttr(self._op, "padding1", DATA_TYPE.UINT_8,
                         PARAM_TYPE.ELEMENT, padding_desc.padding[1]) == 0
        assert setOpAttr(self._op, "padding2", DATA_TYPE.UINT_8,
                         PARAM_TYPE.ELEMENT, padding_desc.padding[2]) == 0
        assert setOpAttr(self._op, "edge_padding_type", DATA_TYPE.INT,
                         PARAM_TYPE.ELEMENT, padding_desc.type) == 0

    def resetResizeDesc(self, resize_desc: ResizeDesc) -> None:
        """Reset ResizeDesc.
        
        Args:
            resize_desc(ResizeDesc): New ResizeDesc.
        """
        assert self._op is not None, "Please create op."
        assert self.resize_desc is not None, "Op not have attribute resize."

        assert setOpAttr(self._op, "resize_type", DATA_TYPE.INT,
                         PARAM_TYPE.ELEMENT, resize_desc.type) == 0
        if resize_desc.width and resize_desc.height:
            assert setOpAttr(self._op, "resize_width", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT, resize_desc.width) == 0
            assert setOpAttr(self._op, "resize_height", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT, resize_desc.height) == 0

    def resetTensorDesc(self, tensor_desc: TensorDesc) -> None:
        """Reset TensorDesc.
        
        Args:
            tensor_desc(TensorDesc): New TensorDesc.
        """
        assert self._op is not None, "Please create op."
        assert setOpAttr(self._op, "tensor_type0", DATA_TYPE.INT,
                         PARAM_TYPE.ELEMENT, tensor_desc.type) == 0

    def resetCropDesc(self, crop_desc: CropDesc) -> None:
        """Reset CropDesc.
        
        Args:
            crop_desc(CropDesc): New CropDesc.
        """
        assert self._op is not None, "Please create op."
        assert self.crop_desc is not None, "Op not have attribute crop."
        assert setOpAttr(self._op, "crop_x", DATA_TYPE.INT, PARAM_TYPE.ELEMENT,
                         crop_desc.start_x) == 0
        assert setOpAttr(self._op, "crop_y", DATA_TYPE.INT, PARAM_TYPE.ELEMENT,
                         crop_desc.start_y) == 0
        if crop_desc.width and crop_desc.height:
            assert setOpAttr(self._op, "crop_width", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT, crop_desc.width) == 0
            assert setOpAttr(self._op, "crop_height", DATA_TYPE.INT,
                             PARAM_TYPE.ELEMENT, crop_desc.height) == 0
