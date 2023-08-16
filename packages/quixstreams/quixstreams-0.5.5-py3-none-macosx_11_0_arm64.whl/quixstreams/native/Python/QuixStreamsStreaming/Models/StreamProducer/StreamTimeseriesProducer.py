# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .TimeseriesBufferProducer import TimeseriesBufferProducer
from .ParameterDefinitionBuilder import ParameterDefinitionBuilder
from ..LeadingEdgeBuffer import LeadingEdgeBuffer
from ....InteropHelpers.InteropUtils import InteropUtils


class StreamTimeseriesProducer(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamTimeseriesProducer
        
        Returns
        ----------
        
        StreamTimeseriesProducer:
            Instance wrapping the .net type StreamTimeseriesProducer
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = StreamTimeseriesProducer._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(StreamTimeseriesProducer, cls).__new__(cls)
            StreamTimeseriesProducer._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamTimeseriesProducer
        
        Returns
        ----------
        
        StreamTimeseriesProducer:
            Instance wrapping the .net type StreamTimeseriesProducer
        """
        if '_StreamTimeseriesProducer_pointer' in dir(self):
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
        del StreamTimeseriesProducer._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("streamtimeseriesproducer_get_buffer")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Buffer(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesBufferProducer
        """
        result = InteropUtils.invoke("streamtimeseriesproducer_get_buffer", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesproducer_publish")
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
        InteropUtils.invoke("streamtimeseriesproducer_publish", self._pointer, data)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesproducer_publish2")
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
        InteropUtils.invoke("streamtimeseriesproducer_publish2", self._pointer, data)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesproducer_publish3")
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
        InteropUtils.invoke("streamtimeseriesproducer_publish3", self._pointer, timestamp)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesproducer_get_defaultlocation")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_DefaultLocation(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("streamtimeseriesproducer_get_defaultlocation", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesproducer_set_defaultlocation")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_DefaultLocation(self, value: str) -> None:
        """
        Parameters
        ----------
        
        value: str
            Underlying .Net type is string
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        InteropUtils.invoke("streamtimeseriesproducer_set_defaultlocation", self._pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesproducer_adddefinitions")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def AddDefinitions(self, definitions: c_void_p) -> None:
        """
        Parameters
        ----------
        
        definitions: c_void_p
            GC Handle Pointer to .Net type List<ParameterDefinition>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streamtimeseriesproducer_adddefinitions", self._pointer, definitions)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesproducer_adddefinition")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
    def AddDefinition(self, parameterId: str, name: str = None, description: str = None) -> c_void_p:
        """
        Parameters
        ----------
        
        parameterId: str
            Underlying .Net type is string
        
        name: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        description: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDefinitionBuilder
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        name_ptr = InteropUtils.utf8_to_ptr(name)
        description_ptr = InteropUtils.utf8_to_ptr(description)
        
        result = InteropUtils.invoke("streamtimeseriesproducer_adddefinition", self._pointer, parameterId_ptr, name_ptr, description_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesproducer_addlocation")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def AddLocation(self, location: str) -> c_void_p:
        """
        Parameters
        ----------
        
        location: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDefinitionBuilder
        """
        location_ptr = InteropUtils.utf8_to_ptr(location)
        
        result = InteropUtils.invoke("streamtimeseriesproducer_addlocation", self._pointer, location_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesproducer_flush")
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
        InteropUtils.invoke("streamtimeseriesproducer_flush", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesproducer_createleadingedgebuffer")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_int]
    def CreateLeadingEdgeBuffer(self, leadingEdgeDelayMs: int) -> c_void_p:
        """
        Parameters
        ----------
        
        leadingEdgeDelayMs: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type LeadingEdgeBuffer
        """
        result = InteropUtils.invoke("streamtimeseriesproducer_createleadingedgebuffer", self._pointer, leadingEdgeDelayMs)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamtimeseriesproducer_dispose")
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
        InteropUtils.invoke("streamtimeseriesproducer_dispose", self._pointer)
