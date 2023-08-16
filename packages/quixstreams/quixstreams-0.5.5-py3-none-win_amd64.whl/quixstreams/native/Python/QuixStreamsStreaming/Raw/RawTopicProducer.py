# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from typing import Callable
from ...InteropHelpers.InteropUtils import InteropUtils


class RawTopicProducer(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type RawTopicProducer
        
        Returns
        ----------
        
        RawTopicProducer:
            Instance wrapping the .net type RawTopicProducer
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = RawTopicProducer._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(RawTopicProducer, cls).__new__(cls)
            RawTopicProducer._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type RawTopicProducer
        
        Returns
        ----------
        
        RawTopicProducer:
            Instance wrapping the .net type RawTopicProducer
        """
        if '_RawTopicProducer_pointer' in dir(self):
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
        del RawTopicProducer._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("rawtopicproducer_constructor")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Constructor(brokerAddress: str, topicName: str, brokerProperties: c_void_p = None) -> c_void_p:
        """
        Parameters
        ----------
        
        brokerAddress: str
            Underlying .Net type is string
        
        topicName: str
            Underlying .Net type is string
        
        brokerProperties: c_void_p
            (Optional) GC Handle Pointer to .Net type Dictionary<string, string>. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type RawTopicProducer
        """
        brokerAddress_ptr = InteropUtils.utf8_to_ptr(brokerAddress)
        topicName_ptr = InteropUtils.utf8_to_ptr(topicName)
        
        result = InteropUtils.invoke("rawtopicproducer_constructor", brokerAddress_ptr, topicName_ptr, brokerProperties)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("rawtopicproducer_add_ondisposed")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnDisposed(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IntPtr
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0, p1: value(c_void_p(p0), c_void_p(p1))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in rawtopicproducer_add_ondisposed, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO RawTopicProducer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in rawtopicproducer_add_ondisposed, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("rawtopicproducer_add_ondisposed", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("rawtopicproducer_remove_ondisposed")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnDisposed(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type IntPtr
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("rawtopicproducer_remove_ondisposed", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("rawtopicproducer_publish")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Publish(self, message: c_void_p) -> None:
        """
        Parameters
        ----------
        
        message: c_void_p
            GC Handle Pointer to .Net type RawMessage
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("rawtopicproducer_publish", self._pointer, message)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("rawtopicproducer_flush")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def Flush(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("rawtopicproducer_flush", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("rawtopicproducer_dispose")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def Dispose(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("rawtopicproducer_dispose", self._pointer)
