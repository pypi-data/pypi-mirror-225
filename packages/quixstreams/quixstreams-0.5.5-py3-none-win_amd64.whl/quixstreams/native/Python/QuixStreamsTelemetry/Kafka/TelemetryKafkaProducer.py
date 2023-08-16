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


class TelemetryKafkaProducer(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TelemetryKafkaProducer
        
        Returns
        ----------
        
        TelemetryKafkaProducer:
            Instance wrapping the .net type TelemetryKafkaProducer
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = TelemetryKafkaProducer._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(TelemetryKafkaProducer, cls).__new__(cls)
            TelemetryKafkaProducer._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TelemetryKafkaProducer
        
        Returns
        ----------
        
        TelemetryKafkaProducer:
            Instance wrapping the .net type TelemetryKafkaProducer
        """
        if '_TelemetryKafkaProducer_pointer' in dir(self):
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
        del TelemetryKafkaProducer._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("telemetrykafkaproducer_constructor")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Constructor(producer: c_void_p, byteSplitter: c_void_p, streamId: str = None) -> c_void_p:
        """
        Parameters
        ----------
        
        producer: c_void_p
            GC Handle Pointer to .Net type IProducer
        
        byteSplitter: c_void_p
            GC Handle Pointer to .Net type IByteSplitter
        
        streamId: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TelemetryKafkaProducer
        """
        streamId_ptr = InteropUtils.utf8_to_ptr(streamId)
        
        result = InteropUtils.invoke("telemetrykafkaproducer_constructor", producer, byteSplitter, streamId_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaproducer_get_streamid")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_StreamId(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("telemetrykafkaproducer_get_streamid", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaproducer_add_onwriteexception")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnWriteException(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler<Exception>
        
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
                print("Registering value_converter_func_wrapper in telemetrykafkaproducer_add_onwriteexception, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO TelemetryKafkaProducer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in telemetrykafkaproducer_add_onwriteexception, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("telemetrykafkaproducer_add_onwriteexception", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaproducer_remove_onwriteexception")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnWriteException(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("telemetrykafkaproducer_remove_onwriteexception", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaproducer_dispose")
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
        InteropUtils.invoke("telemetrykafkaproducer_dispose", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaproducer_get_onstreampipelineassigned")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_OnStreamPipelineAssigned(self) -> Callable[[], None]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Callable[[], None]:
            Underlying .Net type is Action
        """
        result = InteropUtils.invoke("telemetrykafkaproducer_get_onstreampipelineassigned", self._pointer)
        return Exception("NOT IMPLEMENTED YET")
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaproducer_set_onstreampipelineassigned")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_OnStreamPipelineAssigned(self, value: Callable[[], None]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[], None]
            Underlying .Net type is Action
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda : value()

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in telemetrykafkaproducer_set_onstreampipelineassigned, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO TelemetryKafkaProducer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in telemetrykafkaproducer_set_onstreampipelineassigned, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("telemetrykafkaproducer_set_onstreampipelineassigned", self._pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
