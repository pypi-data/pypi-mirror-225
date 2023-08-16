# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .IStreamProducer import IStreamProducer
from typing import Callable
from ..InteropHelpers.InteropUtils import InteropUtils


class ITopicProducer(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ITopicProducer
        
        Returns
        ----------
        
        ITopicProducer:
            Instance wrapping the .net type ITopicProducer
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = ITopicProducer._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(ITopicProducer, cls).__new__(cls)
            ITopicProducer._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ITopicProducer
        
        Returns
        ----------
        
        ITopicProducer:
            Instance wrapping the .net type ITopicProducer
        """
        if '_ITopicProducer_pointer' in dir(self):
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
        del ITopicProducer._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("itopicproducer_createstream")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def CreateStream(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IStreamProducer
        """
        result = InteropUtils.invoke("itopicproducer_createstream", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicproducer_createstream2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def CreateStream2(self, streamId: str) -> c_void_p:
        """
        Parameters
        ----------
        
        streamId: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IStreamProducer
        """
        streamId_ptr = InteropUtils.utf8_to_ptr(streamId)
        
        result = InteropUtils.invoke("itopicproducer_createstream2", self._pointer, streamId_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicproducer_getstream")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def GetStream(self, streamId: str) -> c_void_p:
        """
        Parameters
        ----------
        
        streamId: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IStreamProducer
        """
        streamId_ptr = InteropUtils.utf8_to_ptr(streamId)
        
        result = InteropUtils.invoke("itopicproducer_getstream", self._pointer, streamId_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicproducer_getorcreatestream")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def GetOrCreateStream(self, streamId: str, onStreamCreated: Callable[[c_void_p], None] = None) -> c_void_p:
        """
        Parameters
        ----------
        
        streamId: str
            Underlying .Net type is string
        
        onStreamCreated: Callable[[c_void_p], None]
            (Optional) Underlying .Net type is Action<IStreamProducer>. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IStreamProducer
        """
        streamId_ptr = InteropUtils.utf8_to_ptr(streamId)
        onStreamCreated_func_wrapper_addr = None
        if onStreamCreated is not None:
            onStreamCreated_converter = lambda p0: onStreamCreated(c_void_p(p0))

            onStreamCreated_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p)(onStreamCreated_converter)
            onStreamCreated_func_wrapper_addr = ctypes.cast(onStreamCreated_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering onStreamCreated_converter_func_wrapper in itopicproducer_getorcreatestream, addr {}".format(onStreamCreated_func_wrapper_addr))
                onStreamCreated_func_wrapper_addr_val = onStreamCreated_func_wrapper_addr.value
                # TODO ITopicProducer._weakrefs.append(weakref.ref(onStreamCreated_converter_func_wrapper, lambda x: print("De-referenced onStreamCreated_converter_func_wrapper in itopicproducer_getorcreatestream, addr {}".format(onStreamCreated_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("itopicproducer_getorcreatestream", self._pointer, streamId_ptr, onStreamCreated_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, onStreamCreated_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicproducer_flush")
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
        InteropUtils.invoke("itopicproducer_flush", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicproducer_add_ondisposed")
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
                print("Registering value_converter_func_wrapper in itopicproducer_add_ondisposed, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO ITopicProducer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in itopicproducer_add_ondisposed, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("itopicproducer_add_ondisposed", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicproducer_remove_ondisposed")
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
        InteropUtils.invoke("itopicproducer_remove_ondisposed", self._pointer, value)
