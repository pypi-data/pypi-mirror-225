# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

__all__ = [
    "createDecoderChannel", "destroyDecoderChannel", "startDecoder",
    "resetDecoder", "stopDecoder", "sendStreamToDecoder",
    "receiveFrameFromDecoder", "jpegSyncDecoder", "transferFrameFromDecoder",
    "decReleaseFrame", "getJpegInfo", "getVideoInfo",
    "getStreamInfoFromDecoder", "getDecoderStatus", "jpegDecGetCaps",
    "videoDecGetCaps", "getDecoderAvailableChannels", "Decoder", "H264Reader"
]

from _vaststream_pybind11 import vame as _vame
import os
import warnings
from typing import Optional, Tuple
from .common import *
from .utils import *


@err_check
def createDecoderChannel(channelId: int, params: DecChannelParamters) -> int:
    """Create a decoder channel.

    Args:
        channelId(int): Decoder channel's ID.
        params(DecChannelParamters): The init parameter for decoder channel.
    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vame.createDecoderChannel(params, channelId)


@err_check
def destroyDecoderChannel(channelId: int) -> int:
    """Destroy a decoder channel.

    Args:
        channelId(int): Decoder channel's ID.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vame.destroyDecoderChannel(channelId)


@err_check
def startDecoder(channelId: int) -> int:
    """Start the decoder.

    Args:
        channelId(int): Decoder channel's ID.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vame.startDecoder(channelId)


@err_check
def resetDecoder(channelId: int) -> int:
    """Restart the decoder.

    Args:
        channelId(int): Decoder channel's ID.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vame.resetDecoder(channelId)


@err_check
def stopDecoder(channelId: int) -> int:
    """Stop the decoder.

    Args:
        channelId(int): Decoder channel's ID.

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vame.stopDecoder(channelId)


def sendStreamToDecoder(channelId: int,
                        stream: Stream,
                        timeout: int = 4000) -> int:
    """Send a stream to decoder.

    Args:
        channelId(int): Decoder channel's ID.
        stream(Stream): The stream that send to decoder.
        timeout(int): timeout value(default 4000).

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    ret = _vame.sendStreamToDecoder(channelId, stream, timeout)
    if ret >= _vame.vameER_RSLT_ERR_START:
        raise RuntimeError(f"sendStreamToDecoder error, ret: {ret}.")
    if ret != _vame.vameER_SUCCESS:
        warnings.warn(f"sendStreamToDecoder waring: {ret}")
    return ret


def receiveFrameFromDecoder(
        channelId: int,
        decOutOptions: DecOutputOptions,
        timeout: int = 4000) -> Tuple[int, Optional[Frame]]:
    """Receive a frame from Decoder.

    Hint:
        If return code gets ``vame.WARN_MORE_DATA``, it means you need to send more streams.
        If return code gets ``vame.WARN_EOS``, it means the decoder has been stopped.

    Args:
        channelId(int): Decoder channel's ID.
        decOutOptions(DecOutputOptions): Decoder output options.
        timeout(int): timeout value(default 4000).

    Returns:
        Tuple[int, Optional[Frame]]: First is the return code. 0 for success, False otherwise and frame get None.
    """
    frame = _vame.frame()
    ret = _vame.receiveFrameFromDecoder(channelId, frame, decOutOptions,
                                        timeout)
    if ret >= _vame.vameER_RSLT_ERR_START:
        raise RuntimeError(f"receiveFrameFromDecoder error, ret: {ret}.")
    if ret == _vame.vameER_SUCCESS:
        return (ret, frame)
    return (ret, None)


