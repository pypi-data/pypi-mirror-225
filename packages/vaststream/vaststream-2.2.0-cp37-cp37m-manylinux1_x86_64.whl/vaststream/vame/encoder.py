# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

__all__ = [
    "createEncoderChannel", "destroyEncoderChannel", "startEncoder",
    "resetEncoder", "stopEncoder", "sendFrameToEncoder",
    "receiveStreamFromEncoder", "jpegSyncEncoder", "encReleaseStream",
    "getEncoderAvailableChannels", "YUVReader", "Encoder"
]

from _vaststream_pybind11 import vame as _vame
import os
import warnings
import numpy as np
from typing import Tuple, Optional
from .common import *
from .utils import *


@err_check
def createEncoderChannel(channelId: int, params: EncChannelParamters) -> int:
    """Create an encoder channel.

    Args:
        channelId(int): Encoder channel's ID.
        params(EncChannelParamters): The init parameter for encoder channel.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    # 类型兼容
    paramsPybind = _vame.encChannelParamters()
    paramsPybind.codecType = params.codecType
    paramsPybind.outbufNum = params.outbufNum
    paramsPybind.enProfiling = params.enProfiling
    if isinstance(params.config, EncJPEGConfiguration):
        paramsPybind.jpegConfig = params.config
    else:
        paramsPybind.videoConfig = params.config
    return _vame.createEncoderChannel(paramsPybind, channelId)


@err_check
def destroyEncoderChannel(channelId: int) -> int:
    """Destroy an encoder channel.

    Args:
        channelId(int): Encoder channel's ID.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vame.destroyEncoderChannel(channelId)


@err_check
def startEncoder(channelId: int) -> int:
    """Start the encoder.

    Args:
        channelId(int): Encoder channel's ID.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vame.startEncoder(channelId)


@err_check
def resetEncoder(channelId: int) -> int:
    """Restart the encoder.

    Args:
        channelId(int): Encoder channel's ID.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vame.resetEncoder(channelId)


@err_check
def stopEncoder(channelId: int) -> int:
    """Stop the encoder.

    Args:
        channelId(int): Encoder channel's ID.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vame.stopEncoder(channelId)


def sendFrameToEncoder(channelId: int,
                       frame: Frame,
                       extParams: EncExtendedParams = None,
                       timeout: int = 4000) -> int:
    """Send a frame to the encoder

    Args:
        channelId(int): Encoder channel's ID.
        frame(Frame): The frame that send to encoder.
        extParams(EncExtendedParams): Ext params for encoder(default None).
        timeout(int): timeout value(default 4000).

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    ret = _vame.sendFrameToEncoder(channelId, frame, extParams, timeout)
    if ret >= _vame.vameER_RSLT_ERR_START:
        raise RuntimeError(f"sendFrameToEncoder error, ret: {ret}.")
    if ret != _vame.vameER_SUCCESS:
        warnings.warn(f"sendFrameToEncoder waring: {ret}")
    return ret


def receiveStreamFromEncoder(channelId: int,
                             timeout: int = 4000
                             ) -> Tuple[int, Optional[Stream]]:
    """Receive a stream from the encoder.

    Hint:
        If return code gets ``vame.WARN_MORE_DATA``, it means you need send more frame,
        If return code gets ``vame.WARN_EOS``, it means the encoder has benn stopped.

    Args:
        channelId(int): Encoder channel's ID.
        timeout(int): timeout value(default 4000).

    Returns:
        Tuple[int, Optional[Stream]]: First is the return code. 0 for success, False otherwise and stream get None.
    """
    stream = _vame.stream()
    ret = _vame.receiveStreamFromEncoder(channelId, stream, timeout)
    if ret >= _vame.vameER_RSLT_ERR_START:
        raise RuntimeError(f"receiveStreamFromEncoder error, ret: {ret}.")
    if ret == _vame.vameER_SUCCESS:
        return (ret, stream)
    return (ret, None)


def jpegSyncEncoder(channelId: int,
                    frame: Frame,
                    extParams: EncExtendedParams = None,
                    timeout: int = 4000) -> Stream:
    """Encode a jpeg file, this is a synchronization api.

    Args:
        channelId(int): Encoder channel's ID.
        frame(Frame): The frame that send to encoder.
        extParams(EncExtendedParams): Ext params for encoder(default None).
        timeout(int): timeout value(default 4000).

    Returns:
        Stream: The encoded stream from the JPEG image.
    """
    stream = _vame.stream()
    ret = _vame.jpegSyncEncoder(channelId, frame, stream, extParams, timeout)
    if ret != _vame.vameER_SUCCESS:
        raise RuntimeError(f"jpegSyncEncoder error, ret: {ret}.")
    return stream


