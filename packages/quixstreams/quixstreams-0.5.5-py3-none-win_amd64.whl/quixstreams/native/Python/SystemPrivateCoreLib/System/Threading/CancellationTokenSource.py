# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .CancellationToken import CancellationToken
from .Tasks.Task import Task
from ....InteropHelpers.InteropUtils import InteropUtils


class CancellationTokenSource(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type CancellationTokenSource
        
        Returns
        ----------
        
        CancellationTokenSource:
            Instance wrapping the .net type CancellationTokenSource
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = CancellationTokenSource._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(CancellationTokenSource, cls).__new__(cls)
            CancellationTokenSource._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type CancellationTokenSource
        
        Returns
        ----------
        
        CancellationTokenSource:
            Instance wrapping the .net type CancellationTokenSource
        """
        if '_CancellationTokenSource_pointer' in dir(self):
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
        del CancellationTokenSource._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("cancellationtokensource_constructor")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationTokenSource
        """
        result = InteropUtils.invoke("cancellationtokensource_constructor")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtokensource_constructor2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def Constructor2(delay: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        delay: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationTokenSource
        """
        result = InteropUtils.invoke("cancellationtokensource_constructor2", delay)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtokensource_constructor3")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor3(millisecondsDelay: int) -> c_void_p:
        """
        Parameters
        ----------
        
        millisecondsDelay: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationTokenSource
        """
        result = InteropUtils.invoke("cancellationtokensource_constructor3", millisecondsDelay)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtokensource_get_iscancellationrequested")
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
        result = InteropUtils.invoke("cancellationtokensource_get_iscancellationrequested", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtokensource_get_token")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Token(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationToken
        """
        result = InteropUtils.invoke("cancellationtokensource_get_token", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtokensource_cancel")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def Cancel(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("cancellationtokensource_cancel", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtokensource_cancel2")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, ctypes.c_ubyte]
    def Cancel2(self, throwOnFirstException: bool) -> None:
        """
        Parameters
        ----------
        
        throwOnFirstException: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        throwOnFirstException_bool = 1 if throwOnFirstException else 0
        
        InteropUtils.invoke("cancellationtokensource_cancel2", self._pointer, throwOnFirstException_bool)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtokensource_cancelasync")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def CancelAsync(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        result = InteropUtils.invoke("cancellationtokensource_cancelasync", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtokensource_cancelafter")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def CancelAfter(self, delay: c_void_p) -> None:
        """
        Parameters
        ----------
        
        delay: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("cancellationtokensource_cancelafter", self._pointer, delay)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtokensource_cancelafter2")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, ctypes.c_int]
    def CancelAfter2(self, millisecondsDelay: int) -> None:
        """
        Parameters
        ----------
        
        millisecondsDelay: int
            Underlying .Net type is int
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("cancellationtokensource_cancelafter2", self._pointer, millisecondsDelay)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtokensource_tryreset")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def TryReset(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("cancellationtokensource_tryreset", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtokensource_dispose")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def Dispose(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("cancellationtokensource_dispose", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtokensource_createlinkedtokensource")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def CreateLinkedTokenSource(token1: c_void_p, token2: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        token1: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        token2: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationTokenSource
        """
        result = InteropUtils.invoke("cancellationtokensource_createlinkedtokensource", token1, token2)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtokensource_createlinkedtokensource2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def CreateLinkedTokenSource2(token: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        token: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationTokenSource
        """
        result = InteropUtils.invoke("cancellationtokensource_createlinkedtokensource2", token)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("cancellationtokensource_createlinkedtokensource3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def CreateLinkedTokenSource3(tokens: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        tokens: c_void_p
            GC Handle Pointer to .Net type CancellationToken[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type CancellationTokenSource
        """
        result = InteropUtils.invoke("cancellationtokensource_createlinkedtokensource3", tokens)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