def jpegSyncDecoder(channelId: int,
                    imagePath: str,
                    timeout: int = 4000) -> Frame:
    """Decode a jpeg file, this is a synchronization api.

    Args:
        channelId(int): Decoder channel's ID.
        imagePath(str): The JPEG image's path.
        timeout(int): timeout value(default 4000).

    Returns:
        Frame: The decoded frame from the JPEG image.
    """
    if not os.path.exists(imagePath):
        raise RuntimeError(f"Can not find file: {imagePath}.")
    frame = _vame.frame()
    ret = _vame.jpegSyncDecoder(channelId, imagePath, frame, timeout)
    if ret != _vame.vameER_SUCCESS:
        raise RuntimeError(f"jpegSyncDecoder error, ret: {ret}.")
    return frame


def transferFrameFromDecoder(channelId: int, frame: Frame,
                             crop: bool) -> Frame:
    """Transfer frame data from device to host.

    Args:
        channelId(int): Decoder channel's ID.
        frame(Frame): The decoded frame from teh decoder.
        crop(int): Wether to crop the frame.

    Returns:
        Frame: The frame transfered from the input frame.
    """
    ret = _vame.transferFrameFromDecoder(channelId, frame, crop)
    if ret != _vame.vameER_SUCCESS:
        raise RuntimeError(f"transferFrameFromDecoder error, ret: {ret}.")
    return frame


@err_check
def decReleaseFrame(channelId: int, frame: Frame, timeout: int = 4000) -> int:
    """Receive a frame from Decoder.

    Args:
        channelId(int): Decoder channel's ID.
        frame(Frame): The frame to be released.
        timeout(int): timeout value(default 4000).

    Returns:
        int: The return code. 0 for success, False otherwise.
    """
    return _vame.decReleaseFrame(channelId, frame, timeout)


def getJpegInfo(imagePath: str) -> DecJpegInfo:
    """Get jpeg information.

    Args:
        imagePath(str): The JPEG image's path.

    Returns:
        DecJpegInfo: The JPEG image's information.

    """
    jpegInfo = _vame.decJpegInfo()
    ret = _vame.getJpegInfo(imagePath, jpegInfo)
    if ret != _vame.vameER_SUCCESS:
        raise RuntimeError(f"getJpegInfo error, ret: {ret}.")
    return jpegInfo


def getVideoInfo(stream: Stream, codecType: CODEC_TYPE) -> DecVideoInfo:
    """Get video information from the stream.

    Args:
        stream(Stream): The stream of the video.
        codecType(CODEC_TYPE): The codec type of the video.

    Returns:
        DecVideoInfo: The video's information.
    """
    decVideoInfo = _vame.decVideoInfo()
    ret = _vame.getVideoInfo(stream, codecType, decVideoInfo)
    if ret != _vame.vameER_SUCCESS:
        raise RuntimeError(f"getVideoInfo error, ret: {ret}.")
    return decVideoInfo


def getStreamInfoFromDecoder(channelId: int) -> DecStreamInfo:
    """Get the Stream information by Decoder.

    Args:
        channelId(int): Decoder channel's ID.

    Returns:
        DecStreamInfo: The stream information of the decoder.
    """
    decStreamInfo = _vame.decStreamInfo()
    ret = _vame.getStreamInfoFromDecoder(channelId, decStreamInfo)
    if ret != _vame.vameER_SUCCESS:
        raise RuntimeError(f"getStreamInfoFromDecoder error, ret: {ret}.")
    return decStreamInfo


def getDecoderStatus(channelId: int) -> DecStatus:
    """Get the Decoder status information.

    Args:
        channelId(int): Decoder channel's ID.

    Returns:
        DecStatus: The status of the decoder.
    """
    decStatus = _vame.decStatus()
    ret = _vame.getDecoderStatus(channelId, decStatus)
    if ret != _vame.vameER_SUCCESS:
        raise RuntimeError(f"getDecoderStatus error, ret: {ret}.")
    return decStatus


def jpegDecGetCaps() -> JpegDecCapability:
    """Get the capability to decode jpeg on the device.

    Returns:
        JpegDecCapability: The JPEG decode capability of the decoder.
    """
    jpegDecCapability = _vame.jpegDecCapability()
    ret = _vame.jpegDecGetCaps(jpegDecCapability)
    if ret != _vame.vameER_SUCCESS:
        raise RuntimeError(f"jpegDecGetCaps error, ret: {ret}.")
    return jpegDecCapability


