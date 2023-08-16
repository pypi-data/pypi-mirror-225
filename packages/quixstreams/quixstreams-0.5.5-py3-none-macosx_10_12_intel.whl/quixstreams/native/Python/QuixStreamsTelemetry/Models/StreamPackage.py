# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...SystemPrivateCoreLib.System.Type import Type
from ...QuixStreamsTransport.IO.TransportContext import TransportContext
from ...InteropHelpers.InteropUtils import InteropUtils


class StreamPackage(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamPackage
        
        Returns
        ----------
        
        StreamPackage:
            Instance wrapping the .net type StreamPackage
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = StreamPackage._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(StreamPackage, cls).__new__(cls)
            StreamPackage._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamPackage
        
        Returns
        ----------
        
        StreamPackage:
            Instance wrapping the .net type StreamPackage
        """
        if '_StreamPackage_pointer' in dir(self):
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
        del StreamPackage._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("streampackage_constructor")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Constructor(type: c_void_p, value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        type: c_void_p
            GC Handle Pointer to .Net type Type
        
        value: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StreamPackage
        """
        result = InteropUtils.invoke("streampackage_constructor", type, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampackage_get_type")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Type(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("streampackage_get_type", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampackage_set_type")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_Type(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streampackage_set_type", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampackage_get_transportcontext")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_TransportContext(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TransportContext
        """
        result = InteropUtils.invoke("streampackage_get_transportcontext", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampackage_set_transportcontext")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_TransportContext(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type TransportContext
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streampackage_set_transportcontext", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampackage_get_value")
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
        result = InteropUtils.invoke("streampackage_get_value", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampackage_set_value")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_Value(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streampackage_set_value", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampackage_tojson")
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
        result = InteropUtils.invoke("streampackage_tojson", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
