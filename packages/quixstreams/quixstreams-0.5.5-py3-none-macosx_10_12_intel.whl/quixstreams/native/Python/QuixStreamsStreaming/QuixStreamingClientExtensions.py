# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .Models.CommitMode import CommitMode
from ..QuixStreamsTelemetry.Kafka.AutoOffsetReset import AutoOffsetReset
from .ITopicConsumer import ITopicConsumer
from ..InteropHelpers.InteropUtils import InteropUtils


class QuixStreamingClientExtensions(object):
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("quixstreamingclientextensions_gettopicconsumer")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p, ctypes.c_int, ctypes.c_int]
    @staticmethod
    def GetTopicConsumer(client: c_void_p, topicId: str, consumerGroup: str = None, commitMode: CommitMode = CommitMode.Automatic, autoOffset: AutoOffsetReset = AutoOffsetReset.Latest) -> c_void_p:
        """
        Parameters
        ----------
        
        client: c_void_p
            GC Handle Pointer to .Net type IQuixStreamingClient
        
        topicId: str
            Underlying .Net type is string
        
        consumerGroup: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        commitMode: CommitMode
            (Optional) Underlying .Net type is CommitMode. Defaults to Automatic
        
        autoOffset: AutoOffsetReset
            (Optional) Underlying .Net type is AutoOffsetReset. Defaults to Latest
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ITopicConsumer
        """
        topicId_ptr = InteropUtils.utf8_to_ptr(topicId)
        consumerGroup_ptr = InteropUtils.utf8_to_ptr(consumerGroup)
        
        result = InteropUtils.invoke("quixstreamingclientextensions_gettopicconsumer", client, topicId_ptr, consumerGroup_ptr, commitMode.value, autoOffset.value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
