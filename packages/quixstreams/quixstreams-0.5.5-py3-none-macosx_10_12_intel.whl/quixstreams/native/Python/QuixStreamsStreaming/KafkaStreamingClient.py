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


class KafkaStreamingClient(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type KafkaStreamingClient
        
        Returns
        ----------
        
        KafkaStreamingClient:
            Instance wrapping the .net type KafkaStreamingClient
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = KafkaStreamingClient._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(KafkaStreamingClient, cls).__new__(cls)
            KafkaStreamingClient._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type KafkaStreamingClient
        
        Returns
        ----------
        
        KafkaStreamingClient:
            Instance wrapping the .net type KafkaStreamingClient
        """
        if '_KafkaStreamingClient_pointer' in dir(self):
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
        del KafkaStreamingClient._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("kafkastreamingclient_constructor")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p, ctypes.c_ubyte]
    @staticmethod
    def Constructor(brokerAddress: str, securityOptions: c_void_p = None, properties: c_void_p = None, debug: bool = False) -> c_void_p:
        """
        Parameters
        ----------
        
        brokerAddress: str
            Underlying .Net type is string
        
        securityOptions: c_void_p
            (Optional) GC Handle Pointer to .Net type SecurityOptions. Defaults to None
        
        properties: c_void_p
            (Optional) GC Handle Pointer to .Net type IDictionary<string, string>. Defaults to None
        
        debug: bool
            (Optional) Underlying .Net type is Boolean. Defaults to False
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type KafkaStreamingClient
        """
        brokerAddress_ptr = InteropUtils.utf8_to_ptr(brokerAddress)
        debug_bool = 1 if debug else 0
        
        result = InteropUtils.invoke("kafkastreamingclient_constructor", brokerAddress_ptr, securityOptions, properties, debug_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("kafkastreamingclient_gettopicconsumer")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p, ctypes.c_int]
    def GetTopicConsumer(self, topic: str, consumerGroup: str = None, options: c_void_p = None, autoOffset: AutoOffsetReset = AutoOffsetReset.Latest) -> c_void_p:
        """
        Parameters
        ----------
        
        topic: str
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
        topic_ptr = InteropUtils.utf8_to_ptr(topic)
        consumerGroup_ptr = InteropUtils.utf8_to_ptr(consumerGroup)
        
        result = InteropUtils.invoke("kafkastreamingclient_gettopicconsumer", self._pointer, topic_ptr, consumerGroup_ptr, options, autoOffset.value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("kafkastreamingclient_getrawtopicconsumer")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p, InteropUtils.create_nullable(ctypes.c_int)]
    def GetRawTopicConsumer(self, topic: str, consumerGroup: str = None, autoOffset: Optional[AutoOffsetReset] = None) -> c_void_p:
        """
        Parameters
        ----------
        
        topic: str
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
        topic_ptr = InteropUtils.utf8_to_ptr(topic)
        consumerGroup_ptr = InteropUtils.utf8_to_ptr(consumerGroup)
        autoOffset_conv = autoOffset.value
        autoOffset_nullable = InteropUtils.create_nullable(ctypes.c_int)(autoOffset_conv)
        
        result = InteropUtils.invoke("kafkastreamingclient_getrawtopicconsumer", self._pointer, topic_ptr, consumerGroup_ptr, autoOffset_nullable)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("kafkastreamingclient_getrawtopicproducer")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def GetRawTopicProducer(self, topic: str) -> c_void_p:
        """
        Parameters
        ----------
        
        topic: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IRawTopicProducer
        """
        topic_ptr = InteropUtils.utf8_to_ptr(topic)
        
        result = InteropUtils.invoke("kafkastreamingclient_getrawtopicproducer", self._pointer, topic_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("kafkastreamingclient_gettopicproducer")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def GetTopicProducer(self, topic: str) -> c_void_p:
        """
        Parameters
        ----------
        
        topic: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ITopicProducer
        """
        topic_ptr = InteropUtils.utf8_to_ptr(topic)
        
        result = InteropUtils.invoke("kafkastreamingclient_gettopicproducer", self._pointer, topic_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
