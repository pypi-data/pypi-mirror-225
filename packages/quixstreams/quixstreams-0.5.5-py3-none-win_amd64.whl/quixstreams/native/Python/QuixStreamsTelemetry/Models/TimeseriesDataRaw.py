# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...InteropHelpers.InteropUtils import InteropUtils


class TimeseriesDataRaw(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TimeseriesDataRaw
        
        Returns
        ----------
        
        TimeseriesDataRaw:
            Instance wrapping the .net type TimeseriesDataRaw
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = TimeseriesDataRaw._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(TimeseriesDataRaw, cls).__new__(cls)
            TimeseriesDataRaw._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TimeseriesDataRaw
        
        Returns
        ----------
        
        TimeseriesDataRaw:
            Instance wrapping the .net type TimeseriesDataRaw
        """
        if '_TimeseriesDataRaw_pointer' in dir(self):
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
        del TimeseriesDataRaw._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("timeseriesdataraw_constructor")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataRaw
        """
        result = InteropUtils.invoke("timeseriesdataraw_constructor")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataraw_constructor2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [ctypes.c_longlong, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Constructor2(epoch: int, timestamps: c_void_p, numericValues: c_void_p, stringValues: c_void_p, binaryValues: c_void_p, tagValues: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        epoch: int
            Underlying .Net type is long
        
        timestamps: c_void_p
            GC Handle Pointer to .Net type long[]
        
        numericValues: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, double?[]>
        
        stringValues: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, string[]>
        
        binaryValues: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, byte[][]>
        
        tagValues: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, string[]>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataRaw
        """
        epoch_long = ctypes.c_longlong(epoch)
        
        result = InteropUtils.invoke("timeseriesdataraw_constructor2", epoch_long, timestamps, numericValues, stringValues, binaryValues, tagValues)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataraw_tojson")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def ToJson(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("timeseriesdataraw_tojson", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataraw_get_epoch")
    _interop_func.restype = ctypes.c_longlong
    _interop_func.argtypes = [c_void_p]
    def get_Epoch(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("timeseriesdataraw_get_epoch", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataraw_set_epoch")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, ctypes.c_longlong]
    def set_Epoch(self, value: int) -> None:
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
        
        InteropUtils.invoke("timeseriesdataraw_set_epoch", self._pointer, value_long)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataraw_get_timestamps")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Timestamps(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type long[]
        """
        result = InteropUtils.invoke("timeseriesdataraw_get_timestamps", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataraw_set_timestamps")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_Timestamps(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type long[]
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("timeseriesdataraw_set_timestamps", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataraw_get_numericvalues")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_NumericValues(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Dictionary<string, double?[]>
        """
        result = InteropUtils.invoke("timeseriesdataraw_get_numericvalues", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataraw_set_numericvalues")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_NumericValues(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, double?[]>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("timeseriesdataraw_set_numericvalues", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataraw_get_stringvalues")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_StringValues(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Dictionary<string, string[]>
        """
        result = InteropUtils.invoke("timeseriesdataraw_get_stringvalues", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataraw_set_stringvalues")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_StringValues(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, string[]>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("timeseriesdataraw_set_stringvalues", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataraw_get_binaryvalues")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_BinaryValues(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Dictionary<string, byte[][]>
        """
        result = InteropUtils.invoke("timeseriesdataraw_get_binaryvalues", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataraw_set_binaryvalues")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_BinaryValues(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, byte[][]>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("timeseriesdataraw_set_binaryvalues", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataraw_get_tagvalues")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_TagValues(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Dictionary<string, string[]>
        """
        result = InteropUtils.invoke("timeseriesdataraw_get_tagvalues", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataraw_set_tagvalues")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_TagValues(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, string[]>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("timeseriesdataraw_set_tagvalues", self._pointer, value)
