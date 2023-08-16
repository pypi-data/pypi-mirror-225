# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .TimeseriesBufferConsumer import TimeseriesBufferConsumer
from typing import Callable
from ..ParameterDefinition import ParameterDefinition
from ....InteropHelpers.InteropUtils import InteropUtils


class StreamTimeseriesConsumer(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamTimeseriesConsumer
        
        Returns
        ----------
        
        StreamTimeseriesConsumer:
            Instance wrapping the .net type StreamTimeseriesConsumer
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = StreamTimeseriesConsumer._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(StreamTimeseriesConsumer, cls).__new__(cls)
            StreamTimeseriesConsumer._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamTimeseriesConsumer
        
        Returns
        ----------
        
        StreamTimeseriesConsumer:
            Instance wrapping the .net type StreamTimeseriesConsumer
        """
        if '_StreamTimeseriesConsumer_pointer' in dir(self):
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
        del StreamTimeseriesConsumer._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("streamtimeseriesconsumer_createbuffer")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def CreateBuffer(self, parametersFilter: c_void_p, bufferConfiguration: c_void_p = None) -> c_void_p:
        """
        Parameters
        ----------
        
        parametersFilter: c_void_p
            GC Handle Pointer to .Net type string[]
        
        bufferConfiguration: c_void_p
            (Optional) GC Handle Pointer to .Net type TimeseriesBufferConfiguration. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesBufferConsumer
        """
        result = InteropUtils.invoke("streamtimeseriesconsumer_createbuffer", self._pointer, parametersFilter, bufferConfiguration)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesconsumer_createbuffer2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def CreateBuffer2(self, parametersFilter: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        parametersFilter: c_void_p
            GC Handle Pointer to .Net type string[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesBufferConsumer
        """
        result = InteropUtils.invoke("streamtimeseriesconsumer_createbuffer2", self._pointer, parametersFilter)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesconsumer_add_ondefinitionschanged")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnDefinitionsChanged(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler<ParameterDefinitionsChangedEventArgs>
        
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
                print("Registering value_converter_func_wrapper in streamtimeseriesconsumer_add_ondefinitionschanged, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO StreamTimeseriesConsumer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in streamtimeseriesconsumer_add_ondefinitionschanged, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("streamtimeseriesconsumer_add_ondefinitionschanged", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesconsumer_remove_ondefinitionschanged")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnDefinitionsChanged(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("streamtimeseriesconsumer_remove_ondefinitionschanged", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesconsumer_add_ondatareceived")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnDataReceived(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler<TimeseriesDataReadEventArgs>
        
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
                print("Registering value_converter_func_wrapper in streamtimeseriesconsumer_add_ondatareceived, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO StreamTimeseriesConsumer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in streamtimeseriesconsumer_add_ondatareceived, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("streamtimeseriesconsumer_add_ondatareceived", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesconsumer_remove_ondatareceived")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnDataReceived(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("streamtimeseriesconsumer_remove_ondatareceived", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesconsumer_add_onrawreceived")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnRawReceived(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler<TimeseriesDataRawReadEventArgs>
        
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
                print("Registering value_converter_func_wrapper in streamtimeseriesconsumer_add_onrawreceived, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO StreamTimeseriesConsumer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in streamtimeseriesconsumer_add_onrawreceived, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("streamtimeseriesconsumer_add_onrawreceived", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesconsumer_remove_onrawreceived")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnRawReceived(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("streamtimeseriesconsumer_remove_onrawreceived", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesconsumer_get_definitions")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Definitions(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type List<ParameterDefinition>
        """
        result = InteropUtils.invoke("streamtimeseriesconsumer_get_definitions", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesconsumer_dispose")
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
        InteropUtils.invoke("streamtimeseriesconsumer_dispose", self._pointer)
