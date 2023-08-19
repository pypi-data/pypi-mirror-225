# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

__all__ = [
    "CODEC_TYPE",
    "SOURCE_MODE",
    "MEMORY_TYPE",
    "PIXEL_FORMAT",
    "STATE",
    "VIDEO_FIELD",
    "FRAME_TYPE",
    "CHROMA_FORMAT",
    "JPEG_CODING_MODE",
    "VIDEO_PROFILE",
    "VIDEO_LEVEL",
    "DECODE_MODE",
    "ENC_QUALITY_MODE",
    "ENC_TUNE_TYPE",
    "ENC_QP_TYPE",
    "ENC_SEI_NAL_TYPE",
    "Stream",
    "CropInfo",
    "Frame",
    "HardwareID",
    "Rational",
    "DecChannelParamters",
    "DecStreamInfo",
    "DecJpegInfo",
    "DecStatus",
    "DecOutputOptions",
    "DecVideoInfo",
    "JpegDecCapability",
    "VideoDecCapability",
    "EncExternalSEI",
    "EncPictureArea",
    "EncPictureROI",
    "EncExtendedParams",
    "EncVideoConfiguration",
    "EncJPEGConfiguration",
    "EncChannelParamters",
    "EncOutputOptions",
    "WARN_MORE_DATA",
    "WARN_EOS",
    "DEC_MAX_PIX_FMT_NUM",
    "DEC_MAX_CODING_MODE_NUM",
    "DEC_JPEG_MAX_WIDTH",
    "DEC_JPEG_MAX_HEIGHT",
    "DEC_JPEG_MIN_WIDTH",
    "DEC_JPEG_MIN_HEIGHT",
    "DEC_VIDEO_MAX_WIDTH",
    "DEC_VIDEO_MAX_HEIGHT",
    "DEC_VIDEO_MIN_WIDTH",
    "DEC_VIDEO_MIN_HEIGHT",
    "DEC_MAX_STREAM_BUFFER_SIZE",
    "ENC_MAX_STRM_BUF_NUM",
    "ENC_MAX_REF_FRAMES",
    "ENC_MAX_GOP_SIZE",
    "ENC_MAX_LTR_FRAMES",
    "ENC_MAX_ROI_NUM",
    "ENC_DEFAULT_PAR",
    "ENC_VIDEO_MAX_HEIGHT",
    "ENC_VIDEO_MAX_WIDTH",
    "ENC_VIDEO_MIN_HEIGHT",
    "ENC_VIDEO_MIN_WIDTH",
    "ENC_JPEG_MAX_HEIGHT",
    "ENC_JPEG_MAX_WIDTH",
    "ENC_JPEG_MIN_HEIGHT",
    "ENC_JPEG_MIN_WIDTH",
    "ENC_MAX_OUTBUF_NUM",
    "systemInitialize",
    "systemUninitialize"
]

from _vaststream_pybind11 import vame as _vame
import numpy as np
from .utils import *
from typing import List, Union, Any

# =========================== ENUM =============================


class CODEC_TYPE():
    """An enum that defines codec types.

    Contains DEC_JPEG, DEC_H264, DEC_HEVC, ENC_JPEG, ENC_H264, ENC_HEVC.
    """
    DEC_JPEG: int = _vame.codecType.VAME_CODEC_DEC_JPEG
    DEC_H264: int = _vame.codecType.VAME_CODEC_DEC_H264
    DEC_HEVC: int = _vame.codecType.VAME_CODEC_DEC_HEVC
    ENC_JPEG: int = _vame.codecType.VAME_CODEC_ENC_JPEG
    ENC_H264: int = _vame.codecType.VAME_CODEC_ENC_H264
    ENC_HEVC: int = _vame.codecType.VAME_CODEC_ENC_HEVC


class SOURCE_MODE():
    """An enum that defines source mode.

    Contains SRC_FRAME.
    """
    SRC_FRAME: int = _vame.sourceMode.VAME_SRC_FRAME


class MEMORY_TYPE():
    """An enum that defines memory type.

    Contains DEVICE, HOST, FLUSH.
    """
    DEVICE: int = _vame.memoryType.VAME_MEM_DEVICE
    HOST: int = _vame.memoryType.VAME_MEM_HOST
    FLUSH: int = _vame.memoryType.VAME_MEM_FLUSH


