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


class ParameterValue(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterValue
        
        Returns
        ----------
        
        ParameterValue:
            Instance wrapping the .net type ParameterValue
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = ParameterValue._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(ParameterValue, cls).__new__(cls)
            ParameterValue._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterValue
        
        Returns
        ----------
        
        ParameterValue:
            Instance wrapping the .net type ParameterValue
        """
        if '_ParameterValue_pointer' in dir(self):
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
        del ParameterValue._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("parametervalue_constructor")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [ctypes.c_longlong, c_void_p]
    @staticmethod
    def Constructor(timestampRawIndex: int, timeseriesDataParameter: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        timestampRawIndex: int
            Underlying .Net type is long
        
        timeseriesDataParameter: c_void_p
            GC Handle Pointer to .Net type TimeseriesDataParameter
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterValue
        """
        timestampRawIndex_long = ctypes.c_longlong(timestampRawIndex)
        
        result = InteropUtils.invoke("parametervalue_constructor", timestampRawIndex_long, timeseriesDataParameter)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parametervalue_get_parameterid")
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
        result = InteropUtils.invoke("parametervalue_get_parameterid", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parametervalue_get_numericvalue")
    _interop_func.restype = InteropUtils.create_nullable(ctypes.c_double)
    _interop_func.argtypes = [c_void_p]
    def get_NumericValue(self) -> Optional[float]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[float]:
            Underlying .Net type is double?
        """
        result = InteropUtils.invoke("parametervalue_get_numericvalue", self._pointer)
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parametervalue_set_numericvalue")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, InteropUtils.create_nullable(ctypes.c_double)]
    def set_NumericValue(self, value: Optional[float]) -> None:
        """
        Parameters
        ----------
        
        value: Optional[float]
            Underlying .Net type is double?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_nullable = InteropUtils.create_nullable(ctypes.c_double)(value)
        
        InteropUtils.invoke("parametervalue_set_numericvalue", self._pointer, value_nullable)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parametervalue_get_stringvalue")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_StringValue(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("parametervalue_get_stringvalue", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parametervalue_set_stringvalue")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_StringValue(self, value: str) -> None:
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
        
        InteropUtils.invoke("parametervalue_set_stringvalue", self._pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parametervalue_get_binaryvalue")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_BinaryValue(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type byte[]
        """
        result = InteropUtils.invoke("parametervalue_get_binaryvalue", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parametervalue_set_binaryvalue")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_BinaryValue(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type byte[]
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("parametervalue_set_binaryvalue", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parametervalue_get_value")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Value(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Object
        """
        result = InteropUtils.invoke("parametervalue_get_value", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parametervalue_op_equality")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Equality(lhs: c_void_p, rhs: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        lhs: c_void_p
            GC Handle Pointer to .Net type ParameterValue
        
        rhs: c_void_p
            GC Handle Pointer to .Net type ParameterValue
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("parametervalue_op_equality", lhs, rhs)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parametervalue_op_inequality")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Inequality(lhs: c_void_p, rhs: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        lhs: c_void_p
            GC Handle Pointer to .Net type ParameterValue
        
        rhs: c_void_p
            GC Handle Pointer to .Net type ParameterValue
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("parametervalue_op_inequality", lhs, rhs)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parametervalue_equals")
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
        result = InteropUtils.invoke("parametervalue_equals", self._pointer, obj)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parametervalue_gethashcode")
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
        result = InteropUtils.invoke("parametervalue_gethashcode", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parametervalue_tostring")
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
        result = InteropUtils.invoke("parametervalue_tostring", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parametervalue_get_type")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Type(self) -> ParameterValueType:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        ParameterValueType:
            Underlying .Net type is ParameterValueType
        """
        result = InteropUtils.invoke("parametervalue_get_type", self._pointer)
        return result
