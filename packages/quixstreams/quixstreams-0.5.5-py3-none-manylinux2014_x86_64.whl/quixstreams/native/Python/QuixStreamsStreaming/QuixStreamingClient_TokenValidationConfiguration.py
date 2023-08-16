# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ..SystemPrivateCoreLib.System.TimeSpan import TimeSpan
from ..InteropHelpers.InteropUtils import InteropUtils


class TokenValidationConfiguration(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TokenValidationConfiguration
        
        Returns
        ----------
        
        TokenValidationConfiguration:
            Instance wrapping the .net type TokenValidationConfiguration
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = TokenValidationConfiguration._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(TokenValidationConfiguration, cls).__new__(cls)
            TokenValidationConfiguration._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TokenValidationConfiguration
        
        Returns
        ----------
        
        TokenValidationConfiguration:
            Instance wrapping the .net type TokenValidationConfiguration
        """
        if '_TokenValidationConfiguration_pointer' in dir(self):
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
        del TokenValidationConfiguration._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("tokenvalidationconfiguration_constructor")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type QuixStreamingClient.TokenValidationConfiguration
        """
        result = InteropUtils.invoke("tokenvalidationconfiguration_constructor")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("tokenvalidationconfiguration_get_enabled")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_Enabled(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("tokenvalidationconfiguration_get_enabled", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("tokenvalidationconfiguration_set_enabled")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, ctypes.c_ubyte]
    def set_Enabled(self, value: bool) -> None:
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
        
        InteropUtils.invoke("tokenvalidationconfiguration_set_enabled", self._pointer, value_bool)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("tokenvalidationconfiguration_get_warningbeforeexpiry")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_WarningBeforeExpiry(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan?
        """
        result = InteropUtils.invoke("tokenvalidationconfiguration_get_warningbeforeexpiry", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("tokenvalidationconfiguration_set_warningbeforeexpiry")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_WarningBeforeExpiry(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type TimeSpan?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("tokenvalidationconfiguration_set_warningbeforeexpiry", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("tokenvalidationconfiguration_get_warnaboutnonpattoken")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_WarnAboutNonPatToken(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("tokenvalidationconfiguration_get_warnaboutnonpattoken", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("tokenvalidationconfiguration_set_warnaboutnonpattoken")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, ctypes.c_ubyte]
    def set_WarnAboutNonPatToken(self, value: bool) -> None:
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
        
        InteropUtils.invoke("tokenvalidationconfiguration_set_warnaboutnonpattoken", self._pointer, value_bool)