class PIXEL_FORMAT():
    """An enum that defines pixel format.

    Important:
        Vame's decoder and encoder only support nv12.

    Contains NONE, YUV420P, YUV444P, YUV422P, YUV420P9, YUV422P9, YUV444P9,
    YUV420P10, YUV422P10, YUV444P10, YUV420P12, YUV422P12, YUV444P12,
    NV12, NV21, GRAY8, GRAY9, GRAY10, GRAY12, RGB24, BGR24, ARGB, RGBA, ABGR, BGRA.
    """
    NONE: int = _vame.pixelFormat.VAME_PIX_FMT_NONE
    YUV420P: int = _vame.pixelFormat.VAME_PIX_FMT_YUV420P
    YUV444P: int = _vame.pixelFormat.VAME_PIX_FMT_YUV444P
    YUV422P: int = _vame.pixelFormat.VAME_PIX_FMT_YUV422P
    YUV420P9: int = _vame.pixelFormat.VAME_PIX_FMT_YUV420P9
    YUV422P9: int = _vame.pixelFormat.VAME_PIX_FMT_YUV422P9
    YUV444P9: int = _vame.pixelFormat.VAME_PIX_FMT_YUV444P9
    YUV420P10: int = _vame.pixelFormat.VAME_PIX_FMT_YUV420P10
    YUV422P10: int = _vame.pixelFormat.VAME_PIX_FMT_YUV422P10
    YUV444P10: int = _vame.pixelFormat.VAME_PIX_FMT_YUV444P10
    YUV420P12: int = _vame.pixelFormat.VAME_PIX_FMT_YUV420P12
    YUV422P12: int = _vame.pixelFormat.VAME_PIX_FMT_YUV422P12
    YUV444P12: int = _vame.pixelFormat.VAME_PIX_FMT_YUV444P12
    NV12: int = _vame.pixelFormat.VAME_PIX_FMT_NV12
    NV21: int = _vame.pixelFormat.VAME_PIX_FMT_NV21
    GRAY8: int = _vame.pixelFormat.VAME_PIX_FMT_GRAY8
    GRAY9: int = _vame.pixelFormat.VAME_PIX_FMT_GRAY9
    GRAY10: int = _vame.pixelFormat.VAME_PIX_FMT_GRAY10
    GRAY12: int = _vame.pixelFormat.VAME_PIX_FMT_GRAY12
    RGB24: int = _vame.pixelFormat.VAME_PIX_FMT_RGB24
    BGR24: int = _vame.pixelFormat.VAME_PIX_FMT_BGR24
    ARGB: int = _vame.pixelFormat.VAME_PIX_FMT_ARGB
    RGBA: int = _vame.pixelFormat.VAME_PIX_FMT_RGBA
    ABGR: int = _vame.pixelFormat.VAME_PIX_FMT_ABGR
    BGRA: int = _vame.pixelFormat.VAME_PIX_FMT_BGRA


class STATE():
    """An enum that defines state.

    Contains ST_NONE, ST_READY, ST_RUNNING, ST_ERROR, ST_STOPPING, ST_STOPPED.
    """
    ST_NONE: int = _vame.state.VAME_ST_NONE
    ST_READY: int = _vame.state.VAME_ST_READY
    ST_RUNNING: int = _vame.state.VAME_ST_RUNNING
    ST_ERROR: int = _vame.state.VAME_ST_ERROR
    ST_STOPPING: int = _vame.state.VAME_ST_STOPPING
    ST_STOPPED: int = _vame.state.VAME_ST_STOPPED


class VIDEO_FIELD():
    """An enum that defines video field.

    Contains FLD_FRAME.
    """
    FLD_FRAME: int = _vame.videoField.VAME_FLD_FRAME


class FRAME_TYPE():
    """An enum that defines frame type.

    Contains I, P, B.
    """
    I: int = _vame.frameType.VAME_FRM_I
    P: int = _vame.frameType.VAME_FRM_P
    B: int = _vame.frameType.VAME_FRM_B


