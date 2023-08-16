# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ....SystemPrivateCoreLib.System.DateTime import DateTime
from .TimeseriesDataBuilder import TimeseriesDataBuilder
from ....InteropHelpers.InteropUtils import InteropUtils


class TimeseriesBufferProducer(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TimeseriesBufferProducer
        
        Returns
        ----------
        
        TimeseriesBufferProducer:
            Instance wrapping the .net type TimeseriesBufferProducer
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = TimeseriesBufferProducer._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(TimeseriesBufferProducer, cls).__new__(cls)
            TimeseriesBufferProducer._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TimeseriesBufferProducer
        
        Returns
        ----------
        
        TimeseriesBufferProducer:
            Instance wrapping the .net type TimeseriesBufferProducer
        """
        if '_TimeseriesBufferProducer_pointer' in dir(self):
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
        del TimeseriesBufferProducer._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("timeseriesbufferproducer_get_epoch")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Epoch(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("timeseriesbufferproducer_get_epoch", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbufferproducer_set_epoch")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_Epoch(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("timeseriesbufferproducer_set_epoch", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbufferproducer_addtimestamp")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def AddTimestamp(self, dateTime: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        dateTime: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataBuilder
        """
        result = InteropUtils.invoke("timeseriesbufferproducer_addtimestamp", self._pointer, dateTime)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbufferproducer_addtimestamp2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def AddTimestamp2(self, timeSpan: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        timeSpan: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataBuilder
        """
        result = InteropUtils.invoke("timeseriesbufferproducer_addtimestamp2", self._pointer, timeSpan)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbufferproducer_addtimestampmilliseconds")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_longlong]
    def AddTimestampMilliseconds(self, timeMilliseconds: int) -> c_void_p:
        """
        Parameters
        ----------
        
        timeMilliseconds: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataBuilder
        """
        timeMilliseconds_long = ctypes.c_longlong(timeMilliseconds)
        
        result = InteropUtils.invoke("timeseriesbufferproducer_addtimestampmilliseconds", self._pointer, timeMilliseconds_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbufferproducer_addtimestampnanoseconds")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_longlong]
    def AddTimestampNanoseconds(self, timeNanoseconds: int) -> c_void_p:
        """
        Parameters
        ----------
        
        timeNanoseconds: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataBuilder
        """
        timeNanoseconds_long = ctypes.c_longlong(timeNanoseconds)
        
        result = InteropUtils.invoke("timeseriesbufferproducer_addtimestampnanoseconds", self._pointer, timeNanoseconds_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbufferproducer_publish")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Publish(self, data: c_void_p) -> None:
        """
        Parameters
        ----------
        
        data: c_void_p
            GC Handle Pointer to .Net type TimeseriesData
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("timeseriesbufferproducer_publish", self._pointer, data)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbufferproducer_publish2")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Publish2(self, data: c_void_p) -> None:
        """
        Parameters
        ----------
        
        data: c_void_p
            GC Handle Pointer to .Net type TimeseriesDataRaw
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("timeseriesbufferproducer_publish2", self._pointer, data)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbufferproducer_publish3")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Publish3(self, timestamp: c_void_p) -> None:
        """
        Parameters
        ----------
        
        timestamp: c_void_p
            GC Handle Pointer to .Net type TimeseriesDataTimestamp
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("timeseriesbufferproducer_publish3", self._pointer, timestamp)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbufferproducer_get_defaulttags")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_DefaultTags(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Dictionary<string, string>
        """
        result = InteropUtils.invoke("timeseriesbufferproducer_get_defaulttags", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbufferproducer_set_defaulttags")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_DefaultTags(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, string>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("timeseriesbufferproducer_set_defaulttags", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbufferproducer_flush")
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
        InteropUtils.invoke("timeseriesbufferproducer_flush", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbufferproducer_dispose")
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
        InteropUtils.invoke("timeseriesbufferproducer_dispose", self._pointer)
