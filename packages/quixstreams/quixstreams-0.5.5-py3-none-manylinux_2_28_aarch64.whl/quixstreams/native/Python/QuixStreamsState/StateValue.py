# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .StateValue_StateType import StateType
from ..InteropHelpers.InteropUtils import InteropUtils


class StateValue(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StateValue
        
        Returns
        ----------
        
        StateValue:
            Instance wrapping the .net type StateValue
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = StateValue._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(StateValue, cls).__new__(cls)
            StateValue._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StateValue
        
        Returns
        ----------
        
        StateValue:
            Instance wrapping the .net type StateValue
        """
        if '_StateValue_pointer' in dir(self):
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
        del StateValue._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("statevalue_constructor")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor(value: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        value: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StateValue
        """
        value_bool = 1 if value else 0
        
        result = InteropUtils.invoke("statevalue_constructor", value_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("statevalue_constructor2")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor2(value: int) -> c_void_p:
        """
        Parameters
        ----------
        
        value: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StateValue
        """
        value_long = ctypes.c_longlong(value)
        
        result = InteropUtils.invoke("statevalue_constructor2", value_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("statevalue_constructor3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def Constructor3(value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type byte[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StateValue
        """
        result = InteropUtils.invoke("statevalue_constructor3", value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("statevalue_constructor4")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_int]
    @staticmethod
    def Constructor4(value: c_void_p, type: StateType) -> c_void_p:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type byte[]
        
        type: StateType
            Underlying .Net type is StateValue.StateType
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StateValue
        """
        result = InteropUtils.invoke("statevalue_constructor4", value, type.value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("statevalue_constructor5")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor5(value: str) -> c_void_p:
        """
        Parameters
        ----------
        
        value: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StateValue
        """
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        result = InteropUtils.invoke("statevalue_constructor5", value_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("statevalue_constructor6")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [ctypes.c_double]
    @staticmethod
    def Constructor6(value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StateValue
        """
        result = InteropUtils.invoke("statevalue_constructor6", value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("statevalue_get_type")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Type(self) -> StateType:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        StateType:
            Underlying .Net type is StateValue.StateType
        """
        result = InteropUtils.invoke("statevalue_get_type", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("statevalue_get_doublevalue")
    _interop_func.restype = ctypes.c_double
    _interop_func.argtypes = [c_void_p]
    def get_DoubleValue(self) -> float:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("statevalue_get_doublevalue", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("statevalue_get_longvalue")
    _interop_func.restype = ctypes.c_longlong
    _interop_func.argtypes = [c_void_p]
    def get_LongValue(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("statevalue_get_longvalue", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("statevalue_get_stringvalue")
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
        result = InteropUtils.invoke("statevalue_get_stringvalue", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("statevalue_get_boolvalue")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_BoolValue(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("statevalue_get_boolvalue", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("statevalue_get_binaryvalue")
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
        result = InteropUtils.invoke("statevalue_get_binaryvalue", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("statevalue_isnull")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def IsNull(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("statevalue_isnull", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("statevalue_gethashcode")
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
        result = InteropUtils.invoke("statevalue_gethashcode", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("statevalue_equals")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Equals(self, other: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        other: c_void_p
            GC Handle Pointer to .Net type StateValue
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("statevalue_equals", self._pointer, other)
        return result