class CHROMA_FORMAT():
    """An enum that defines chrome format.

    Contains FMT_NONE, FMT_400, FMT_411, FMT_420, FMT_422, FMT_440, FMT_444.
    """
    FMT_NONE: int = _vame.chromaFormat.VAME_CHROMA_FMT_NONE
    FMT_400: int = _vame.chromaFormat.VAME_CHROMA_FMT_400
    FMT_411: int = _vame.chromaFormat.VAME_CHROMA_FMT_411
    FMT_420: int = _vame.chromaFormat.VAME_CHROMA_FMT_420
    FMT_422: int = _vame.chromaFormat.VAME_CHROMA_FMT_422
    FMT_440: int = _vame.chromaFormat.VAME_CHROMA_FMT_440
    FMT_444: int = _vame.chromaFormat.VAME_CHROMA_FMT_444


class JPEG_CODING_MODE():
    """An enum that defines jpeg coding mode.

    Contains NONE, BASELINE, PROGRESSIVE, NONINTERLEAVED.
    """
    NONE: int = _vame.jpegCodingMode.VAME_JPEG_NONE
    BASELINE: int = _vame.jpegCodingMode.VAME_JPEG_BASELINE
    PROGRESSIVE: int = _vame.jpegCodingMode.VAME_JPEG_PROGRESSIVE
    NONINTERLEAVED: int = _vame.jpegCodingMode.VAME_JPEG_NONINTERLEAVED


class VIDEO_PROFILE():
    """An enum that defines video profile.

    Contains HEVC_MAIN_STILL_PICTURE, HEVC_MAIN, HEVC_MAIN_10, HEVC_MAIN_REXT,
    H264_BASELINE, H264_MAIN, H264_HIGH, H264_HIGH_10, AV1_MAIN, AV1_HIGH, AV1_PROFESSIONAL.
    """
    HEVC_MAIN_STILL_PICTURE: int = _vame.videoProfile.VAME_VIDEO_PRFL_HEVC_MAIN_STILL_PICTURE
    HEVC_MAIN: int = _vame.videoProfile.VAME_VIDEO_PRFL_HEVC_MAIN
    HEVC_MAIN_10: int = _vame.videoProfile.VAME_VIDEO_PRFL_HEVC_MAIN_10
    HEVC_MAIN_REXT: int = _vame.videoProfile.VAME_VIDEO_PRFL_HEVC_MAIN_REXT
    H264_BASELINE: int = _vame.videoProfile.VAME_VIDEO_PRFL_H264_BASELINE
    H264_MAIN: int = _vame.videoProfile.VAME_VIDEO_PRFL_H264_MAIN
    H264_HIGH: int = _vame.videoProfile.VAME_VIDEO_PRFL_H264_HIGH
    H264_HIGH_10: int = _vame.videoProfile.VAME_VIDEO_PRFL_H264_HIGH_10
    AV1_MAIN: int = _vame.videoProfile.VAME_VIDEO_PRFL_AV1_MAIN
    AV1_HIGH: int = _vame.videoProfile.VAME_VIDEO_PRFL_AV1_HIGH
    AV1_PROFESSIONAL: int = _vame.videoProfile.VAME_VIDEO_PRFL_AV1_PROFESSIONAL


