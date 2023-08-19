"""
Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
The information contained herein is confidential property of the company.
The user, copying, transfer or disclosure of such information is prohibited
except by express written agreement with VASTAI Technologies Co., Ltd.
"""
# coding: utf-8

from typing import Any
from _vaststream_pybind11 import vacm as _vacm
from .common import *

# =========================== ENUM =============================


class LOG_CHANNEL():
    """
    vacm log channel.\n
    ----------\n
    @enum LC_APP: app log channel.\n
    @enum LC_CM: vacm log channel.\n
    @enum LC_CE: vace log channel.\n
    @enum LC_CL: vacl log channel.\n
    @enum LC_ME: vame log channel.\n
    @enum LC_ML: vaml log channel.\n
    @enum LC_RT: runtime log channel.\n
    @enum LC_NN: vacm log channel.\n
    @enum LC_TM: vacm log channel.\n
    """
    LC_APP: int = _vacm.logChannel.vacmLC_APP
    LC_CM: int = _vacm.logChannel.vacmLC_CM
    LC_CE: int = _vacm.logChannel.vacmLC_CE
    LC_CL: int = _vacm.logChannel.vacmLC_CL
    LC_ME: int = _vacm.logChannel.vacmLC_ME
    LC_ML: int = _vacm.logChannel.vacmLC_ML
    LC_RT: int = _vacm.logChannel.vacmLC_RT
    LC_NN: int = _vacm.logChannel.vacmLC_NN
    LC_TM: int = _vacm.logChannel.vacmLC_TM


class LOG_LEVEL():
    """
    vacm log level.\n
    ----------\n
    @enum LL_TRACE: trace log level.\n
    @enum LL_DEBUG: debug log level.\n
    @enum LL_INFO: info log level.\n
    @enum LL_WARN: warn log level.\n
    @enum LL_ERROR: error log level.\n
    @enum LL_ALARM: alarm log level.\n
    @enum LL_FATAL: fatal log level.\n
    """
    LL_TRACE: int = _vacm.logLevel.vacmLL_TRACE
    LL_DEBUG: int = _vacm.logLevel.vacmLL_DEBUG
    LL_INFO: int = _vacm.logLevel.vacmLL_INFO
    LL_WARN: int = _vacm.logLevel.vacmLL_WARN
    LL_ERROR: int = _vacm.logLevel.vacmLL_ERROR
    LL_ALARM: int = _vacm.logLevel.vacmLL_ALARM
    LL_FATAL: int = _vacm.logLevel.vacmLL_FATAL

# =========================== API =============================


def initLogger() -> int:
    """
    Initialize logger system for message logging.\n
    ------------\n
    """
    return _vacm.initLogger()


def logMessage(logChannel: LOG_CHANNEL, logLevel: LOG_LEVEL, fmt: str) -> int:
    """
    Write a message to the log file.\n
    ------------\n
    logChannel [in]: The log channel, which is pre-configured in the log configuration file.\n
    logLevel [in]: The log level.
    """
    return _vacm.logMessage(logChannel, logLevel, fmt)
