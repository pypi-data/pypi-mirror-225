# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ....SystemPrivateCoreLib.System.DateTime import DateTime
from .EventDataBuilder import EventDataBuilder
from .EventDefinitionBuilder import EventDefinitionBuilder
from ....InteropHelpers.InteropUtils import InteropUtils


class StreamEventsProducer(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamEventsProducer
        
        Returns
        ----------
        
        StreamEventsProducer:
            Instance wrapping the .net type StreamEventsProducer
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = StreamEventsProducer._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(StreamEventsProducer, cls).__new__(cls)
            StreamEventsProducer._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamEventsProducer
        
        Returns
        ----------
        
        StreamEventsProducer:
            Instance wrapping the .net type StreamEventsProducer
        """
        if '_StreamEventsProducer_pointer' in dir(self):
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
        del StreamEventsProducer._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("streameventsproducer_get_defaulttags")
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
        result = InteropUtils.invoke("streameventsproducer_get_defaulttags", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streameventsproducer_set_defaulttags")
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
        InteropUtils.invoke("streameventsproducer_set_defaulttags", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streameventsproducer_get_defaultlocation")
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
        result = InteropUtils.invoke("streameventsproducer_get_defaultlocation", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streameventsproducer_set_defaultlocation")
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
        
        InteropUtils.invoke("streameventsproducer_set_defaultlocation", self._pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streameventsproducer_get_epoch")
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
        result = InteropUtils.invoke("streameventsproducer_get_epoch", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streameventsproducer_set_epoch")
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
        InteropUtils.invoke("streameventsproducer_set_epoch", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streameventsproducer_addtimestamp")
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
            GC Handle Pointer to .Net type EventDataBuilder
        """
        result = InteropUtils.invoke("streameventsproducer_addtimestamp", self._pointer, dateTime)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streameventsproducer_addtimestamp2")
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
            GC Handle Pointer to .Net type EventDataBuilder
        """
        result = InteropUtils.invoke("streameventsproducer_addtimestamp2", self._pointer, timeSpan)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streameventsproducer_addtimestampmilliseconds")
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
            GC Handle Pointer to .Net type EventDataBuilder
        """
        timeMilliseconds_long = ctypes.c_longlong(timeMilliseconds)
        
        result = InteropUtils.invoke("streameventsproducer_addtimestampmilliseconds", self._pointer, timeMilliseconds_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streameventsproducer_addtimestampnanoseconds")
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
            GC Handle Pointer to .Net type EventDataBuilder
        """
        timeNanoseconds_long = ctypes.c_longlong(timeNanoseconds)
        
        result = InteropUtils.invoke("streameventsproducer_addtimestampnanoseconds", self._pointer, timeNanoseconds_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streameventsproducer_adddefinitions")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def AddDefinitions(self, definitions: c_void_p) -> None:
        """
        Parameters
        ----------
        
        definitions: c_void_p
            GC Handle Pointer to .Net type List<EventDefinition>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streameventsproducer_adddefinitions", self._pointer, definitions)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streameventsproducer_adddefinition")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
    def AddDefinition(self, eventId: str, name: str = None, description: str = None) -> c_void_p:
        """
        Parameters
        ----------
        
        eventId: str
            Underlying .Net type is string
        
        name: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        description: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventDefinitionBuilder
        """
        eventId_ptr = InteropUtils.utf8_to_ptr(eventId)
        name_ptr = InteropUtils.utf8_to_ptr(name)
        description_ptr = InteropUtils.utf8_to_ptr(description)
        
        result = InteropUtils.invoke("streameventsproducer_adddefinition", self._pointer, eventId_ptr, name_ptr, description_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streameventsproducer_addlocation")
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
            GC Handle Pointer to .Net type EventDefinitionBuilder
        """
        location_ptr = InteropUtils.utf8_to_ptr(location)
        
        result = InteropUtils.invoke("streameventsproducer_addlocation", self._pointer, location_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streameventsproducer_flush")
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
        InteropUtils.invoke("streameventsproducer_flush", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streameventsproducer_publish")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Publish(self, data: c_void_p) -> None:
        """
        Parameters
        ----------
        
        data: c_void_p
            GC Handle Pointer to .Net type EventData
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streameventsproducer_publish", self._pointer, data)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streameventsproducer_publish2")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Publish2(self, events: c_void_p) -> None:
        """
        Parameters
        ----------
        
        events: c_void_p
            GC Handle Pointer to .Net type ICollection<EventData>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streameventsproducer_publish2", self._pointer, events)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streameventsproducer_dispose")
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
        InteropUtils.invoke("streameventsproducer_dispose", self._pointer)