class VIDEO_LEVEL():
    """An enum that defines video level.

    Contains HEVC_1, HEVC_2, HEVC_2_1, HEVC_3, HEVC_3_1, HEVC_4, HEVC_4_1,
    HEVC_5, HEVC_5_1, HEVC_5_2, HEVC_6, HEVC_6_1, HEVC_6_2, H264_1, H264_1_b,
    H264_1_1, H264_1_2, H264_1_3, H264_2, H264_2_1, H264_2_2, H264_3, H264_3_1,
    H264_3_2, H264_4, H264_4_1, H264_4_2, H264_5, H264_5_1, H264_5_2, H264_6,
    H264_6_1, H264_6_2.
    """
    HEVC_1: int = _vame.videoLevel.VAME_VIDEO_LVL_HEVC_1
    HEVC_2: int = _vame.videoLevel.VAME_VIDEO_LVL_HEVC_2
    HEVC_2_1: int = _vame.videoLevel.VAME_VIDEO_LVL_HEVC_2_1
    HEVC_3: int = _vame.videoLevel.VAME_VIDEO_LVL_HEVC_3
    HEVC_3_1: int = _vame.videoLevel.VAME_VIDEO_LVL_HEVC_3_1
    HEVC_4: int = _vame.videoLevel.VAME_VIDEO_LVL_HEVC_4
    HEVC_4_1: int = _vame.videoLevel.VAME_VIDEO_LVL_HEVC_4_1
    HEVC_5: int = _vame.videoLevel.VAME_VIDEO_LVL_HEVC_5
    HEVC_5_1: int = _vame.videoLevel.VAME_VIDEO_LVL_HEVC_5_1
    HEVC_5_2: int = _vame.videoLevel.VAME_VIDEO_LVL_HEVC_5_2
    HEVC_6: int = _vame.videoLevel.VAME_VIDEO_LVL_HEVC_6
    HEVC_6_1: int = _vame.videoLevel.VAME_VIDEO_LVL_HEVC_6_1
    HEVC_6_2: int = _vame.videoLevel.VAME_VIDEO_LVL_HEVC_6_2
    H264_1: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_1
    H264_1_b: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_1_b
    H264_1_1: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_1_1
    H264_1_2: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_1_2
    H264_1_3: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_1_3
    H264_2: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_2
    H264_2_1: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_2_1
    H264_2_2: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_2_2
    H264_3: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_3
    H264_3_1: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_3_1
    H264_3_2: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_3_2
    H264_4: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_4
    H264_4_1: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_4_1
    H264_4_2: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_4_2
    H264_5: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_5
    H264_5_1: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_5_1
    H264_5_2: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_5_2
    H264_6: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_6
    H264_6_1: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_6_1
    H264_6_2: int = _vame.videoLevel.VAME_VIDEO_LVL_H264_6_2


class DECODE_MODE():
    """An enum that defines decode mode.

    Contains NORMAL, INTRA_ONLY.
    """
    NORMAL: int = _vame.decodeMode.VAME_DEC_NORMAL
    INTRA_ONLY: int = _vame.decodeMode.VAME_DEC_INTRA_ONLY


class ENC_QUALITY_MODE():
    """An enum that defines encode quality mode.

    Contains GOLD, SILVER, SILVER2, BRONZE.
    """
    GOLD: int = _vame.encQualityMode.VAME_GOLD_QUALITY
    SILVER: int = _vame.encQualityMode.VAME_SILVER_QUALITY
    SILVER2: int = _vame.encQualityMode.VAME_SILVER2_QUALITY
    BRONZE: int = _vame.encQualityMode.VAME_BRONZE_QUALITY


class ENC_TUNE_TYPE():
    """An enum that defines encode tune type.

    Contains PSNR, SSIM, VISUAL, SHARP_VISUAL.
    """
    PSNR: int = _vame.encTuneType.VAME_ENC_TUNE_PSNR
    SSIM: int = _vame.encTuneType.VAME_ENC_TUNE_SSIM
    VISUAL: int = _vame.encTuneType.VAME_ENC_TUNE_VISUAL
    SHARP_VISUAL: int = _vame.encTuneType.VAME_ENC_TUNE_SHARP_VISUAL


class ENC_QP_TYPE():
    """An enum that defines encode qp type.

    Contains QP, QP_DELTA.
    """
    QP: int = _vame.encQPType.VAME_ENC_QP
    QP_DELTA: int = _vame.encQPType.VAME_ENC_QP_DELTA


class ENC_SEI_NAL_TYPE():
    """An enum that defines encode sei nal type.

    Contains SEI_PREFIX, SEI_SUFFIX.
    """
    SEI_PREFIX: int = _vame.encSEINalType.VAME_ENC_SEI_PREFIX
    SEI_SUFFIX: int = _vame.encSEINalType.VAME_ENC_SEI_SUFFIX


# =========================== STRUCT =============================


class Stream(_vame.stream):
    """A struct that defines video stream.

    Attributes:
        stream(np.ndarray): The data contained in the Stream.
        pts(int): The stream's presentation time stamp.
        inputBusAddress(int): The stream's input busAddress on the device.
    """
    stream: np.ndarray
    pts: int
    inputBusAddress: int


