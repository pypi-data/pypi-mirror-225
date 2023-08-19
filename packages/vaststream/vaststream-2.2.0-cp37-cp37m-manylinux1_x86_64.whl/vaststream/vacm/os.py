# """
# Copyright (C) 2022-2023 VASTAI Technologies Co., Ltd. All Rights Reserved.
# The information contained herein is confidential property of the company.
# The user, copying, transfer or disclosure of such information is prohibited
# except by express written agreement with VASTAI Technologies Co., Ltd.
# """
# # coding: utf-8
# from _vaststream_pybind11 import vacm
# from .common import *


# def createEvent(autoReset: bool) -> any:
#     """
#     Create an event object for inter-process synchronization.\n
#     ----------\n
#     autoReset [in]: If reset the event automatically..\n
#     """
#     return vacm.createEvent(autoReset)


# @err_check
# def waitEvent(evt: any, timeout: int) -> int:
#     """
#     Wait for an event object to be signaled.\n
#     """
#     return vacm.waitEvent(evt, timeout)


# @err_check
# def setEvent(evt: any) -> int:
#     """
#     Set an event object to be signaled state.\n
#     """
#     return vacm.setEvent(evt)


# @err_check
# def resetEvent(evt: any) -> int:
#     """
#     Reset an event object to be un-signaled state.\n
#     """
#     return vacm.resetEvent(evt)


# @err_check
# def destroyEvent(evt: any) -> int:
#     """
#     Destroy an event object.\n
#     """
#     return vacm.destroyEvent(evt)


# def createMutex() -> any:
#     """
#     Create a mutex object for inter-thread synchronization.\n
#     """
#     return vacm.createMutex()


# @err_check
# def lockMutex(mtx: any) -> int:
#     """
#     Lock a mutex object. It will block until other thread exit the object.\n
#     """
#     return vacm.lockMutex(mtx)


# def tryLockMutex(mtx: any) -> bool:
#     """
#     Lock a mutex object. It will block until other thread exit the object.\n
#     """
#     return vacm.tryLockMutex(mtx)


# @err_check
# def unlockMutex(mtx: any) -> int:
#     """
#     Unlock a mutex object.\n
#     """
#     return vacm.unlockMutex(mtx)


# @err_check
# def destroyMutex(mtx: any) -> int:
#     """
#     Destroy a mutex object\n
#     """
#     return vacm.destroyMutex(mtx)


# def createCondVariable() -> any:
#     """
#     Create a condition variable object for inter-process synchronization.\n
#     """
#     return vacm.createCondVariable()


# @err_check
# def waitCondVariable(cdv: any, mtx: any, timeout: int) -> int:
#     """
#     Wait for a condition variable object to be notified.\n
#     """
#     return vacm.waitCondVariable(cdv, mtx, timeout)


# @err_check
# def notifyCondVariable(cdv: any) -> int:
#     """
#     Notify a waiting thread that a condition variable object is in met state.\n
#     """
#     return vacm.notifyCondVariable(cdv)


# @err_check
# def notifyAllCondVariable(cdv: any) -> int:
#     """
#     Notify all waiting threads that a condition variable object is in met state.\n
#     """
#     return vacm.notifyAllCondVariable(cdv)


# def destroyCondVariable(cdv: any) -> int:
#     """
#     Destroy a condition variable object.\n
#     """
#     return vacm.destroyCondVariable(cdv)
