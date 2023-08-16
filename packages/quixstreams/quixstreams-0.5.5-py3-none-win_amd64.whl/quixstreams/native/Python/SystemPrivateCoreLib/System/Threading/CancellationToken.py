# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ....InteropHelpers.InteropUtils import InteropUtils


class CancellationToken(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        ----------
        
        CancellationToken:
            Instance wrapping the .net type CancellationToken
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = CancellationToken._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(CancellationToken, cls).__new__(cls)
            CancellationToken._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        ----------
        
        CancellationToken:
            Instance wrapping the .net type CancellationToken
        """
        if '_CancellationToken_pointer' in dir(self):
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
        del CancellationToken._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("cancellationtoken_constructor")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor(canceled: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        canceled: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationToken
        """
        canceled_bool = 1 if canceled else 0
        
        result = InteropUtils.invoke("cancellationtoken_constructor", canceled_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtoken_get_none")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_None() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationToken
        """
        result = InteropUtils.invoke("cancellationtoken_get_none")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtoken_get_iscancellationrequested")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsCancellationRequested(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("cancellationtoken_get_iscancellationrequested", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtoken_get_canbecanceled")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_CanBeCanceled(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("cancellationtoken_get_canbecanceled", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtoken_equals")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Equals(self, other: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        other: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("cancellationtoken_equals", self._pointer, other)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtoken_equals2")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Equals2(self, other: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        other: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("cancellationtoken_equals2", self._pointer, other)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtoken_gethashcode")
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
        result = InteropUtils.invoke("cancellationtoken_gethashcode", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtoken_op_equality")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Equality(left: c_void_p, right: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        left: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        right: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("cancellationtoken_op_equality", left, right)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtoken_op_inequality")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Inequality(left: c_void_p, right: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        left: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        right: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("cancellationtoken_op_inequality", left, right)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtoken_throwifcancellationrequested")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def ThrowIfCancellationRequested(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("cancellationtoken_throwifcancellationrequested", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtoken_tostring")
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
        result = InteropUtils.invoke("cancellationtoken_tostring", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
