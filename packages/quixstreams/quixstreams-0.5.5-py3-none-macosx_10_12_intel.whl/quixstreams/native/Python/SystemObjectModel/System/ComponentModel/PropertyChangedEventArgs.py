# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ....InteropHelpers.InteropUtils import InteropUtils


class PropertyChangedEventArgs(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type PropertyChangedEventArgs
        
        Returns
        ----------
        
        PropertyChangedEventArgs:
            Instance wrapping the .net type PropertyChangedEventArgs
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = PropertyChangedEventArgs._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(PropertyChangedEventArgs, cls).__new__(cls)
            PropertyChangedEventArgs._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type PropertyChangedEventArgs
        
        Returns
        ----------
        
        PropertyChangedEventArgs:
            Instance wrapping the .net type PropertyChangedEventArgs
        """
        if '_PropertyChangedEventArgs_pointer' in dir(self):
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
        del PropertyChangedEventArgs._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("propertychangedeventargs_constructor")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor(propertyName: str) -> c_void_p:
        """
        Parameters
        ----------
        
        propertyName: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type PropertyChangedEventArgs
        """
        propertyName_ptr = InteropUtils.utf8_to_ptr(propertyName)
        
        result = InteropUtils.invoke("propertychangedeventargs_constructor", propertyName_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("propertychangedeventargs_get_propertyname")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_PropertyName(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("propertychangedeventargs_get_propertyname", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
