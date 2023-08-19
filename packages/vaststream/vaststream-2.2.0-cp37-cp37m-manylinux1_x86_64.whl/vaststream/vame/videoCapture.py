# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

__all__ = ["VideoCapture"]

import os
import importlib
import uuid
import time
import queue
import warnings
import subprocess
import numpy as np
from vaststream import vacm
from threading import Thread
from typing import Optional
from .common import *
from .decoder import *
from .utils import ChannelIdGenerator

WAIT_INTERVAL = 0.01
WAIT_READY_MAX = 10

DECODE_STATUS_INIT = 0
DECODE_STATUS_READY = 1
DECODE_STATUS_RUNNING = 2
DECODE_STATUS_PYAV_FINISH = 3
DECODE_STATUS_STOP = 4
DECODE_STATUS_ERROR = 5
DECODE_STATUS_EXIT = 6


class STREAM_TYPE():
    H264: str = "h264"
    HEVC: str = "hevc"
    MP4: str = "mp4"
    RTSP: str = "rtsp"


def gen_unique_channel_id():
    """Interface of generate global unique id number
    
    Returns:
        int: The current channel id
    """
    generator = ChannelIdGenerator()
    return generator.generator_channel_id()


class VaVdec(object):
    """Vastai video decoder tool class.

    Args:
        channel_id (int): decode channel id,must be global unique
        width (int): image width 
        height (int): image height
        entype (_type_): encode type
        ctx (Context):  context in the device
    """

    def __init__(self,
                 channel_id: int,
                 codec_type: CODEC_TYPE,
                 qSize: int = 8):
        self._channel_id = channel_id
        self._codec_type = codec_type
        self._frame_queue = queue.Queue(qSize)
        self._decoder = None
        self._receive_thread = None
        self._status = DECODE_STATUS_INIT

    def __del__(self):
        self.destroy()

    def _receive_thread_entry(self, ctx: vacm.Context):
        vacm.setCurrentContext(ctx)
        decOutOptions = DecOutputOptions()
        decOutOptions.enableCrop = 1
        decOutOptions.memoryType = MEMORY_TYPE.HOST
        while True:
            if self._status >= DECODE_STATUS_ERROR:
                break
            ret, frame = self._decoder.receiveFrame(decOutOptions)
            if ret == WARN_EOS:
                self._status = DECODE_STATUS_EXIT
                break
            if ret == WARN_MORE_DATA:
                continue
            if frame:
                # 等待队列消费
                while self._frame_queue.full():
                    time.sleep(WAIT_INTERVAL)
                self._frame_queue.put(frame)
                self._decoder.releaseFrame(frame)

    def init(self) -> None:
        """Create Vastai decoder channel
        """
        dec_params = DecChannelParamters()
        dec_params.codecType = self._codec_type
        dec_params.sourceMode = SOURCE_MODE.SRC_FRAME
        dec_params.decodeMode = DECODE_MODE.NORMAL
        dec_params.pixelFormat = PIXEL_FORMAT.NV12
        dec_params.extraBufferNumber = 10
        # 创建解码器
        self._decoder = Decoder(self._channel_id,
                                dec_params,
                                auto_start=False,
                                auto_init=True)
        self._decoder.start()
        # 开启接收线程
        self._receive_thread = Thread(target=self._receive_thread_entry,
                                      args=(vacm.getCurrentContext(), ))
        self._receive_thread.start()
        self._status = DECODE_STATUS_READY

    def process(self, input_data: Stream) -> None:
        """
        send stream to Decoder for decoding

        Args:
            input_data (Stream): _description_
        """
        if self._status == DECODE_STATUS_READY:
            self._status = DECODE_STATUS_RUNNING
        if self._status != DECODE_STATUS_RUNNING:
            raise RuntimeError(f"Process get error status: {self._status}.")
        # 满队列阻塞等待消费
        while self._frame_queue.full():
            warnings.warn("Frame queue is full, Please read faster.")
            time.sleep(WAIT_INTERVAL)
        self._decoder.sendStream(input_data)

    def stop(self) -> None:
        self._decoder.stop()
        self._status = DECODE_STATUS_STOP

    def destroy(self) -> None:
        self._status = DECODE_STATUS_EXIT
        if self._decoder is not None:
            self._receive_thread.join()
            self._decoder.destroy()
            self._frame_queue.empty()
            self._decoder = None

    def read(self) -> Optional[Frame]:
        # 结束状态返回None
        if self._status == DECODE_STATUS_EXIT and self._frame_queue.empty():
            return None
        frame = self._frame_queue.get()
        return frame


