# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...SystemPrivateCoreLib.System.Threading.Tasks.Task import Task
from ..StateValue import StateValue
from ...InteropHelpers.InteropUtils import InteropUtils


class StorageExtensions(object):
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_set")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_longlong]
    @staticmethod
    def Set(stateStorage: c_void_p, key: str, value: int) -> None:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        value: int
            Underlying .Net type is long
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        value_long = ctypes.c_longlong(value)
        
        InteropUtils.invoke("storageextensions_set", stateStorage, key_ptr, value_long)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_setasync")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_longlong]
    @staticmethod
    def SetAsync(stateStorage: c_void_p, key: str, value: int) -> c_void_p:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        value: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        value_long = ctypes.c_longlong(value)
        
        result = InteropUtils.invoke("storageextensions_setasync", stateStorage, key_ptr, value_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_set2")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_double]
    @staticmethod
    def Set2(stateStorage: c_void_p, key: str, value: float) -> None:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        InteropUtils.invoke("storageextensions_set2", stateStorage, key_ptr, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_setasync2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_double]
    @staticmethod
    def SetAsync2(stateStorage: c_void_p, key: str, value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("storageextensions_setasync2", stateStorage, key_ptr, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_set3")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Set3(stateStorage: c_void_p, key: str, value: str) -> None:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        value: str
            Underlying .Net type is string
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        InteropUtils.invoke("storageextensions_set3", stateStorage, key_ptr, value_ptr)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_setasync3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def SetAsync3(stateStorage: c_void_p, key: str, value: str) -> c_void_p:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        value: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        result = InteropUtils.invoke("storageextensions_setasync3", stateStorage, key_ptr, value_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_set4")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Set4(stateStorage: c_void_p, key: str, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        value: c_void_p
            GC Handle Pointer to .Net type byte[]
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        InteropUtils.invoke("storageextensions_set4", stateStorage, key_ptr, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_setasync4")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def SetAsync4(stateStorage: c_void_p, key: str, value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        value: c_void_p
            GC Handle Pointer to .Net type byte[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("storageextensions_setasync4", stateStorage, key_ptr, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_set5")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_ubyte]
    @staticmethod
    def Set5(stateStorage: c_void_p, key: str, value: bool) -> None:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        value: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        value_bool = 1 if value else 0
        
        InteropUtils.invoke("storageextensions_set5", stateStorage, key_ptr, value_bool)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_setasync5")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_ubyte]
    @staticmethod
    def SetAsync5(stateStorage: c_void_p, key: str, value: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        value: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        value_bool = 1 if value else 0
        
        result = InteropUtils.invoke("storageextensions_setasync5", stateStorage, key_ptr, value_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_set6")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Set6(stateStorage: c_void_p, key: str, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        value: c_void_p
            GC Handle Pointer to .Net type StateValue
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        InteropUtils.invoke("storageextensions_set6", stateStorage, key_ptr, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_setasync6")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def SetAsync6(stateStorage: c_void_p, key: str, value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        value: c_void_p
            GC Handle Pointer to .Net type StateValue
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("storageextensions_setasync6", stateStorage, key_ptr, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_get")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Get(stateStorage: c_void_p, key: str) -> c_void_p:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StateValue
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("storageextensions_get", stateStorage, key_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_getasync")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def GetAsync(stateStorage: c_void_p, key: str) -> c_void_p:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<StateValue>
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("storageextensions_getasync", stateStorage, key_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_getdouble")
    _interop_func.restype = ctypes.c_double
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def GetDouble(stateStorage: c_void_p, key: str) -> float:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("storageextensions_getdouble", stateStorage, key_ptr)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_getdoubleasync")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def GetDoubleAsync(stateStorage: c_void_p, key: str) -> c_void_p:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<double>
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("storageextensions_getdoubleasync", stateStorage, key_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_getstring")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def GetString(stateStorage: c_void_p, key: str) -> str:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("storageextensions_getstring", stateStorage, key_ptr)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_getstringasync")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def GetStringAsync(stateStorage: c_void_p, key: str) -> c_void_p:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<string>
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("storageextensions_getstringasync", stateStorage, key_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_getbool")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def GetBool(stateStorage: c_void_p, key: str) -> bool:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("storageextensions_getbool", stateStorage, key_ptr)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_getboolasync")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def GetBoolAsync(stateStorage: c_void_p, key: str) -> c_void_p:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<Boolean>
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("storageextensions_getboolasync", stateStorage, key_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_getlong")
    _interop_func.restype = ctypes.c_longlong
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def GetLong(stateStorage: c_void_p, key: str) -> int:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("storageextensions_getlong", stateStorage, key_ptr)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_getlongasync")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def GetLongAsync(stateStorage: c_void_p, key: str) -> c_void_p:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<long>
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("storageextensions_getlongasync", stateStorage, key_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_getbinary")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def GetBinary(stateStorage: c_void_p, key: str) -> c_void_p:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type byte[]
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("storageextensions_getbinary", stateStorage, key_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_getbinaryasync")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def GetBinaryAsync(stateStorage: c_void_p, key: str) -> c_void_p:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<byte[]>
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("storageextensions_getbinaryasync", stateStorage, key_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_remove")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Remove(stateStorage: c_void_p, key: str) -> None:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        InteropUtils.invoke("storageextensions_remove", stateStorage, key_ptr)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_containskey")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def ContainsKey(stateStorage: c_void_p, key: str) -> bool:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("storageextensions_containskey", stateStorage, key_ptr)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_getallkeys")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def GetAllKeys(stateStorage: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type string[]
        """
        result = InteropUtils.invoke("storageextensions_getallkeys", stateStorage)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("storageextensions_clear")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def Clear(stateStorage: c_void_p) -> None:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("storageextensions_clear", stateStorage)
