# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ....InteropHelpers.InteropUtils import InteropUtils


class EventDataBuilder(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type EventDataBuilder
        
        Returns
        ----------
        
        EventDataBuilder:
            Instance wrapping the .net type EventDataBuilder
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = EventDataBuilder._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(EventDataBuilder, cls).__new__(cls)
            EventDataBuilder._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type EventDataBuilder
        
        Returns
        ----------
        
        EventDataBuilder:
            Instance wrapping the .net type EventDataBuilder
        """
        if '_EventDataBuilder_pointer' in dir(self):
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
        del EventDataBuilder._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("eventdatabuilder_constructor")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_longlong]
    @staticmethod
    def Constructor(streamEventsProducer: c_void_p, timestampNanoseconds: int) -> c_void_p:
        """
        Parameters
        ----------
        
        streamEventsProducer: c_void_p
            GC Handle Pointer to .Net type StreamEventsProducer
        
        timestampNanoseconds: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventDataBuilder
        """
        timestampNanoseconds_long = ctypes.c_longlong(timestampNanoseconds)
        
        result = InteropUtils.invoke("eventdatabuilder_constructor", streamEventsProducer, timestampNanoseconds_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdatabuilder_addvalue")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def AddValue(self, eventId: str, value: str) -> c_void_p:
        """
        Parameters
        ----------
        
        eventId: str
            Underlying .Net type is string
        
        value: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventDataBuilder
        """
        eventId_ptr = InteropUtils.utf8_to_ptr(eventId)
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        result = InteropUtils.invoke("eventdatabuilder_addvalue", self._pointer, eventId_ptr, value_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdatabuilder_addtag")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def AddTag(self, tagId: str, value: str) -> c_void_p:
        """
        Parameters
        ----------
        
        tagId: str
            Underlying .Net type is string
        
        value: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventDataBuilder
        """
        tagId_ptr = InteropUtils.utf8_to_ptr(tagId)
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        result = InteropUtils.invoke("eventdatabuilder_addtag", self._pointer, tagId_ptr, value_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdatabuilder_addtags")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def AddTags(self, tagsValues: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        tagsValues: c_void_p
            GC Handle Pointer to .Net type IEnumerable<KeyValuePair<string, string>>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventDataBuilder
        """
        result = InteropUtils.invoke("eventdatabuilder_addtags", self._pointer, tagsValues)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdatabuilder_publish")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def Publish(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("eventdatabuilder_publish", self._pointer)
