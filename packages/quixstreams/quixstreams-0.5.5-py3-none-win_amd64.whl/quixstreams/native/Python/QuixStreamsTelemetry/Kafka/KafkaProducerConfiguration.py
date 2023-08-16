# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...InteropHelpers.InteropUtils import InteropUtils


class KafkaProducerConfiguration(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type KafkaProducerConfiguration
        
        Returns
        ----------
        
        KafkaProducerConfiguration:
            Instance wrapping the .net type KafkaProducerConfiguration
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = KafkaProducerConfiguration._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(KafkaProducerConfiguration, cls).__new__(cls)
            KafkaProducerConfiguration._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type KafkaProducerConfiguration
        
        Returns
        ----------
        
        KafkaProducerConfiguration:
            Instance wrapping the .net type KafkaProducerConfiguration
        """
        if '_KafkaProducerConfiguration_pointer' in dir(self):
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
        del KafkaProducerConfiguration._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("kafkaproducerconfiguration_constructor")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Constructor(brokerList: str, properties: c_void_p = None) -> c_void_p:
        """
        Parameters
        ----------
        
        brokerList: str
            Underlying .Net type is string
        
        properties: c_void_p
            (Optional) GC Handle Pointer to .Net type IDictionary<string, string>. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type KafkaProducerConfiguration
        """
        brokerList_ptr = InteropUtils.utf8_to_ptr(brokerList)
        
        result = InteropUtils.invoke("kafkaproducerconfiguration_constructor", brokerList_ptr, properties)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("kafkaproducerconfiguration_get_brokerlist")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_BrokerList(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("kafkaproducerconfiguration_get_brokerlist", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("kafkaproducerconfiguration_get_maxmessagesize")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_MaxMessageSize(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("kafkaproducerconfiguration_get_maxmessagesize", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("kafkaproducerconfiguration_get_maxkeysize")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_MaxKeySize(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("kafkaproducerconfiguration_get_maxkeysize", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("kafkaproducerconfiguration_get_properties")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Properties(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IDictionary<string, string>
        """
        result = InteropUtils.invoke("kafkaproducerconfiguration_get_properties", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
