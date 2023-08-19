# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.

__all__ = ["__version__", "__time_compiled__"]

# import os
# import ctypes

# 校验C++库安装
# LIB_PATH = "/opt/vastai/vaststream2.0"  # 安装到指定位置
# if not os.path.exists(LIB_PATH):
#     raise Exception(
#         f"Please install vaststream c++ library, can not find library in {LIB_PATH}."
#     )

# # 校验C++库版本
# VACM_LIB_PATH = os.path.join(LIB_PATH, "lib", "libvacm.so")
# VERSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                             "VERSION")
# with open(VERSION_FILE, "r") as f:
#     version = f.read()
# lib = ctypes.CDLL(VACM_LIB_PATH)

# ver = ctypes.c_char_p()
# major = ctypes.c_uint32(0)
# minor = ctypes.c_uint32(0)
# rev = ctypes.c_uint32(0)
# bn = ctypes.c_uint32(0)
# lib.vacmGetVersion.argtypes = (ctypes.POINTER(ctypes.c_char_p),
#                                ctypes.POINTER(ctypes.c_uint32),
#                                ctypes.POINTER(ctypes.c_uint32),
#                                ctypes.POINTER(ctypes.c_uint32),
#                                ctypes.POINTER(ctypes.c_uint32))
# lib.vacmGetVersion(ctypes.pointer(ver), ctypes.pointer(major),
#                    ctypes.pointer(minor), ctypes.pointer(rev),
#                    ctypes.pointer(bn))
# lib_version = f"{major.value}.{minor.value}.{rev.value}.{bn.value}"
# TODO: 现在发布C++发布流程有问题，校验失败，需要修复
# if version != lib_version:
#     raise Exception(
#         f"Python version {version} can not match c++ library version {lib_version}"
#     )

from _vaststream_pybind11 import __version__, __time_compiled__