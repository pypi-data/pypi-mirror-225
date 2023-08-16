# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...InteropHelpers.InteropUtils import InteropUtils


class TransportContext(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TransportContext
        
        Returns
        ----------
        
        TransportContext:
            Instance wrapping the .net type TransportContext
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = TransportContext._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(TransportContext, cls).__new__(cls)
            TransportContext._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TransportContext
        
        Returns
        ----------
        
        TransportContext:
            Instance wrapping the .net type TransportContext
        """
        if '_TransportContext_pointer' in dir(self):
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
        del TransportContext._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("transportcontext_constructor")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def Constructor(dictionary: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        dictionary: c_void_p
            GC Handle Pointer to .Net type IDictionary<string, Object>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TransportContext
        """
        result = InteropUtils.invoke("transportcontext_constructor", dictionary)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("transportcontext_constructor2")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor2() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TransportContext
        """
        result = InteropUtils.invoke("transportcontext_constructor2")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
