# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...InteropHelpers.InteropUtils import InteropUtils


class RawMessage(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type RawMessage
        
        Returns
        ----------
        
        RawMessage:
            Instance wrapping the .net type RawMessage
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = RawMessage._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(RawMessage, cls).__new__(cls)
            RawMessage._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type RawMessage
        
        Returns
        ----------
        
        RawMessage:
            Instance wrapping the .net type RawMessage
        """
        if '_RawMessage_pointer' in dir(self):
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
        del RawMessage._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("rawmessage_constructor")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Constructor(key: c_void_p, value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        key: c_void_p
            GC Handle Pointer to .Net type byte[]
        
        value: c_void_p
            GC Handle Pointer to .Net type byte[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type RawMessage
        """
        result = InteropUtils.invoke("rawmessage_constructor", key, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("rawmessage_constructor2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def Constructor2(value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type byte[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type RawMessage
        """
        result = InteropUtils.invoke("rawmessage_constructor2", value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("rawmessage_get_metadata")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Metadata(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ReadOnlyDictionary<string, string>
        """
        result = InteropUtils.invoke("rawmessage_get_metadata", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("rawmessage_get_key")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Key(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type byte[]
        """
        result = InteropUtils.invoke("rawmessage_get_key", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("rawmessage_set_key")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_Key(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("rawmessage_set_key", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("rawmessage_get_value")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Value(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type byte[]
        """
        result = InteropUtils.invoke("rawmessage_get_value", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("rawmessage_set_value")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_Value(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("rawmessage_set_value", self._pointer, value)