class CropInfo(_vame.cropInfo):
    """A struct that defines crop infomation in frame.

    Attributes:
        flag(int): Wether to crop frame while frame aligned in the device(1: True, 0: False).
        width(int): The frame's display width.
        height(int): The frane's display height.
        xOffset(int): The x-coordinate's offset to crop frame.
        yOffset(int): The y-coordinate's offset to crop frame.
    """
    flag: int
    width: int
    height: int
    xOffset: int
    yOffset: int


class Frame(_vame.frame):
    """A struct that defines video frame.

    Hint:
        You can show the frame which is decoded from vame decoder by opencv,
        but you need to make sure the frame's width is a multiple of 2,
        otherwise you will get a zero ndarray.

        Example:
            >>> img = np.array(frame)
            >>> img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR_NV12)
            >>> cv2.imshow("test.jpg", img)
            >>> cv2.waitKey()

    Attributes:
        data(np.ndarray): The data contained in the frame.
        busAddress(List[int]): The frame's busAddress on the device.
        stride(List[int]): The aligned width on the device.
        dataSize(int): The data size of the frame's data.
        width(int): The frame's width in the decoder.
        height(int): The frame's height in the decoder.
        pts(int): The frame's pts.
        memoryType(MEMORY_TYPE): The frame's memory type(host or device).
        field(VIDEO_FIELD): The frame's video field.
        pixelFormat(PIXEL_FORMAT): The frame's pixel format.
        frameType(FRAME_TYPE): The frame's type(I or P or B).
        cropInfo(CropInfo): The frame's crop information.
    """
    data: np.ndarray
    busAddress: List[int]
    stride: List[int]
    dataSize: int
    width: int
    height: int
    pts: int
    memoryType: MEMORY_TYPE
    field: VIDEO_FIELD
    pixelFormat: PIXEL_FORMAT
    frameType: FRAME_TYPE
    cropInfo: CropInfo


# class Version(_vame.version):
#     major: int
#     minor: int
#     build: int


class HardwareID(_vame.hardwareID):
    """A struct that defines hardware id.

    Attributes:
        coreID(int): The core id of hardware.
        dieID(int): The die id of hardware.
    """
    coreID: int
    dieID: int


class Rational(_vame.rational):
    """A struct that defines FPS.

    Attributes:
        numerator(int): The numerator of FPS.
        denominator(int): The denominator of FPS.
    """
    numerator: int
    denominator: int


class DecChannelParamters(_vame.decChannelParamters):
    """A struct that defines decode channel parameters.

    Important:
        Unreleased frame cannot exceed the extraBufferNumber.

    Attributes:
        codecType(CODEC_TYPE): The decode channel's codec type.
        sourceMode(SOURCE_MODE): The decode channel's source mode.
        decodeMode(DECODE_MODE): The decode channel's decode mode.
        pixelFormat(PIXEL_FORMAT): The decode channel's pixel format.
        extraBufferNumber(int): The decode channel's extra buffer number.
    """
    codecType: CODEC_TYPE
    sourceMode: SOURCE_MODE
    decodeMode: DECODE_MODE
    pixelFormat: PIXEL_FORMAT
    extraBufferNumber: int


class DecStreamInfo(_vame.decStreamInfo):
    """A struct that defines decode stream information.

    Attributes:
        width(int): The decode stream's width.
        height(int): The decode stream's height.
        fps(int): The decode stream's fps.
        pixelSize(int): The decode stream's pixel size.
    """
    width: int
    height: int
    fps: int
    pixelSize: int


class DecJpegInfo(_vame.decJpegInfo):
    """A struct that defines decode jpeg information.

    Attributes:
        width(int): The JPEG image's width.
        height(int): The JPEG image's height.
        x_density(int): The JPEG image's x_density.
        y_density(int): The JPEG image's y_density
        outputFormat(CHROMA_FORMAT): The JPEG image's chroma format.
        codingMode(JPEG_CODING_MODE): The JPEG image's coding mode.
    """
    width: int
    height: int
    x_density: int
    y_density: int
    outputFormat: CHROMA_FORMAT
    codingMode: JPEG_CODING_MODE