def encReleaseStream(channelId: int,
                     stream: Stream,
                     timeout: int = 4000) -> int:
    """Release a stream from the encoder.

    Args:
        channelId(int): Encoder channel's ID.
        stream(Stream): The stream to be released.
        timeout(int): timeout value(default 4000).

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vame.encReleaseStream(channelId, stream, timeout)


def getEncoderAvailableChannels() -> int:
    """Get available channels of the encoder.

    Returns:
        int: The available channels of the encoder.
    """
    return _vame.getEncoderAvailableChannels()


class Encoder():
    """The decoder tool class.

    If you use the ``with..as..``, the encoder will create in the ``__enter__``
    and destroy in the ``__exit__`` .if auto_start is True, the encoder will start
    and stop when you create and destroy the encoder.if auto_init is True, the
    vame will Initialize and Uninitialize when you create and destroy the encoder.

    Important:
        If you use the ``with..as..``, make sure you join the thread in the ``with`` scope
        when you regard encoder as args, because the encoder will destroy when you out
        of the ``with`` scope.

        Example:
            >>> with vame.Encoder(...) as encoder:
            >>>     t = Thread(target=func, args=(encoder,))
            >>>     t.join()
    
    Hint:
        The Encoder tool class will destroy when the encoder instance released by the python GC,
        so you do not need to create and destroy encoder explicitly.

    Args:
        channelId(int): Encoder channel index.
        param(DecChannelParamters): The init parameter for encoder channel.
        auto_start(auto_start): Whether to start and stop channel automatically(default False).
        auto_init(auto_init): Whether to systemInitialize and systemUninitialize automatically(default True).

    Examples:
        >>> with vame.Encoder(...) as encoder:
        >>>     encoder.start()
        >>>     encoder.stop()
    or you can use it like this:

        >>> encoder = vame.Encoder(...)
        >>> encoder.start()
        >>> encoder.stop()
    """

    def __init__(self,
                 channelId: int,
                 params: EncChannelParamters,
                 auto_start: bool = False,
                 auto_init: bool = True) -> None:
        self.channelId = channelId
        self.params = params
        self.auto_start = auto_start
        self.auto_init = auto_init
        self._instance = False
        self.create()

    def __enter__(self):
        # self.create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.destroy()

    def __del__(self):
        self.destroy()

    def create(self) -> int:
        """Create the encoder channel.

        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        ret = _vame.vameER_SUCCESS
        if not self._instance:
            if self.auto_init: systemInitialize()
            ret = createEncoderChannel(self.channelId, self.params)
            self._instance = True
            if self.auto_start: startEncoder(self.channelId)
        return ret

    def destroy(self) -> int:
        """Destroy the encoder channel.

        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        ret = _vame.vameER_SUCCESS
        if self._instance:
            if self.auto_start: stopEncoder(self.channelId)
            ret = destroyEncoderChannel(self.channelId)
            self._instance = False
            if self.auto_init: systemUninitialize()
        return ret

    def start(self) -> int:
        """Start the encoder.

        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        assert self._instance, "Please create encoder."
        return startEncoder(self.channelId)

    def stop(self) -> int:
        """Stop the encoder.

        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        assert self._instance, "Please create encoder."
        return stopEncoder(self.channelId)

    def reset(self) -> int:
        """Reset the encoder.

        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        assert self._instance, "Please create encoder."
        return resetEncoder(self.channelId)

    def sendFrame(self,
                  frame: Frame,
                  extParams: EncExtendedParams = None,
                  timeout: int = 4000) -> int:
        """Send a frame to Encoder to encode.

        Args:
            frame(Frame): The frame that send to encoder.
            extParams(EncExtendedParams): Ext params for encoder(default None).
            timeout(int): timeout value(default 4000).

        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        assert self._instance, "Please create encoder."
        return sendFrameToEncoder(self.channelId, frame, extParams, timeout)

    def receiveStream(self,
                      timeout: int = 4000) -> Tuple[int, Optional[Stream]]:
        """Receive a stream from Encoder.

        Hint:
            If return code gets ``vame.WARN_MORE_DATA``, it means you need send more frame,
            If return code gets ``vame.WARN_EOS``, it means the encoder has benn stopped.

        Args:
            timeout(int): timeout value(default 4000).

        Returns:
            Tuple[int, Optional[Stream]]: First is the return code. 0 for success, False otherwise and stream get None.
        """
        assert self._instance, "Please create encoder."
        return receiveStreamFromEncoder(self.channelId, timeout)

    def jpegSync(self,
                 frame: Frame,
                 extParams: EncExtendedParams = None,
                 timeout: int = 4000) -> Stream:
        """Jpeg Encode Sync api.

        Args:
            frame(Frame): The frame that send to encoder.
            extParams(EncExtendedParams): Ext params for encoder(default None).
            timeout(int): timeout value(default 4000).

        Returns:
            Stream: The encoded stream from the JPEG image.
        """
        assert self._instance, "Please create encoder."
        return jpegSyncEncoder(self.channelId, frame, extParams, timeout)

    def releaseStream(self, stream: Stream, timeout: int = 4000) -> int:
        """Release a stream from the encoder.

        Args:
            stream(Stream): The stream to be released.
            timeout(int): timeout value(default 4000).

        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        assert self._instance, "Please create encoder."
        return encReleaseStream(self.channelId, stream, timeout)


