# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ....QuixStreamsTelemetry.Models.EventLevel import EventLevel
from ....InteropHelpers.InteropUtils import InteropUtils


class EventDefinitionBuilder(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type EventDefinitionBuilder
        
        Returns
        ----------
        
        EventDefinitionBuilder:
            Instance wrapping the .net type EventDefinitionBuilder
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = EventDefinitionBuilder._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(EventDefinitionBuilder, cls).__new__(cls)
            EventDefinitionBuilder._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type EventDefinitionBuilder
        
        Returns
        ----------
        
        EventDefinitionBuilder:
            Instance wrapping the .net type EventDefinitionBuilder
        """
        if '_EventDefinitionBuilder_pointer' in dir(self):
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
        del EventDefinitionBuilder._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("eventdefinitionbuilder_constructor")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Constructor(streamEventsProducer: c_void_p, location: str, properties: c_void_p = None) -> c_void_p:
        """
        Parameters
        ----------
        
        streamEventsProducer: c_void_p
            GC Handle Pointer to .Net type StreamEventsProducer
        
        location: str
            Underlying .Net type is string
        
        properties: c_void_p
            (Optional) GC Handle Pointer to .Net type EventDefinition. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventDefinitionBuilder
        """
        location_ptr = InteropUtils.utf8_to_ptr(location)
        
        result = InteropUtils.invoke("eventdefinitionbuilder_constructor", streamEventsProducer, location_ptr, properties)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdefinitionbuilder_setlevel")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_int]
    def SetLevel(self, level: EventLevel) -> c_void_p:
        """
        Parameters
        ----------
        
        level: EventLevel
            Underlying .Net type is EventLevel
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventDefinitionBuilder
        """
        result = InteropUtils.invoke("eventdefinitionbuilder_setlevel", self._pointer, level.value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdefinitionbuilder_setcustomproperties")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def SetCustomProperties(self, customProperties: str) -> c_void_p:
        """
        Parameters
        ----------
        
        customProperties: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventDefinitionBuilder
        """
        customProperties_ptr = InteropUtils.utf8_to_ptr(customProperties)
        
        result = InteropUtils.invoke("eventdefinitionbuilder_setcustomproperties", self._pointer, customProperties_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdefinitionbuilder_adddefinition")
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
        
        result = InteropUtils.invoke("eventdefinitionbuilder_adddefinition", self._pointer, eventId_ptr, name_ptr, description_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