class VideoCapture():
    """The VideoCapture tool class.

    You can use this like opencv's videoCapture, this class only support annex-b **h264/h265**
    file or **mp4** file.

    Important:
        If you want to use this class, please install av lib(pip install av).

    Important:
        If you decode mp4 file, please make sure you know what happend, the pyav library can
        not support bsf, so we use ffmpeg shell to transfer mp4 to h264/hevc file, there will
        be a tmp file created in the directory of the mp4 file, and it will be destroyed when
        the class destroyed.If you do not have ffmpeg installed in your device, there maybe
        something wrong happen.Also you can transfer manually, use command:

        ``ffmpeg -i xxx.mp4 -codec copy -bsf: h264_mp4toannexb -f h264 xxx.h264``

    Args:
        stream_name: video stream name.

    Examples:
        >>> with vame.VideoCapture(...) as cap:
        >>>     while True:
        >>>         frame = cap.read()
        >>>         if frame is None: break
    or you can use it like this:

        >>> cap = vame.VideoCapture(...)
        >>> while True:
        >>>     frame = cap.read()
        >>>     if frame is None: break
    """

    def __init__(self, strame_name):
        self.__check_av()
        self.stream_name = strame_name
        self._width = 0
        self._height = 0
        self._vdec = None
        self._codec_type = None
        self._stream_type = None
        self._stream_tmp = None
        self._decode_thread = None
        self._status = DECODE_STATUS_INIT
        self._check_stream()
        self._open()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._destroy()

    def __del__(self):
        self._destroy()
    
    def __check_av(self):
        try:
            self.av = importlib.import_module('av')
        except Exception as e:
            raise RuntimeError("Please install av lib(pip install av).")

    @property
    def width(self) -> int:
        """The width of the stream."""
        return self._width

    @property
    def height(self) -> int:
        """The height of the stream."""
        return self._height

    @property
    def codec_type(self) -> CODEC_TYPE:
        """The codec type of the stream."""
        return self._codec_type

    def _open(self):
        # ffmpeg解析参数
        self._get_param()
        self._mp4toannexb()
        # 开启硬解码线程
        self._decode_thread = Thread(target=self._decode_thread_entry,
                                     args=(vacm.getCurrentContext(), ))
        self._decode_thread.start()

        # Wait decode thread decode ready
        for _ in range(0, WAIT_READY_MAX):
            if self._status == DECODE_STATUS_INIT:
                time.sleep(WAIT_INTERVAL)

        if self._status != DECODE_STATUS_READY:
            raise RuntimeError(
                f"Open {self.stream_name} failed for waiting decoder to be ready."
            )

    def _check_stream(self):
        # 校验支持的文件格式
        stream_name_lower = self.stream_name.lower()
        if stream_name_lower.endswith(".mp4"):
            self._stream_type = STREAM_TYPE.MP4
        elif stream_name_lower.endswith(".h264"):
            self._stream_type = STREAM_TYPE.H264
        elif stream_name_lower.endswith(".hevc"):
            self._stream_type = STREAM_TYPE.HEVC
        # TODO: 支持rtsp 
        # elif stream_name_lower.startswith("rtsp://"):
        #     self._stream_type = STREAM_TYPE.RTSP
        else:
            raise RuntimeError("Only support .mp4 .h264 .hevc stream.")

    def _mp4toannexb(self):
        # av库不支持bsf，这里用ffmpeg命令转换
        if self._stream_type == STREAM_TYPE.MP4:
            stream_dir = os.path.dirname(self.stream_name)
            stream_base_name = os.path.basename(
                self.stream_name).split('.')[0] + '-' + uuid.uuid4().hex
            if self.codec_type == CODEC_TYPE.DEC_H264:
                stream_tmp_path = os.path.join(stream_dir,
                                               stream_base_name + '.h264')
                bsf = "h264_mp4toannexb"
            elif self.codec_type == CODEC_TYPE.DEC_HEVC:
                stream_tmp_path = os.path.join(stream_dir,
                                               stream_base_name + '.hevc')
                bsf = "hevc_mp4toannexb"
            self._stream_tmp = stream_tmp_path
            # shell转换
            try:
                subprocess.check_call([
                    "ffmpeg",
                    "-i",
                    self.stream_name,
                    "-vcodec",
                    "copy",
                    "-an",
                    "-bsf:v",
                    bsf,
                    stream_tmp_path,
                ])
            except:
                raise RuntimeError("Please check your ffmpeg can work.")
            assert os.path.exists(self._stream_tmp)
            self.stream_name = self._stream_tmp

    def _get_param(self):
        # 通过ffmpeg获取stream各种参数信息
        container = self.av.open(self.stream_name)
        stream = [s for s in container.streams if s.type == 'video']
        if len(stream) == 0:
            # The stream is not video
            raise RuntimeError(
                f"Can not find video stream in {self.stream_name}.")

        video_context = container.streams.video[0].codec_context
        self._width = video_context.width
        self._height = video_context.height
        codec_id_name = video_context.name
        self._codec_type = self._get_codec_type(codec_id_name)

        container.close()

    def _get_codec_type(self, codec_id_name):
        # 获取vame支持的编码协议
        codec_type_tbl = {
            'h264': CODEC_TYPE.DEC_H264,
            'hevc': CODEC_TYPE.DEC_HEVC
        }

        if codec_id_name in codec_type_tbl.keys():
            return codec_type_tbl[codec_id_name]
        else:
            raise RuntimeError(f"Unsupported codec type {codec_id_name}.")

    def _decode_thread_entry(self, ctx: vacm.Context):
        vacm.setCurrentContext(ctx)

        channelId = gen_unique_channel_id()
        self._vdec = VaVdec(channelId, self._codec_type)
        # 创建编码器，开启接收线程
        self._vdec.init()
        self._status = DECODE_STATUS_READY

        # read开始后再发送解码数据
        while (self._status == DECODE_STATUS_READY):
            time.sleep(WAIT_INTERVAL)

        # 发送数据到解码器
        container = self.av.open(self.stream_name)
        video_stream = next(s for s in container.streams if s.type == 'video')
        cnt = 0
        for packet in container.demux(video_stream):
            if self._status != DECODE_STATUS_RUNNING:
                break
            # Get stream from packet
            pkt = np.frombuffer(packet.to_bytes(), np.uint8)
            size = pkt.size
            if size == 0:
                # Last frame data is empty
                self._status = DECODE_STATUS_PYAV_FINISH
                self._vdec.stop()
            else:
                cnt += 1
                stream = Stream()
                stream.stream = pkt
                stream.pts = cnt
                self._vdec.process(stream)

        # 等待read结束
        while self._status < DECODE_STATUS_STOP:
            time.sleep(WAIT_INTERVAL)
        # 销毁解码器
        self._status = DECODE_STATUS_EXIT
        if self._vdec is not None:
            self._vdec.destroy()
            self._vdec = None

    def _destroy(self):
        self._status = DECODE_STATUS_EXIT
        if self._vdec is not None:
            self._vdec.destroy()
            self._vdec = None
        if self._stream_tmp is not None:
            os.remove(self._stream_tmp)
            self._stream_tmp = None

    def read(self):
        """Read decoded frame.

        Returns:
            Optional[Frame]: Get None if read over else frame from stream.
        """
        # 解码结束
        if self._status == DECODE_STATUS_EXIT:
            return None

        # 首次读完解码数据，开始往解码器发送数据
        if self._status == DECODE_STATUS_READY:
            self._status = DECODE_STATUS_RUNNING
        frame = self._vdec.read()

        # 解码结束
        if frame is None:
            self._status = DECODE_STATUS_STOP
            self._decode_thread.join()
        return frame