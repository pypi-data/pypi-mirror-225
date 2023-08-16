# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .Models.ParameterValue import ParameterValue
from ..InteropHelpers.InteropUtils import InteropUtils


class TimeseriesDataTimestampValues(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TimeseriesDataTimestampValues
        
        Returns
        ----------
        
        TimeseriesDataTimestampValues:
            Instance wrapping the .net type TimeseriesDataTimestampValues
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = TimeseriesDataTimestampValues._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(TimeseriesDataTimestampValues, cls).__new__(cls)
            TimeseriesDataTimestampValues._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TimeseriesDataTimestampValues
        
        Returns
        ----------
        
        TimeseriesDataTimestampValues:
            Instance wrapping the .net type TimeseriesDataTimestampValues
        """
        if '_TimeseriesDataTimestampValues_pointer' in dir(self):
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
        del TimeseriesDataTimestampValues._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("timeseriesdatatimestampvalues_get_values")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Values(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IEnumerable<ParameterValue>
        """
        result = InteropUtils.invoke("timeseriesdatatimestampvalues_get_values", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestampvalues_containskey")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def ContainsKey(self, key: str) -> bool:
        """
        Parameters
        ----------
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("timeseriesdatatimestampvalues_containskey", self._pointer, key_ptr)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestampvalues_trygetvalue")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def TryGetValue(self, key: str, value: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        key: str
            Underlying .Net type is string
        
        value: c_void_p
            GC Handle Pointer to .Net type ParameterValue&
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("timeseriesdatatimestampvalues_trygetvalue", self._pointer, key_ptr, value)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestampvalues_get_count")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Count(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timeseriesdatatimestampvalues_get_count", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestampvalues_get_keys")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Keys(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IEnumerable<string>
        """
        result = InteropUtils.invoke("timeseriesdatatimestampvalues_get_keys", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestampvalues_get_item")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def get_Item(self, key: str) -> c_void_p:
        """
        Parameters
        ----------
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterValue
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("timeseriesdatatimestampvalues_get_item", self._pointer, key_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestampvalues_equals")
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
        result = InteropUtils.invoke("timeseriesdatatimestampvalues_equals", self._pointer, obj)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestampvalues_gethashcode")
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
        result = InteropUtils.invoke("timeseriesdatatimestampvalues_gethashcode", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdatatimestampvalues_tostring")
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
        result = InteropUtils.invoke("timeseriesdatatimestampvalues_tostring", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
