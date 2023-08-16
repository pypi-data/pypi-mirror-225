# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ..SystemPrivateUri.System.Uri import Uri
from ..SystemPrivateCoreLib.System.TimeSpan import TimeSpan
from ..InteropHelpers.InteropUtils import InteropUtils


class HttpClient(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type HttpClient
        
        Returns
        ----------
        
        HttpClient:
            Instance wrapping the .net type HttpClient
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = HttpClient._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(HttpClient, cls).__new__(cls)
            HttpClient._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type HttpClient
        
        Returns
        ----------
        
        HttpClient:
            Instance wrapping the .net type HttpClient
        """
        if '_HttpClient_pointer' in dir(self):
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
        del HttpClient._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("httpclient_constructor")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type HttpClient
        """
        result = InteropUtils.invoke("httpclient_constructor")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("httpclient_get_baseaddress")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_BaseAddress(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Uri
        """
        result = InteropUtils.invoke("httpclient_get_baseaddress", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("httpclient_set_baseaddress")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_BaseAddress(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Uri
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("httpclient_set_baseaddress", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("httpclient_get_timeout")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Timeout(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("httpclient_get_timeout", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("httpclient_set_timeout")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_Timeout(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("httpclient_set_timeout", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("httpclient_get_maxresponsecontentbuffersize")
    _interop_func.restype = ctypes.c_longlong
    _interop_func.argtypes = [c_void_p]
    def get_MaxResponseContentBufferSize(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("httpclient_get_maxresponsecontentbuffersize", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("httpclient_set_maxresponsecontentbuffersize")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, ctypes.c_longlong]
    def set_MaxResponseContentBufferSize(self, value: int) -> None:
        """
        Parameters
        ----------
        
        value: int
            Underlying .Net type is long
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_long = ctypes.c_longlong(value)
        
        InteropUtils.invoke("httpclient_set_maxresponsecontentbuffersize", self._pointer, value_long)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("httpclient_getstringasync")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def GetStringAsync(self, requestUri: str) -> c_void_p:
        """
        Parameters
        ----------
        
        requestUri: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<string>
        """
        requestUri_ptr = InteropUtils.utf8_to_ptr(requestUri)
        
        result = InteropUtils.invoke("httpclient_getstringasync", self._pointer, requestUri_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("httpclient_getstringasync2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def GetStringAsync2(self, requestUri: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        requestUri: c_void_p
            GC Handle Pointer to .Net type Uri
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<string>
        """
        result = InteropUtils.invoke("httpclient_getstringasync2", self._pointer, requestUri)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("httpclient_getstringasync3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def GetStringAsync3(self, requestUri: str, cancellationToken: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        requestUri: str
            Underlying .Net type is string
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<string>
        """
        requestUri_ptr = InteropUtils.utf8_to_ptr(requestUri)
        
        result = InteropUtils.invoke("httpclient_getstringasync3", self._pointer, requestUri_ptr, cancellationToken)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("httpclient_getstringasync4")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def GetStringAsync4(self, requestUri: c_void_p, cancellationToken: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        requestUri: c_void_p
            GC Handle Pointer to .Net type Uri
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<string>
        """
        result = InteropUtils.invoke("httpclient_getstringasync4", self._pointer, requestUri, cancellationToken)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("httpclient_getbytearrayasync")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def GetByteArrayAsync(self, requestUri: str) -> c_void_p:
        """
        Parameters
        ----------
        
        requestUri: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<byte[]>
        """
        requestUri_ptr = InteropUtils.utf8_to_ptr(requestUri)
        
        result = InteropUtils.invoke("httpclient_getbytearrayasync", self._pointer, requestUri_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("httpclient_getbytearrayasync2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def GetByteArrayAsync2(self, requestUri: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        requestUri: c_void_p
            GC Handle Pointer to .Net type Uri
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<byte[]>
        """
        result = InteropUtils.invoke("httpclient_getbytearrayasync2", self._pointer, requestUri)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("httpclient_getbytearrayasync3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def GetByteArrayAsync3(self, requestUri: str, cancellationToken: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        requestUri: str
            Underlying .Net type is string
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<byte[]>
        """
        requestUri_ptr = InteropUtils.utf8_to_ptr(requestUri)
        
        result = InteropUtils.invoke("httpclient_getbytearrayasync3", self._pointer, requestUri_ptr, cancellationToken)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("httpclient_getbytearrayasync4")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def GetByteArrayAsync4(self, requestUri: c_void_p, cancellationToken: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        requestUri: c_void_p
            GC Handle Pointer to .Net type Uri
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<byte[]>
        """
        result = InteropUtils.invoke("httpclient_getbytearrayasync4", self._pointer, requestUri, cancellationToken)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("httpclient_cancelpendingrequests")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def CancelPendingRequests(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("httpclient_cancelpendingrequests", self._pointer)
