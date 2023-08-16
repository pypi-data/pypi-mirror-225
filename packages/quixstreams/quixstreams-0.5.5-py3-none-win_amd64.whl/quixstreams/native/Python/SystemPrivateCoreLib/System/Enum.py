# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .Type import Type
from .TypeCode import TypeCode
from ...InteropHelpers.InteropUtils import InteropUtils


class Enum(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type Enum
        
        Returns
        ----------
        
        Enum:
            Instance wrapping the .net type Enum
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = Enum._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(Enum, cls).__new__(cls)
            Enum._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type Enum
        
        Returns
        ----------
        
        Enum:
            Instance wrapping the .net type Enum
        """
        if '_Enum_pointer' in dir(self):
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
        del Enum._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("enum_getname2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def GetName2(enumType: c_void_p, value: c_void_p) -> str:
        """
        Parameters
        ----------
        
        enumType: c_void_p
            GC Handle Pointer to .Net type Type
        
        value: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("enum_getname2", enumType, value)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_getnames")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def GetNames(enumType: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        enumType: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type string[]
        """
        result = InteropUtils.invoke("enum_getnames", enumType)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_getunderlyingtype")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def GetUnderlyingType(enumType: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        enumType: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("enum_getunderlyingtype", enumType)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_getvalues")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def GetValues(enumType: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        enumType: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Array
        """
        result = InteropUtils.invoke("enum_getvalues", enumType)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_getvaluesasunderlyingtype")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def GetValuesAsUnderlyingType(enumType: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        enumType: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Array
        """
        result = InteropUtils.invoke("enum_getvaluesasunderlyingtype", enumType)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_hasflag")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def HasFlag(self, flag: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        flag: c_void_p
            GC Handle Pointer to .Net type Enum
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("enum_hasflag", self._pointer, flag)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_isdefined2")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def IsDefined2(enumType: c_void_p, value: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        enumType: c_void_p
            GC Handle Pointer to .Net type Type
        
        value: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("enum_isdefined2", enumType, value)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_parse")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Parse(enumType: c_void_p, value: str) -> c_void_p:
        """
        Parameters
        ----------
        
        enumType: c_void_p
            GC Handle Pointer to .Net type Type
        
        value: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Object
        """
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        result = InteropUtils.invoke("enum_parse", enumType, value_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_parse3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_ubyte]
    @staticmethod
    def Parse3(enumType: c_void_p, value: str, ignoreCase: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        enumType: c_void_p
            GC Handle Pointer to .Net type Type
        
        value: str
            Underlying .Net type is string
        
        ignoreCase: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Object
        """
        value_ptr = InteropUtils.utf8_to_ptr(value)
        ignoreCase_bool = 1 if ignoreCase else 0
        
        result = InteropUtils.invoke("enum_parse3", enumType, value_ptr, ignoreCase_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_tryparse")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def TryParse(enumType: c_void_p, value: str, result: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        enumType: c_void_p
            GC Handle Pointer to .Net type Type
        
        value: str
            Underlying .Net type is string
        
        result: c_void_p
            GC Handle Pointer to .Net type Object&
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        result2 = InteropUtils.invoke("enum_tryparse", enumType, value_ptr, result)
        return result2
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_tryparse3")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_ubyte, c_void_p]
    @staticmethod
    def TryParse3(enumType: c_void_p, value: str, ignoreCase: bool, result: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        enumType: c_void_p
            GC Handle Pointer to .Net type Type
        
        value: str
            Underlying .Net type is string
        
        ignoreCase: bool
            Underlying .Net type is Boolean
        
        result: c_void_p
            GC Handle Pointer to .Net type Object&
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        value_ptr = InteropUtils.utf8_to_ptr(value)
        ignoreCase_bool = 1 if ignoreCase else 0
        
        result2 = InteropUtils.invoke("enum_tryparse3", enumType, value_ptr, ignoreCase_bool, result)
        return result2
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_equals")
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
        result = InteropUtils.invoke("enum_equals", self._pointer, obj)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_gethashcode")
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
        result = InteropUtils.invoke("enum_gethashcode", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_compareto")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p, c_void_p]
    def CompareTo(self, target: c_void_p) -> int:
        """
        Parameters
        ----------
        
        target: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("enum_compareto", self._pointer, target)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_tostring")
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
        result = InteropUtils.invoke("enum_tostring", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_tostring2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def ToString2(self, format: str) -> str:
        """
        Parameters
        ----------
        
        format: str
            Underlying .Net type is string
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        format_ptr = InteropUtils.utf8_to_ptr(format)
        
        result = InteropUtils.invoke("enum_tostring2", self._pointer, format_ptr)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_tostring3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def ToString3(self, provider: c_void_p) -> str:
        """
        Parameters
        ----------
        
        provider: c_void_p
            GC Handle Pointer to .Net type IFormatProvider
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("enum_tostring3", self._pointer, provider)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_tostring4")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def ToString4(self, format: str, provider: c_void_p) -> str:
        """
        Parameters
        ----------
        
        format: str
            Underlying .Net type is string
        
        provider: c_void_p
            GC Handle Pointer to .Net type IFormatProvider
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        format_ptr = InteropUtils.utf8_to_ptr(format)
        
        result = InteropUtils.invoke("enum_tostring4", self._pointer, format_ptr, provider)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_format")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Format(enumType: c_void_p, value: c_void_p, format: str) -> str:
        """
        Parameters
        ----------
        
        enumType: c_void_p
            GC Handle Pointer to .Net type Type
        
        value: c_void_p
            GC Handle Pointer to .Net type Object
        
        format: str
            Underlying .Net type is string
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        format_ptr = InteropUtils.utf8_to_ptr(format)
        
        result = InteropUtils.invoke("enum_format", enumType, value, format_ptr)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_gettypecode")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def GetTypeCode(self) -> TypeCode:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        TypeCode:
            Underlying .Net type is TypeCode
        """
        result = InteropUtils.invoke("enum_gettypecode", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_toobject")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def ToObject(enumType: c_void_p, value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        enumType: c_void_p
            GC Handle Pointer to .Net type Type
        
        value: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Object
        """
        result = InteropUtils.invoke("enum_toobject", enumType, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_toobject4")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_int]
    @staticmethod
    def ToObject4(enumType: c_void_p, value: int) -> c_void_p:
        """
        Parameters
        ----------
        
        enumType: c_void_p
            GC Handle Pointer to .Net type Type
        
        value: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Object
        """
        result = InteropUtils.invoke("enum_toobject4", enumType, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_toobject5")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_ubyte]
    @staticmethod
    def ToObject5(enumType: c_void_p, value: int) -> c_void_p:
        """
        Parameters
        ----------
        
        enumType: c_void_p
            GC Handle Pointer to .Net type Type
        
        value: int
            Underlying .Net type is byte
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Object
        """
        result = InteropUtils.invoke("enum_toobject5", enumType, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("enum_toobject8")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_longlong]
    @staticmethod
    def ToObject8(enumType: c_void_p, value: int) -> c_void_p:
        """
        Parameters
        ----------
        
        enumType: c_void_p
            GC Handle Pointer to .Net type Type
        
        value: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Object
        """
        value_long = ctypes.c_longlong(value)
        
        result = InteropUtils.invoke("enum_toobject8", enumType, value_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
