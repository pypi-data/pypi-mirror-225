# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .SaslMechanism import SaslMechanism
from ...InteropHelpers.InteropUtils import InteropUtils


class SecurityOptions(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type SecurityOptions
        
        Returns
        ----------
        
        SecurityOptions:
            Instance wrapping the .net type SecurityOptions
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = SecurityOptions._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(SecurityOptions, cls).__new__(cls)
            SecurityOptions._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type SecurityOptions
        
        Returns
        ----------
        
        SecurityOptions:
            Instance wrapping the .net type SecurityOptions
        """
        if '_SecurityOptions_pointer' in dir(self):
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
        del SecurityOptions._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("securityoptions_constructor")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type SecurityOptions
        """
        result = InteropUtils.invoke("securityoptions_constructor")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("securityoptions_constructor2")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor2(sslCertificates: str, username: str, password: str, saslMechanism: SaslMechanism = SaslMechanism.ScramSha256) -> c_void_p:
        """
        Parameters
        ----------
        
        sslCertificates: str
            Underlying .Net type is string
        
        username: str
            Underlying .Net type is string
        
        password: str
            Underlying .Net type is string
        
        saslMechanism: SaslMechanism
            (Optional) Underlying .Net type is SaslMechanism. Defaults to ScramSha256
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type SecurityOptions
        """
        sslCertificates_ptr = InteropUtils.utf8_to_ptr(sslCertificates)
        username_ptr = InteropUtils.utf8_to_ptr(username)
        password_ptr = InteropUtils.utf8_to_ptr(password)
        
        result = InteropUtils.invoke("securityoptions_constructor2", sslCertificates_ptr, username_ptr, password_ptr, saslMechanism.value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("securityoptions_get_saslmechanism")
    _interop_func.restype = InteropUtils.create_nullable(ctypes.c_int)
    _interop_func.argtypes = [c_void_p]
    def get_SaslMechanism(self) -> Optional[SaslMechanism]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[SaslMechanism]:
            Underlying .Net type is SaslMechanism?
        """
        result = InteropUtils.invoke("securityoptions_get_saslmechanism", self._pointer)
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("securityoptions_set_saslmechanism")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, InteropUtils.create_nullable(ctypes.c_int)]
    def set_SaslMechanism(self, value: Optional[SaslMechanism]) -> None:
        """
        Parameters
        ----------
        
        value: Optional[SaslMechanism]
            Underlying .Net type is SaslMechanism?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_conv = value.value
        value_nullable = InteropUtils.create_nullable(ctypes.c_int)(value_conv)
        
        InteropUtils.invoke("securityoptions_set_saslmechanism", self._pointer, value_nullable)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("securityoptions_get_username")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Username(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("securityoptions_get_username", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("securityoptions_set_username")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_Username(self, value: str) -> None:
        """
        Parameters
        ----------
        
        value: str
            Underlying .Net type is string
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        InteropUtils.invoke("securityoptions_set_username", self._pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("securityoptions_get_password")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Password(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("securityoptions_get_password", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("securityoptions_set_password")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_Password(self, value: str) -> None:
        """
        Parameters
        ----------
        
        value: str
            Underlying .Net type is string
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        InteropUtils.invoke("securityoptions_set_password", self._pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("securityoptions_get_sslcertificates")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_SslCertificates(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("securityoptions_get_sslcertificates", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("securityoptions_set_sslcertificates")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_SslCertificates(self, value: str) -> None:
        """
        Parameters
        ----------
        
        value: str
            Underlying .Net type is string
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_ptr = InteropUtils.utf8_to_ptr(value)
        
        InteropUtils.invoke("securityoptions_set_sslcertificates", self._pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("securityoptions_get_usessl")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_UseSsl(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("securityoptions_get_usessl", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("securityoptions_set_usessl")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, ctypes.c_ubyte]
    def set_UseSsl(self, value: bool) -> None:
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
        
        InteropUtils.invoke("securityoptions_set_usessl", self._pointer, value_bool)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("securityoptions_get_usesasl")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_UseSasl(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("securityoptions_get_usesasl", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("securityoptions_set_usesasl")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, ctypes.c_ubyte]
    def set_UseSasl(self, value: bool) -> None:
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
        
        InteropUtils.invoke("securityoptions_set_usesasl", self._pointer, value_bool)
