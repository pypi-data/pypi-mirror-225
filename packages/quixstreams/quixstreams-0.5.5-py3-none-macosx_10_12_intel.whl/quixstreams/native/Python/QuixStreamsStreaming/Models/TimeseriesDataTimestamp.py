# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ..TimeseriesDataTimestampValues import TimeseriesDataTimestampValues
from ..Utils.TimeseriesDataTimestampTags import TimeseriesDataTimestampTags
from ...SystemPrivateCoreLib.System.DateTime import DateTime
from ...SystemPrivateCoreLib.System.TimeSpan import TimeSpan
from ...InteropHelpers.InteropUtils import InteropUtils


class TimeseriesDataTimestamp(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TimeseriesDataTimestamp
        
        Returns
        ----------
        
        TimeseriesDataTimestamp:
            Instance wrapping the .net type TimeseriesDataTimestamp
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = TimeseriesDataTimestamp._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(TimeseriesDataTimestamp, cls).__new__(cls)
            TimeseriesDataTimestamp._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TimeseriesDataTimestamp
        
        Returns
        ----------
        
        TimeseriesDataTimestamp:
            Instance wrapping the .net type TimeseriesDataTimestamp
        """
        if '_TimeseriesDataTimestamp_pointer' in dir(self):
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
        del TimeseriesDataTimestamp._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_get_parameters")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Parameters(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataTimestampValues
        """
        result = InteropUtils.invoke("timeseriesdatatimestamp_get_parameters", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_get_tags")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Tags(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataTimestampTags
        """
        result = InteropUtils.invoke("timeseriesdatatimestamp_get_tags", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_get_timestampnanoseconds")
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
        result = InteropUtils.invoke("timeseriesdatatimestamp_get_timestampnanoseconds", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_set_timestampnanoseconds")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, ctypes.c_longlong]
    def set_TimestampNanoseconds(self, value: int) -> None:
        """
        Parameters
        ----------
        
        value: int
            Underlying .Net type is long
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_long = ctypes.c_longlong(value)
        
        InteropUtils.invoke("timeseriesdatatimestamp_set_timestampnanoseconds", self._pointer, value_long)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_get_timestampmilliseconds")
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
        result = InteropUtils.invoke("timeseriesdatatimestamp_get_timestampmilliseconds", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_get_timestamp")
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
        result = InteropUtils.invoke("timeseriesdatatimestamp_get_timestamp", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_get_timestampastimespan")
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
        result = InteropUtils.invoke("timeseriesdatatimestamp_get_timestampastimespan", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_addvalue")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_double]
    def AddValue(self, parameterId: str, value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        parameterId: str
            Underlying .Net type is string
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataTimestamp
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        
        result = InteropUtils.invoke("timeseriesdatatimestamp_addvalue", self._pointer, parameterId_ptr, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_addvalue2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def AddValue2(self, parameterId: str, value: str) -> c_void_p:
        """
        Parameters
        ----------
        
        parameterId: str
            Underlying .Net type is string
        
        value: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataTimestamp
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        result = InteropUtils.invoke("timeseriesdatatimestamp_addvalue2", self._pointer, parameterId_ptr, value_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_addvalue3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def AddValue3(self, parameterId: str, value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        parameterId: str
            Underlying .Net type is string
        
        value: c_void_p
            GC Handle Pointer to .Net type byte[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataTimestamp
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        
        result = InteropUtils.invoke("timeseriesdatatimestamp_addvalue3", self._pointer, parameterId_ptr, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_addvalue4")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def AddValue4(self, parameterId: str, value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        parameterId: str
            Underlying .Net type is string
        
        value: c_void_p
            GC Handle Pointer to .Net type ParameterValue
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataTimestamp
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        
        result = InteropUtils.invoke("timeseriesdatatimestamp_addvalue4", self._pointer, parameterId_ptr, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_removevalue")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def RemoveValue(self, parameterId: str) -> c_void_p:
        """
        Parameters
        ----------
        
        parameterId: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataTimestamp
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        
        result = InteropUtils.invoke("timeseriesdatatimestamp_removevalue", self._pointer, parameterId_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_addtag")
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
            GC Handle Pointer to .Net type TimeseriesDataTimestamp
        """
        tagId_ptr = InteropUtils.utf8_to_ptr(tagId)
        tagValue_ptr = InteropUtils.utf8_to_ptr(tagValue)
        
        result = InteropUtils.invoke("timeseriesdatatimestamp_addtag", self._pointer, tagId_ptr, tagValue_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_addtags")
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
            GC Handle Pointer to .Net type TimeseriesDataTimestamp
        """
        result = InteropUtils.invoke("timeseriesdatatimestamp_addtags", self._pointer, tags)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_removetag")
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
            GC Handle Pointer to .Net type TimeseriesDataTimestamp
        """
        tagId_ptr = InteropUtils.utf8_to_ptr(tagId)
        
        result = InteropUtils.invoke("timeseriesdatatimestamp_removetag", self._pointer, tagId_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_equals")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Equals(self, obj: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        obj: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("timeseriesdatatimestamp_equals", self._pointer, obj)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_gethashcode")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def GetHashCode(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timeseriesdatatimestamp_gethashcode", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestamp_tostring")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def ToString(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("timeseriesdatatimestamp_tostring", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
