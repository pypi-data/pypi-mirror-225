# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ..Utils.TimeseriesDataTimestamps import TimeseriesDataTimestamps
from .TimeseriesDataTimestamp import TimeseriesDataTimestamp
from ...InteropHelpers.InteropUtils import InteropUtils


class TimeseriesData(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TimeseriesData
        
        Returns
        ----------
        
        TimeseriesData:
            Instance wrapping the .net type TimeseriesData
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = TimeseriesData._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(TimeseriesData, cls).__new__(cls)
            TimeseriesData._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TimeseriesData
        
        Returns
        ----------
        
        TimeseriesData:
            Instance wrapping the .net type TimeseriesData
        """
        if '_TimeseriesData_pointer' in dir(self):
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
        del TimeseriesData._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("timeseriesdata_constructor")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor(capacity: int = None) -> c_void_p:
        """
        Parameters
        ----------
        
        capacity: int
            (Optional) Underlying .Net type is int. Defaults to 10
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesData
        """
        result = InteropUtils.invoke("timeseriesdata_constructor", capacity)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdata_constructor2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_ubyte, ctypes.c_ubyte]
    @staticmethod
    def Constructor2(rawData: c_void_p, parametersFilter: c_void_p = None, merge: bool = True, clean: bool = True) -> c_void_p:
        """
        Parameters
        ----------
        
        rawData: c_void_p
            GC Handle Pointer to .Net type TimeseriesDataRaw
        
        parametersFilter: c_void_p
            (Optional) GC Handle Pointer to .Net type string[]. Defaults to None
        
        merge: bool
            (Optional) Underlying .Net type is Boolean. Defaults to True
        
        clean: bool
            (Optional) Underlying .Net type is Boolean. Defaults to True
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesData
        """
        merge_bool = 1 if merge else 0
        clean_bool = 1 if clean else 0
        
        result = InteropUtils.invoke("timeseriesdata_constructor2", rawData, parametersFilter, merge_bool, clean_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdata_constructor3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_ubyte, ctypes.c_ubyte]
    @staticmethod
    def Constructor3(timestamps: c_void_p, merge: bool = True, clean: bool = True) -> c_void_p:
        """
        Parameters
        ----------
        
        timestamps: c_void_p
            GC Handle Pointer to .Net type List<TimeseriesDataTimestamp>
        
        merge: bool
            (Optional) Underlying .Net type is Boolean. Defaults to True
        
        clean: bool
            (Optional) Underlying .Net type is Boolean. Defaults to True
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesData
        """
        merge_bool = 1 if merge else 0
        clean_bool = 1 if clean else 0
        
        result = InteropUtils.invoke("timeseriesdata_constructor3", timestamps, merge_bool, clean_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdata_clone")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Clone(self, parametersFilter: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        parametersFilter: c_void_p
            GC Handle Pointer to .Net type string[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesData
        """
        result = InteropUtils.invoke("timeseriesdata_clone", self._pointer, parametersFilter)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdata_get_timestamps")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Timestamps(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataTimestamps
        """
        result = InteropUtils.invoke("timeseriesdata_get_timestamps", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdata_addtimestamp")
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
            GC Handle Pointer to .Net type TimeseriesDataTimestamp
        """
        result = InteropUtils.invoke("timeseriesdata_addtimestamp", self._pointer, dateTime)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdata_addtimestamp2")
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
            GC Handle Pointer to .Net type TimeseriesDataTimestamp
        """
        result = InteropUtils.invoke("timeseriesdata_addtimestamp2", self._pointer, timeSpan)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdata_addtimestampmilliseconds")
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
            GC Handle Pointer to .Net type TimeseriesDataTimestamp
        """
        timeMilliseconds_long = ctypes.c_longlong(timeMilliseconds)
        
        result = InteropUtils.invoke("timeseriesdata_addtimestampmilliseconds", self._pointer, timeMilliseconds_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdata_addtimestampnanoseconds")
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
            GC Handle Pointer to .Net type TimeseriesDataTimestamp
        """
        timeNanoseconds_long = ctypes.c_longlong(timeNanoseconds)
        
        result = InteropUtils.invoke("timeseriesdata_addtimestampnanoseconds", self._pointer, timeNanoseconds_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdata_equals")
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
        result = InteropUtils.invoke("timeseriesdata_equals", self._pointer, obj)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdata_gethashcode")
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
        result = InteropUtils.invoke("timeseriesdata_gethashcode", self._pointer)
        return result