class DecStatus(_vame.decStatus):
    """A struct that defines decoder's status.

    Attributes:
        state(STATE): The decoder's state.
        hardwareID(HardwareID): The decoder's state.
        result(int): Wether to get decoder's state successfully.
        runningFrames(int): The number of frames that runing in the decoder.
        reorderedFrames(int): The number of frames that reordered in the decoder.
        bufferedFrames(int): The number of frames that buffered in the decoder.
        droppedFrames(int): The number of frames that dropped in the decoder.
    """
    state: STATE
    hardwareID: HardwareID
    result: int
    runningFrames: int
    reorderedFrames: int
    bufferedFrames: int
    droppedFrames: int


class DecOutputOptions(_vame.decOutputOptions):
    """A struct that defines decoder's output options.

    Attributes:
        memoryType(MEMORY_TYPE): Decide the frame's memory type from the decoder(host or device).
        enableCrop(int): Wether to crop the frame's from the decoder(1: True, 0: False).
    """
    memoryType: MEMORY_TYPE
    enableCrop: int


class DecVideoInfo(_vame.decVideoInfo):
    """A struct that defines decode video information.

    Attributes:
        width(int): The video's width.
        height(int): The video's height.
        cropFlag(int): The video's crop flag.
        cropWidth(int): The video's crop width if cropFlag is True.
        cropHeight(int): The video's height if cropFlag is True.
        xOffset(int): The video's xOffset if cropFlag is True.
        yOffset(int): The video's yOffset if cropFlag is True.
        fps(int): The video's fps.
        pixelFormat(PIXEL_FORMAT): The video's pixel format.
    """
    width: int
    height: int
    cropFlag: int
    cropWidth: int
    cropHeight: int
    xOffset: int
    yOffset: int
    fps: int
    pixelFormat: PIXEL_FORMAT


class JpegDecCapability(_vame.jpegDecCapability):
    """A struct that defines decoder's jpeg capability.

    Attributes:
        maxWidth(int): The max width of JPEG image supported by decoder.
        maxHeight(int): The max height of JPEG image supported by decoder.
        minWidth(int): The min width of JPEG image supported by decoder.
        minHeight(int): The min height of JPEG image supported by decoder.
        codingMode(List[JPEG_CODING_MODE]): The coding mode of JPEG image supported by decoder.
        pixelFormats(List[PIXEL_FORMAT]): The pixel formats of JPEG image supported by decoder.
    """
    maxWidth: int
    maxHeight: int
    minWidth: int
    minHeight: int
    codingMode: List[JPEG_CODING_MODE]
    pixelFormats: List[PIXEL_FORMAT]


class VideoDecCapability(_vame.videoDecCapability):
    """A struct that defines decoder's video capability.

    Attributes:
        bitDepth(int): The bit depth of video supported by decoder.
        maxWidth(int): The max width of video supported by decoder.
        maxHeight(int): The max height of video supported by decoder.
        minWidth(int): The min width of video supported by decoder.
        minHeight(int): The min height of video supported by decoder.
        maxProFile(VIDEO_PROFILE): The max profile of video supported by decoder.
        maxLevel(VIDEO_LEVEL): The max level of video supported by decoder.
        pixelFormats(List[PIXEL_FORMAT]): The pixel formats of video supported by decoder.
    """
    bitDepth: int
    maxWidth: int
    maxHeight: int
    minWidth: int
    minHeight: int
    maxProFile: VIDEO_PROFILE
    maxLevel: VIDEO_LEVEL
    pixelFormats: List[PIXEL_FORMAT]


class EncExternalSEI(_vame.encExternalSEI):
    """A struct that defines encode external sei.

    Attributes:
        nalType(ENC_SEI_NAL_TYPE): The sei nal type of the encoder.
        payloadType(int): The payload type of the encoder.
        payloadDataSize(int): The payload data size of the encoder.
        payloadData(Any): This is a pointer to payload data.
    """
    nalType: ENC_SEI_NAL_TYPE
    payloadType: int
    payloadDataSize: int
    payloadData: Any


class EncPictureArea(_vame.encPictureArea):
    """A struct that defines encode picture area.

    Attributes:
        enable(int): Wether to enable this area(1: True, 0: False).
        top(int): The top of the area.
        left(int): The left of the area.
        bottom(int): The bottom of the area.
        right(int): The right of the area.
    """
    enable: int
    top: int
    left: int
    bottom: int
    right: int


