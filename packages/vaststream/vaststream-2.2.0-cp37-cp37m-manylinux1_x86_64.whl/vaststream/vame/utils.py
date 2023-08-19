# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# coding: utf-8

__all__ = ["err_check", "ChannelIdGenerator"]

import threading
from functools import wraps
from _vaststream_pybind11 import vame as _vame


def err_check(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if ret != _vame.vameER_SUCCESS:
            raise RuntimeError(f"{func.__name__} error, ret: {ret}.")
        return ret

    return wrapper


class ChannelIdGenerator():
    """Generate global unique id number, single instance mode class
    """
    _instance = None
    _instance_lock = threading.Lock()
    channel_id = 0

    def __init__(self):
        """Create a channel id generator instance 
        """
        pass

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def generator_channel_id(self):
        """Generate global unique id number, the id number is increase
        
        Returns:
            int: The current channel id
        """
        curren_channel_id = 0
        with ChannelIdGenerator._instance_lock:
            curren_channel_id = ChannelIdGenerator.channel_id
            ChannelIdGenerator.channel_id += 1

        return curren_channel_id