class YUVReader():
    """YUV Reader tool class.

    There are few python libraries parse yuv file, so we provide
    a tool class to parse yuv file, This tool class can parse a
    yuv file, and put it's data to frame, so you can read frame
    directly from your yuv file.

    Args:
        filePath(str): yuv file path.
        format(PIXEL_FORMAT): The pixel format of your yuv file.
        width(int): The width of you yuv file.
        height(int): The height of you yuv file.
        stride(int): The stride of you yuv file(default None).

    Examples:
        >>> with vame.YUVReader(...) as reader:
        >>>     frame = reader.readFrame()
    or you can use it like this:

        >>> reader = vame.YUVReader(...)
        >>> frame = reader.readFrame()
    """

    SUPPORT_PIXEL_FORMAT = (PIXEL_FORMAT.YUV420P, PIXEL_FORMAT.NV12,
                            PIXEL_FORMAT.NV21)

    def __init__(self,
                 filePath: str,
                 format: PIXEL_FORMAT,
                 width: int,
                 height: int,
                 stride: int = None):
        if not os.path.exists(filePath):
            raise RuntimeError(f"Can not find YUV file {filePath}.")
        self.filePath = filePath
        self.format = format
        self.width = width
        self.height = height
        self.stride = [width, 0, 0] if stride is None else [stride, 0, 0]
        self.busAddress = [0, 0, 0]
        self.luma_size = 0
        self.chroma_size_cb = 0
        self.chroma_size_cr = 0
        self.pic_size = 0
        self.fileHandle = None
        self._parse()
        self.create()

    def _parse(self):
        # 仅支持420
        if self.format not in self.SUPPORT_PIXEL_FORMAT:
            raise RuntimeError(
                f"The format {self.format} is not supported yet, only support {self.SUPPORT_PIXEL_FORMAT}."
            )
        self.luma_size = self.stride[0] * self.height
        # 奇数向上取整
        stride_align = ((self.stride[0] + 1) // 2 * 2) // 2
        height_align = ((self.height + 1) // 2 * 2) // 2
        if self.format == PIXEL_FORMAT.YUV420P:
            self.stride[1] = stride_align
            self.stride[2] = stride_align
            self.chroma_size_cb = self.stride[1] * height_align
            self.chroma_size_cr = self.stride[2] * height_align
        else:
            self.stride[1] = (self.stride[0] + 1) // 2 * 2
            self.chroma_size_cb = self.stride[1] * height_align
            self.chroma_size_cr = 0
        self.pic_size = self.luma_size + self.chroma_size_cb + self.chroma_size_cr

    def __enter__(self):
        # self.create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.destroy()

    def __del__(self):
        self.destroy()

    def create(self) -> None:
        """Create the reader.
        """
        if self.fileHandle is None:
            self.fileHandle = open(self.filePath, "rb")

    def destroy(self) -> None:
        """Destroy the reader.
        """
        if self.fileHandle is not None:
            self.fileHandle.close()
            self.fileHandle = None

    def readFrame(self) -> Optional[Frame]:
        """Read one frame data from yuv file to a frame.

        Returns:
            Optional[Frame]: Read a frame if success else None.
        """
        assert self.fileHandle is not None, "Please create reader."
        dataBytes = self.fileHandle.read(self.pic_size)
        if dataBytes == b'':
            return None

        frame = Frame()
        frame.data = np.frombuffer(dataBytes, np.byte)
        frame.dataSize = self.pic_size
        frame.width = self.width
        frame.height = self.height
        frame.stride = self.stride
        frame.busAddress = self.busAddress
        frame.memoryType = MEMORY_TYPE.HOST
        frame.pixelFormat = self.format

        return frame