class EncPictureROI(_vame.encPictureROI):
    """A struct that defines encode picture ROI.

    Attributes:
        area(EncPictureArea): The area description of the ROI.
        qpType(ENC_QP_TYPE): The qp type of the ROI.
        qpValue(INT): The qp value of the ROI.
    """
    area: EncPictureArea
    qpType: ENC_QP_TYPE
    qpValue: int


class EncExtendedParams(_vame.encExtendedParams):
    """A struct that defines encode extended parameters.

    Attributes:
        forceIDR(int): Wether to make the frame to be a IDR frame(1: True, 0: False).
        roi(EncPictureROI): The ROI description of the encoder.
    """
    forceIDR: int
    roi: EncPictureROI


class EncVideoConfiguration(_vame.encVideoConfiguration):
    """A struct that defines video encoder configuration.

    Attributes:
        profile(VIDEO_PROFILE): The profile of the video encoder.
        level(VIDEO_LEVEL): The level of the video encoder.
        width(int): The width of the video encoder.
        height(int): The height of the encoder.
        frameRate(Rational): The frameRate of the encoder.
        bitDepthLuma(int): The bitDepthLuma of the video encoder.
        bitDepthChroma(int): The bitDepthChroma of the video encoder.
        gopSize(int): The gopSize of the video encoder.
        gdrDuration(int): The gdrDuration of the video encoder.
        lookaheadDepth(int): The lookaheadDepth of the video encoder.
        qualityMode(int): The qualityMode of the video encoder.
        tune(ENC_TUNE_TYPE): The tune of the video encoder.
        keyInt(VIDEO_PROFILE): The keyInt of the video encoder.
        crf(int): The crf of the video encoder.
        cqp(int): The cqp of the video encoder.
        llRc(int): The llRc of the video encoder.
        bitRate(int): The bitRate of the video encoder.
        initQp(int): The initQp of the video encoder.
        vbvBufSize(int): The vbvBufSize of the video encoder.
        vbvMaxRate(int): The vbvMaxRate of the video encoder.
        intraQpDelta(int): The intraQpDelta of the video encoder.
        qpMinI(int): The qpMinI of the video encoder.
        qpMaxI(int): The qpMaxI of the video encoder.
        qpMinPB(int): The qpMinPB of the video encoder.
        qpMaxPB(int): The qpMaxPB of the video encoder.
        vbr(int): The vbr of the video encoder.
        aqStrength(float): The aqStrength of the video encoder.
        enableROI(int): The enableROI of the video encoder.
        P2B(int): The P2B of the video encoder.
        bBPyramid(int): The bBPyramid of the video encoder.
        maxFrameSizeMultiple(float): The maxFrameSizeMultiple of the video encoder.
    """
    profile: VIDEO_PROFILE
    level: VIDEO_LEVEL
    width: int
    height: int
    frameRate: Rational
    bitDepthLuma: int
    bitDepthChroma: int
    gopSize: int
    gdrDuration: int
    lookaheadDepth: int
    qualityMode: ENC_QUALITY_MODE
    tune: ENC_TUNE_TYPE
    keyInt: int
    crf: int
    cqp: int
    llRc: int
    bitRate: int
    initQp: int
    vbvBufSize: int
    vbvMaxRate: int
    intraQpDelta: int
    qpMinI: int
    qpMaxI: int
    qpMinPB: int
    qpMaxPB: int
    vbr: int
    aqStrength: float
    enableROI: int
    P2B: int
    bBPyramid: int
    maxFrameSizeMultiple: float


class EncJPEGConfiguration(_vame.encJPEGConfiguration):
    """A struct that defines JPEG encoder configuration.

    Attributes:
        codingWidth(int): The coding width of the jpeg encoder.
        codingHeight(int): The coding height of the jpeg encoder.
        frameType(PIXEL_FORMAT): The pixel format with of the jpeg encoder.
        userData(str): The user data of the jpeg encoder.
        losslessEn(int): The losslessEn of the jpeg encoder.
    """
    codingWidth: int
    codingHeight: int
    frameType: PIXEL_FORMAT
    userData: str
    losslessEn: int


