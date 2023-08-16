# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .ParameterValueType import ParameterValueType
from ...InteropHelpers.InteropUtils import InteropUtils


class TimeseriesDataParameter(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TimeseriesDataParameter
        
        Returns
        ----------
        
        TimeseriesDataParameter:
            Instance wrapping the .net type TimeseriesDataParameter
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = TimeseriesDataParameter._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(TimeseriesDataParameter, cls).__new__(cls)
            TimeseriesDataParameter._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TimeseriesDataParameter
        
        Returns
        ----------
        
        TimeseriesDataParameter:
            Instance wrapping the .net type TimeseriesDataParameter
        """
        if '_TimeseriesDataParameter_pointer' in dir(self):
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
        del TimeseriesDataParameter._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("timeseriesdataparameter_constructor")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor(parameterId: str) -> c_void_p:
        """
        Parameters
        ----------
        
        parameterId: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataParameter
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        
        result = InteropUtils.invoke("timeseriesdataparameter_constructor", parameterId_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataparameter_constructor2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Constructor2(parameterId: str, numericValues: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        parameterId: str
            Underlying .Net type is string
        
        numericValues: c_void_p
            GC Handle Pointer to .Net type double?[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataParameter
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        
        result = InteropUtils.invoke("timeseriesdataparameter_constructor2", parameterId_ptr, numericValues)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataparameter_constructor3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Constructor3(parameterId: str, stringValues: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        parameterId: str
            Underlying .Net type is string
        
        stringValues: c_void_p
            GC Handle Pointer to .Net type string[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataParameter
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        
        result = InteropUtils.invoke("timeseriesdataparameter_constructor3", parameterId_ptr, stringValues)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataparameter_constructor4")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Constructor4(parameterId: str, binaryValues: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        parameterId: str
            Underlying .Net type is string
        
        binaryValues: c_void_p
            GC Handle Pointer to .Net type byte[][]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeseriesDataParameter
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        
        result = InteropUtils.invoke("timeseriesdataparameter_constructor4", parameterId_ptr, binaryValues)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataparameter_equals")
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
        result = InteropUtils.invoke("timeseriesdataparameter_equals", self._pointer, obj)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataparameter_gethashcode")
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
        result = InteropUtils.invoke("timeseriesdataparameter_gethashcode", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataparameter_get_valuetype")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_ValueType(self) -> ParameterValueType:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        ParameterValueType:
            Underlying .Net type is ParameterValueType
        """
        result = InteropUtils.invoke("timeseriesdataparameter_get_valuetype", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataparameter_get_parameterid")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_ParameterId(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("timeseriesdataparameter_get_parameterid", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataparameter_get_numericvalues")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_NumericValues(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type double?[]
        """
        result = InteropUtils.invoke("timeseriesdataparameter_get_numericvalues", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataparameter_get_stringvalues")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_StringValues(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type string[]
        """
        result = InteropUtils.invoke("timeseriesdataparameter_get_stringvalues", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesdataparameter_get_binaryvalues")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_BinaryValues(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type byte[][]
        """
        result = InteropUtils.invoke("timeseriesdataparameter_get_binaryvalues", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
