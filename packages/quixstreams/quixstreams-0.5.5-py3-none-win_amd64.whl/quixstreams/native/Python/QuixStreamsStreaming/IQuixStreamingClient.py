# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ..QuixStreamsTelemetry.Kafka.AutoOffsetReset import AutoOffsetReset
from .ITopicConsumer import ITopicConsumer
from .Raw.IRawTopicConsumer import IRawTopicConsumer
from .Raw.IRawTopicProducer import IRawTopicProducer
from .ITopicProducer import ITopicProducer
from ..InteropHelpers.InteropUtils import InteropUtils


class IQuixStreamingClient(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type IQuixStreamingClient
        
        Returns
        ----------
        
        IQuixStreamingClient:
            Instance wrapping the .net type IQuixStreamingClient
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = IQuixStreamingClient._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(IQuixStreamingClient, cls).__new__(cls)
            IQuixStreamingClient._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type IQuixStreamingClient
        
        Returns
        ----------
        
        IQuixStreamingClient:
            Instance wrapping the .net type IQuixStreamingClient
        """
        if '_IQuixStreamingClient_pointer' in dir(self):
            return
        
        if type(net_pointer) is not c_void_p:
            self._pointer_owner = net_pointer
            self._pointer = net_pointer.get_interop_ptr__()
        else:
            self._pointer = net_pointer
        
        if finalize:
            self._finalizer = weakref.finalize(self, self._finalizerfunc)
            self._finalizer.atexit = False
        else:
            self._finalizer = lambda: None
    
    def _finalizerfunc(self):
        del IQuixStreamingClient._weakrefs[self._pointer.value]
        InteropUtils.free_hptr(self._pointer)
        self._finalizer.detach()
    
    def get_interop_ptr__(self) -> c_void_p:
        return self._pointer
    
    def dispose_ptr__(self):
        self._finalizer()
    
    def __enter__(self):
        pass
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._finalizer()
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("iquixstreamingclient_gettopicconsumer")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p, ctypes.c_int]
    def GetTopicConsumer(self, topicIdOrName: str, consumerGroup: str = None, options: c_void_p = None, autoOffset: AutoOffsetReset = AutoOffsetReset.Latest) -> c_void_p:
        """
        Parameters
        ----------
        
        topicIdOrName: str
            Underlying .Net type is string
        
        consumerGroup: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        options: c_void_p
            (Optional) GC Handle Pointer to .Net type CommitOptions. Defaults to None
        
        autoOffset: AutoOffsetReset
            (Optional) Underlying .Net type is AutoOffsetReset. Defaults to Latest
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ITopicConsumer
        """
        topicIdOrName_ptr = InteropUtils.utf8_to_ptr(topicIdOrName)
        consumerGroup_ptr = InteropUtils.utf8_to_ptr(consumerGroup)
        
        result = InteropUtils.invoke("iquixstreamingclient_gettopicconsumer", self._pointer, topicIdOrName_ptr, consumerGroup_ptr, options, autoOffset.value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("iquixstreamingclient_getrawtopicconsumer")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p, InteropUtils.create_nullable(ctypes.c_int)]
    def GetRawTopicConsumer(self, topicIdOrName: str, consumerGroup: str = None, autoOffset: Optional[AutoOffsetReset] = None) -> c_void_p:
        """
        Parameters
        ----------
        
        topicIdOrName: str
            Underlying .Net type is string
        
        consumerGroup: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        autoOffset: Optional[AutoOffsetReset]
            (Optional) Underlying .Net type is AutoOffsetReset?. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IRawTopicConsumer
        """
        topicIdOrName_ptr = InteropUtils.utf8_to_ptr(topicIdOrName)
        consumerGroup_ptr = InteropUtils.utf8_to_ptr(consumerGroup)
        autoOffset_conv = autoOffset.value
        autoOffset_nullable = InteropUtils.create_nullable(ctypes.c_int)(autoOffset_conv)
        
        result = InteropUtils.invoke("iquixstreamingclient_getrawtopicconsumer", self._pointer, topicIdOrName_ptr, consumerGroup_ptr, autoOffset_nullable)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("iquixstreamingclient_getrawtopicproducer")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def GetRawTopicProducer(self, topicIdOrName: str) -> c_void_p:
        """
        Parameters
        ----------
        
        topicIdOrName: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IRawTopicProducer
        """
        topicIdOrName_ptr = InteropUtils.utf8_to_ptr(topicIdOrName)
        
        result = InteropUtils.invoke("iquixstreamingclient_getrawtopicproducer", self._pointer, topicIdOrName_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("iquixstreamingclient_gettopicproducer")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def GetTopicProducer(self, topicIdOrName: str) -> c_void_p:
        """
        Parameters
        ----------
        
        topicIdOrName: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ITopicProducer
        """
        topicIdOrName_ptr = InteropUtils.utf8_to_ptr(topicIdOrName)
        
        result = InteropUtils.invoke("iquixstreamingclient_gettopicproducer", self._pointer, topicIdOrName_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