class EncChannelParamters():
    """A struct that defines encoder channel parameters.

    Attributes:
        codecType(CODEC_TYPE): The codec type of the encoder.
        outbufNum(int): The out buffer num of the encoder.
        enProfiling(int): The enProfiling of the encoder.
        config(Union[EncVideoConfiguration, EncJPEGConfiguration]): The config of the encoder.
    """
    codecType: CODEC_TYPE
    outbufNum: int
    enProfiling: int
    config: Union[EncVideoConfiguration, EncJPEGConfiguration]


class EncOutputOptions(_vame.encOutputOptions):
    """A struct that defines encoder output options.

    Attributes:
        reserved: This is just a reserved struct.
    """
    reserved: int


# =========================== DEFINE =============================

WARN_MORE_DATA = _vame.vameER_RSLT_WARN_MORE_DATA
WARN_EOS = _vame.vameER_RSLT_WARN_EOS
DEC_MAX_PIX_FMT_NUM = _vame.VAME_DEC_MAX_PIX_FMT_NUM
DEC_MAX_CODING_MODE_NUM = _vame.VAME_DEC_MAX_CODING_MODE_NUM
DEC_JPEG_MAX_WIDTH = _vame.VAME_DEC_JPEG_MAX_WIDTH
DEC_JPEG_MAX_HEIGHT = _vame.VAME_DEC_JPEG_MAX_HEIGHT
DEC_JPEG_MIN_WIDTH = _vame.VAME_DEC_JPEG_MIN_WIDTH
DEC_JPEG_MIN_HEIGHT = _vame.VAME_DEC_JPEG_MIN_HEIGHT
DEC_VIDEO_MAX_WIDTH = _vame.VAME_DEC_VIDEO_MAX_WIDTH
DEC_VIDEO_MAX_HEIGHT = _vame.VAME_DEC_VIDEO_MAX_HEIGHT
DEC_VIDEO_MIN_WIDTH = _vame.VAME_DEC_VIDEO_MIN_WIDTH
DEC_VIDEO_MIN_HEIGHT = _vame.VAME_DEC_VIDEO_MIN_HEIGHT
DEC_MAX_STREAM_BUFFER_SIZE = _vame.VAME_DEC_MAX_STREAM_BUFFER_SIZE
ENC_MAX_STRM_BUF_NUM = _vame.VAME_ENC_MAX_STRM_BUF_NUM
ENC_MAX_REF_FRAMES = _vame.VAME_ENC_MAX_REF_FRAMES
ENC_MAX_GOP_SIZE = _vame.VAME_ENC_MAX_GOP_SIZE
ENC_MAX_LTR_FRAMES = _vame.VAME_ENC_MAX_LTR_FRAMES
ENC_MAX_ROI_NUM = _vame.VAME_ENC_MAX_ROI_NUM
ENC_DEFAULT_PAR = _vame.VAME_ENC_DEFAULT_PAR
ENC_VIDEO_MAX_HEIGHT = _vame.VAME_ENC_VIDEO_MAX_HEIGHT
ENC_VIDEO_MAX_WIDTH = _vame.VAME_ENC_VIDEO_MAX_WIDTH
ENC_VIDEO_MIN_HEIGHT = _vame.VAME_ENC_VIDEO_MIN_HEIGHT
ENC_VIDEO_MIN_WIDTH = _vame.VAME_ENC_VIDEO_MIN_WIDTH
ENC_JPEG_MAX_HEIGHT = _vame.VAME_ENC_JPEG_MAX_HEIGHT
ENC_JPEG_MAX_WIDTH = _vame.VAME_ENC_JPEG_MAX_WIDTH
ENC_JPEG_MIN_HEIGHT = _vame.VAME_ENC_JPEG_MIN_HEIGHT
ENC_JPEG_MIN_WIDTH = _vame.VAME_ENC_JPEG_MIN_WIDTH
ENC_MAX_OUTBUF_NUM = _vame.VAME_ENC_MAX_OUTBUF_NUM

# =========================== API =============================


@err_check
def systemInitialize() -> int:
    """Initialize the vame system.

    Hint:
        Please initialize before using vame.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vame.systemInitialize()


@err_check
def systemUninitialize() -> int:
    """Uninitialize the vame system.

    Hint:
        Please uninitialize after using vame.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vame.systemUninitialize()


# def getVersion() -> str:
#     """Get the VAME API version information.

#     Returns:
#         str: vame version string.
#     """
#     return _vame.getVersion()
