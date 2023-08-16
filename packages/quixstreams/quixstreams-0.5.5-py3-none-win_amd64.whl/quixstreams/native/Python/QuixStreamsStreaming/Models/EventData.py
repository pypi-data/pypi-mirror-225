# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...SystemPrivateCoreLib.System.DateTime import DateTime
from ...SystemPrivateCoreLib.System.TimeSpan import TimeSpan
from ...InteropHelpers.InteropUtils import InteropUtils


class EventData(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type EventData
        
        Returns
        ----------
        
        EventData:
            Instance wrapping the .net type EventData
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = EventData._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(EventData, cls).__new__(cls)
            EventData._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type EventData
        
        Returns
        ----------
        
        EventData:
            Instance wrapping the .net type EventData
        """
        if '_EventData_pointer' in dir(self):
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
        del EventData._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("eventdata_constructor")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor(eventId: str, timestampNanoseconds: int, eventValue: str) -> c_void_p:
        """
        Parameters
        ----------
        
        eventId: str
            Underlying .Net type is string
        
        timestampNanoseconds: int
            Underlying .Net type is long
        
        eventValue: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventData
        """
        eventId_ptr = InteropUtils.utf8_to_ptr(eventId)
        timestampNanoseconds_long = ctypes.c_longlong(timestampNanoseconds)
        eventValue_ptr = InteropUtils.utf8_to_ptr(eventValue)
        
        result = InteropUtils.invoke("eventdata_constructor", eventId_ptr, timestampNanoseconds_long, eventValue_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdata_constructor2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Constructor2(eventId: str, timestamp: c_void_p, eventValue: str) -> c_void_p:
        """
        Parameters
        ----------
        
        eventId: str
            Underlying .Net type is string
        
        timestamp: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        eventValue: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventData
        """
        eventId_ptr = InteropUtils.utf8_to_ptr(eventId)
        eventValue_ptr = InteropUtils.utf8_to_ptr(eventValue)
        
        result = InteropUtils.invoke("eventdata_constructor2", eventId_ptr, timestamp, eventValue_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdata_constructor3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Constructor3(eventId: str, timestamp: c_void_p, eventValue: str) -> c_void_p:
        """
        Parameters
        ----------
        
        eventId: str
            Underlying .Net type is string
        
        timestamp: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        eventValue: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventData
        """
        eventId_ptr = InteropUtils.utf8_to_ptr(eventId)
        eventValue_ptr = InteropUtils.utf8_to_ptr(eventValue)
        
        result = InteropUtils.invoke("eventdata_constructor3", eventId_ptr, timestamp, eventValue_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdata_clone")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def Clone(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventData
        """
        result = InteropUtils.invoke("eventdata_clone", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdata_get_id")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Id(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("eventdata_get_id", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdata_set_id")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_Id(self, value: str) -> None:
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
        
        InteropUtils.invoke("eventdata_set_id", self._pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdata_get_value")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Value(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("eventdata_get_value", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdata_set_value")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_Value(self, value: str) -> None:
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
        
        InteropUtils.invoke("eventdata_set_value", self._pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdata_get_tags")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Tags(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IDictionary<string, string>
        """
        result = InteropUtils.invoke("eventdata_get_tags", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdata_addtag")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def AddTag(self, tagId: str, tagValue: str) -> c_void_p:
        """
        Parameters
        ----------
        
        tagId: str
            Underlying .Net type is string
        
        tagValue: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventData
        """
        tagId_ptr = InteropUtils.utf8_to_ptr(tagId)
        tagValue_ptr = InteropUtils.utf8_to_ptr(tagValue)
        
        result = InteropUtils.invoke("eventdata_addtag", self._pointer, tagId_ptr, tagValue_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdata_addtags")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def AddTags(self, tags: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        tags: c_void_p
            GC Handle Pointer to .Net type IEnumerable<KeyValuePair<string, string>>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventData
        """
        result = InteropUtils.invoke("eventdata_addtags", self._pointer, tags)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdata_removetag")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def RemoveTag(self, tagId: str) -> c_void_p:
        """
        Parameters
        ----------
        
        tagId: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type EventData
        """
        tagId_ptr = InteropUtils.utf8_to_ptr(tagId)
        
        result = InteropUtils.invoke("eventdata_removetag", self._pointer, tagId_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdata_get_timestampnanoseconds")
    _interop_func.restype = ctypes.c_longlong
    _interop_func.argtypes = [c_void_p]
    def get_TimestampNanoseconds(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("eventdata_get_timestampnanoseconds", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdata_get_timestampmilliseconds")
    _interop_func.restype = ctypes.c_longlong
    _interop_func.argtypes = [c_void_p]
    def get_TimestampMilliseconds(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("eventdata_get_timestampmilliseconds", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdata_get_timestamp")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Timestamp(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("eventdata_get_timestamp", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("eventdata_get_timestampastimespan")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_TimestampAsTimeSpan(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("eventdata_get_timestampastimespan", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