def videoDecGetCaps(codec: CODEC_TYPE) -> VideoDecCapability:
    """Get the capability to decode video on the device.

    Arg:
        codec(CODEC_TYPE): The codec type of the video.

    Returns:
        VideoDecCapability: The video decode capability of the decoder.
    """
    videoDecCapability = _vame.videoDecCapability()
    ret = _vame.videoDecGetCaps(codec, videoDecCapability)
    if ret != _vame.vameER_SUCCESS:
        raise RuntimeError(f"videoDecGetCaps error, ret: {ret}.")
    return videoDecCapability


def getDecoderAvailableChannels() -> int:
    """Get available channels of the decoder.

    Returns:
        int: The available channels of the decoder.
    """
    return _vame.getDecoderAvailableChannels()


class Decoder():
    """The decoder tool class.

    If you use the ``with..as..``, the decoder will create in the ``__enter__``
    and destroy in the ``__exit__`` .if auto_start is True, the decoder will start 
    and stop when you create and destroy the decoder.if auto_init is True, the
    vame will Initialize and Uninitialize when you create and destroy the decoder.

    Important:
        If you use the ``with..as..``, make sure you join the thread in the ``with`` scope
        when you regard decoder as args, because the decoder will destroy when you out
        of the ``with`` scope.

        Example:
            >>> with vame.Decoder(...) as decoder:
            >>>     t = Thread(target=func, args=(decoder,))
            >>>     t.join()
    
    Hint:
        The Decoder tool class will destroy when the decoder instance released by the python GC,
        so you do not need to create and destroy decoder explicitly.

    Args:
        channelId(int): Decoder channel index.
        param(DecChannelParamters): The init parameter for decoder channel.
        auto_start(auto_start): Whether to start and stop channel automatically(default False).
        auto_init(auto_init): Whether to systemInitialize and systemUninitialize automatically(default True).

    Examples:
        >>> with vame.Decoder(...) as decoder:
        >>>     decoder.start()
        >>>     decoder.stop()
    or you can use it like this:

        >>> decoder = vame.Decoder(...)
        >>> decoder.start()
        >>> decoder.stop()
    """

    def __init__(self,
                 channelId: int,
                 params: DecChannelParamters,
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
        """Create the decoder channel.

        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        ret = _vame.vameER_SUCCESS
        if not self._instance:
            if self.auto_init: systemInitialize()
            ret = createDecoderChannel(self.channelId, self.params)
            self._instance = True
            if self.auto_start: startDecoder(self.channelId)
        return ret

    def destroy(self) -> int:
        """Destroy the decoder channel.

        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        ret = _vame.vameER_SUCCESS
        if self._instance:
            if self.auto_start: stopDecoder(self.channelId)
            ret = destroyDecoderChannel(self.channelId)
            self._instance = False
            if self.auto_init: systemUninitialize()
        return ret

    def start(self):
        """Start the decoder.

        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        assert self._instance, "Please create decoder."
        return startDecoder(self.channelId)

    def stop(self):
        """Stop the decoder.

        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        assert self._instance, "Please create decoder."
        return stopDecoder(self.channelId)

    def reset(self):
        """Reset the decoder.

        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        assert self._instance, "Please create decoder."
        return resetDecoder(self.channelId)

    def sendStream(self, stream: Stream, timeout: int = 4000) -> int:
        """Send a stream to decoder.

        Args:
            stream(Stream): The stream data that send to decoder.
            timeout(int): timeout value(default 4000).

        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        assert self._instance, "Please create decoder."
        return sendStreamToDecoder(self.channelId, stream, timeout)

    def receiveFrame(self,
                     decOutOptions: DecOutputOptions,
                     timeout: int = 4000) -> Tuple[int, Optional[Frame]]:
        """Receive a frame from Decoder.

        Hint:
            If return code gets ``vame.WARN_MORE_DATA``, it means you need to send more streams.
            If return code gets ``vame.WARN_EOS``, it means the decoder has been stopped.

        Args:
            decOutOptions(DecOutputOptions): Decoder output options.
            timeout(int): timeout value(default 4000).

        Returns:
            Tuple[int, Optional[Frame]]: First is the return code. 0 for success, False otherwise and frame get None.
        """
        assert self._instance, "Please create decoder."
        return receiveFrameFromDecoder(self.channelId, decOutOptions, timeout)

    def jpegSync(self, imagePath: str, timeout: int = 4000) -> Frame:
        """Decode jpeg, sync api.

        Args:
            imagePath(str): The JPEG image's path.
            timeout(int): timeout value(default 4000).

        Returns:
            Frame: The decoded frame from the JPEG image.
        """
        assert self._instance, "Please create decoder."
        return jpegSyncDecoder(self.channelId, imagePath, timeout)

    def transferFrame(self, frame: Frame, crop: bool) -> Frame:
        """Transfer frame data from device to host.

        Args:
            frame(Frame): The decoded frame from teh decoder.
            crop(int): Wether to crop the frame.

        Returns:
            Frame: The frame transfered from the input frame.
        """
        assert self._instance, "Please create decoder."
        return transferFrameFromDecoder(self.channelId, frame, crop)

    def releaseFrame(self, frame: Frame, timeout: int = 4000) -> int:
        """Receive a frame from Decoder.

        Args:
            frame(Frame): The frame to be released.
            timeout(int): timeout value(default 4000).

        Returns:
            int: The return code. 0 for success, False otherwise.
        """
        assert self._instance, "Please create decoder."
        return decReleaseFrame(self.channelId, frame, timeout)

    def getStreamInfo(self) -> DecStreamInfo:
        """Get the Stream information by Decoder.

        Returns:
            DecStreamInfo: The stream information of the decoder.
        """
        assert self._instance, "Please create decoder."
        return getStreamInfoFromDecoder(self.channelId)

    def getStatus(self) -> DecStatus:
        """Get the Decoder status information.

        Returns:
            DecStatus: The status of the decoder.
        """
        assert self._instance, "Please create decoder."
        return getDecoderStatus(self.channelId)


class H264Reader():
    """H264/HEVC Reader tool class.

    There are few python libraries parse h264 or hevc, so we provide
    a tool class to parse h264/hevc, This tool class can parse a
    h264/hevc file, and put it's NALU to stream, so you can read stream
    directly from your h264/hevc file.

    Args:
        filePath(str): H264/HEVC file path.

    Examples:
        >>> with vame.H264Reader(...) as reader:
        >>>     stream = reader.readStream()
    or you can use it like this:

        >>> reader = vame.H264Reader(...)
        >>> stream = reader.readStream()
    """

    def __init__(self, filePath: str):
        if not os.path.exists(filePath):
            raise RuntimeError(f"Can not find H264/HEVC file {filePath}.")
        self.filePath = filePath
        self._h264Reader = None
        self.cnt = 0
        self.create()

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
        if self._h264Reader is None:
            self._h264Reader = _vame.H264Reader(self.filePath)
            self._h264Reader.init()

    def destroy(self) -> None:
        """Destroy the reader.
        """
        if self._h264Reader is not None:
            self._h264Reader.release()
            self._h264Reader = None

    def readStream(self) -> Optional[Stream]:
        """Read one NALU data from H264/HEVC file to a stream.

        Returns:
            Optional[Stream]: Read a stream if success else None.
        """
        assert self._h264Reader is not None, "please init the reader."
        stream = _vame.stream()
        ret = self._h264Reader.getStream(stream)
        if ret == 0:
            return None
        self.cnt += 1
        stream.pts = self.cnt
        return stream