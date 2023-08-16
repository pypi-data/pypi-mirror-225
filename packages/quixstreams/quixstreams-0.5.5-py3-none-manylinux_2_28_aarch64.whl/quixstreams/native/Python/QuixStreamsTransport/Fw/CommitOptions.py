# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...InteropHelpers.InteropUtils import InteropUtils


class CommitOptions(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type CommitOptions
        
        Returns
        ----------
        
        CommitOptions:
            Instance wrapping the .net type CommitOptions
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = CommitOptions._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(CommitOptions, cls).__new__(cls)
            CommitOptions._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type CommitOptions
        
        Returns
        ----------
        
        CommitOptions:
            Instance wrapping the .net type CommitOptions
        """
        if '_CommitOptions_pointer' in dir(self):
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
        del CommitOptions._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("commitoptions_constructor")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CommitOptions
        """
        result = InteropUtils.invoke("commitoptions_constructor")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("commitoptions_get_autocommitenabled")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_AutoCommitEnabled(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("commitoptions_get_autocommitenabled", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("commitoptions_set_autocommitenabled")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, ctypes.c_ubyte]
    def set_AutoCommitEnabled(self, value: bool) -> None:
        """
        Parameters
        ----------
        
        value: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_bool = 1 if value else 0
        
        InteropUtils.invoke("commitoptions_set_autocommitenabled", self._pointer, value_bool)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("commitoptions_get_commitinterval")
    _interop_func.restype = InteropUtils.create_nullable(ctypes.c_int)
    _interop_func.argtypes = [c_void_p]
    def get_CommitInterval(self) -> Optional[int]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[int]:
            Underlying .Net type is int?
        """
        result = InteropUtils.invoke("commitoptions_get_commitinterval", self._pointer)
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("commitoptions_set_commitinterval")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, InteropUtils.create_nullable(ctypes.c_int)]
    def set_CommitInterval(self, value: Optional[int]) -> None:
        """
        Parameters
        ----------
        
        value: Optional[int]
            Underlying .Net type is int?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_nullable = InteropUtils.create_nullable(ctypes.c_int)(value)
        
        InteropUtils.invoke("commitoptions_set_commitinterval", self._pointer, value_nullable)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("commitoptions_get_commitevery")
    _interop_func.restype = InteropUtils.create_nullable(ctypes.c_int)
    _interop_func.argtypes = [c_void_p]
    def get_CommitEvery(self) -> Optional[int]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[int]:
            Underlying .Net type is int?
        """
        result = InteropUtils.invoke("commitoptions_get_commitevery", self._pointer)
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("commitoptions_set_commitevery")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, InteropUtils.create_nullable(ctypes.c_int)]
    def set_CommitEvery(self, value: Optional[int]) -> None:
        """
        Parameters
        ----------
        
        value: Optional[int]
            Underlying .Net type is int?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_nullable = InteropUtils.create_nullable(ctypes.c_int)(value)
        
        InteropUtils.invoke("commitoptions_set_commitevery", self._pointer, value_nullable)
