# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...InteropHelpers.InteropUtils import InteropUtils


class Uri(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type Uri
        
        Returns
        ----------
        
        Uri:
            Instance wrapping the .net type Uri
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = Uri._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(Uri, cls).__new__(cls)
            Uri._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type Uri
        
        Returns
        ----------
        
        Uri:
            Instance wrapping the .net type Uri
        """
        if '_Uri_pointer' in dir(self):
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
        del Uri._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("uri_constructor")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor(uriString: str) -> c_void_p:
        """
        Parameters
        ----------
        
        uriString: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Uri
        """
        uriString_ptr = InteropUtils.utf8_to_ptr(uriString)
        
        result = InteropUtils.invoke("uri_constructor", uriString_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_constructor2")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor2(uriString: str, dontEscape: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        uriString: str
            Underlying .Net type is string
        
        dontEscape: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Uri
        """
        uriString_ptr = InteropUtils.utf8_to_ptr(uriString)
        dontEscape_bool = 1 if dontEscape else 0
        
        result = InteropUtils.invoke("uri_constructor2", uriString_ptr, dontEscape_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_constructor3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_ubyte]
    @staticmethod
    def Constructor3(baseUri: c_void_p, relativeUri: str, dontEscape: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        baseUri: c_void_p
            GC Handle Pointer to .Net type Uri
        
        relativeUri: str
            Underlying .Net type is string
        
        dontEscape: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Uri
        """
        relativeUri_ptr = InteropUtils.utf8_to_ptr(relativeUri)
        dontEscape_bool = 1 if dontEscape else 0
        
        result = InteropUtils.invoke("uri_constructor3", baseUri, relativeUri_ptr, dontEscape_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_constructor6")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Constructor6(baseUri: c_void_p, relativeUri: str) -> c_void_p:
        """
        Parameters
        ----------
        
        baseUri: c_void_p
            GC Handle Pointer to .Net type Uri
        
        relativeUri: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Uri
        """
        relativeUri_ptr = InteropUtils.utf8_to_ptr(relativeUri)
        
        result = InteropUtils.invoke("uri_constructor6", baseUri, relativeUri_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_constructor7")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Constructor7(baseUri: c_void_p, relativeUri: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        baseUri: c_void_p
            GC Handle Pointer to .Net type Uri
        
        relativeUri: c_void_p
            GC Handle Pointer to .Net type Uri
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Uri
        """
        result = InteropUtils.invoke("uri_constructor7", baseUri, relativeUri)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_absolutepath")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_AbsolutePath(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_absolutepath", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_absoluteuri")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_AbsoluteUri(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_absoluteuri", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_localpath")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_LocalPath(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_localpath", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_authority")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Authority(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_authority", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_isdefaultport")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsDefaultPort(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("uri_get_isdefaultport", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_isfile")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsFile(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("uri_get_isfile", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_isloopback")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsLoopback(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("uri_get_isloopback", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_pathandquery")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_PathAndQuery(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_pathandquery", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_segments")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Segments(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type string[]
        """
        result = InteropUtils.invoke("uri_get_segments", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_isunc")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsUnc(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("uri_get_isunc", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_host")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Host(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_host", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_port")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Port(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("uri_get_port", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_query")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Query(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_query", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_fragment")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Fragment(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_fragment", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_scheme")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Scheme(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_scheme", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_originalstring")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_OriginalString(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_originalstring", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_dnssafehost")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_DnsSafeHost(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_dnssafehost", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_idnhost")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_IdnHost(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_idnhost", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_isabsoluteuri")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsAbsoluteUri(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("uri_get_isabsoluteuri", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_userescaped")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_UserEscaped(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("uri_get_userescaped", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_userinfo")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_UserInfo(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_userinfo", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_ishexencoding")
    _interop_func.restype = ctypes.c_ubyte
    @staticmethod
    def IsHexEncoding(pattern: str, index: int) -> bool:
        """
        Parameters
        ----------
        
        pattern: str
            Underlying .Net type is string
        
        index: int
            Underlying .Net type is int
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        pattern_ptr = InteropUtils.utf8_to_ptr(pattern)
        
        result = InteropUtils.invoke("uri_ishexencoding", pattern_ptr, index)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_checkschemename")
    _interop_func.restype = ctypes.c_ubyte
    @staticmethod
    def CheckSchemeName(schemeName: str) -> bool:
        """
        Parameters
        ----------
        
        schemeName: str
            Underlying .Net type is string
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        schemeName_ptr = InteropUtils.utf8_to_ptr(schemeName)
        
        result = InteropUtils.invoke("uri_checkschemename", schemeName_ptr)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_gethashcode")
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
        result = InteropUtils.invoke("uri_gethashcode", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_tostring")
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
        result = InteropUtils.invoke("uri_tostring", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_op_equality")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Equality(uri1: c_void_p, uri2: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        uri1: c_void_p
            GC Handle Pointer to .Net type Uri
        
        uri2: c_void_p
            GC Handle Pointer to .Net type Uri
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("uri_op_equality", uri1, uri2)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_op_inequality")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Inequality(uri1: c_void_p, uri2: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        uri1: c_void_p
            GC Handle Pointer to .Net type Uri
        
        uri2: c_void_p
            GC Handle Pointer to .Net type Uri
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("uri_op_inequality", uri1, uri2)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_equals")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Equals(self, comparand: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        comparand: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("uri_equals", self._pointer, comparand)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_makerelativeuri")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def MakeRelativeUri(self, uri: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        uri: c_void_p
            GC Handle Pointer to .Net type Uri
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Uri
        """
        result = InteropUtils.invoke("uri_makerelativeuri", self._pointer, uri)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_makerelative")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def MakeRelative(self, toUri: c_void_p) -> str:
        """
        Parameters
        ----------
        
        toUri: c_void_p
            GC Handle Pointer to .Net type Uri
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_makerelative", self._pointer, toUri)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_trycreate3")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def TryCreate3(baseUri: c_void_p, relativeUri: str, result: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        baseUri: c_void_p
            GC Handle Pointer to .Net type Uri
        
        relativeUri: str
            Underlying .Net type is string
        
        result: c_void_p
            GC Handle Pointer to .Net type Uri&
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        relativeUri_ptr = InteropUtils.utf8_to_ptr(relativeUri)
        
        result2 = InteropUtils.invoke("uri_trycreate3", baseUri, relativeUri_ptr, result)
        return result2
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_trycreate4")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def TryCreate4(baseUri: c_void_p, relativeUri: c_void_p, result: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        baseUri: c_void_p
            GC Handle Pointer to .Net type Uri
        
        relativeUri: c_void_p
            GC Handle Pointer to .Net type Uri
        
        result: c_void_p
            GC Handle Pointer to .Net type Uri&
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result2 = InteropUtils.invoke("uri_trycreate4", baseUri, relativeUri, result)
        return result2
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_iswellformedoriginalstring")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def IsWellFormedOriginalString(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("uri_iswellformedoriginalstring", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_unescapedatastring")
    _interop_func.restype = c_void_p
    @staticmethod
    def UnescapeDataString(stringToUnescape: str) -> str:
        """
        Parameters
        ----------
        
        stringToUnescape: str
            Underlying .Net type is string
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        stringToUnescape_ptr = InteropUtils.utf8_to_ptr(stringToUnescape)
        
        result = InteropUtils.invoke("uri_unescapedatastring", stringToUnescape_ptr)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_escapeuristring")
    _interop_func.restype = c_void_p
    @staticmethod
    def EscapeUriString(stringToEscape: str) -> str:
        """
        Parameters
        ----------
        
        stringToEscape: str
            Underlying .Net type is string
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        stringToEscape_ptr = InteropUtils.utf8_to_ptr(stringToEscape)
        
        result = InteropUtils.invoke("uri_escapeuristring", stringToEscape_ptr)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_escapedatastring")
    _interop_func.restype = c_void_p
    @staticmethod
    def EscapeDataString(stringToEscape: str) -> str:
        """
        Parameters
        ----------
        
        stringToEscape: str
            Underlying .Net type is string
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        stringToEscape_ptr = InteropUtils.utf8_to_ptr(stringToEscape)
        
        result = InteropUtils.invoke("uri_escapedatastring", stringToEscape_ptr)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_isbaseof")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def IsBaseOf(self, uri: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        uri: c_void_p
            GC Handle Pointer to .Net type Uri
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("uri_isbaseof", self._pointer, uri)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_urischemefile")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UriSchemeFile() -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_urischemefile")
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_urischemeftp")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UriSchemeFtp() -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_urischemeftp")
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_urischemesftp")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UriSchemeSftp() -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_urischemesftp")
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_urischemeftps")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UriSchemeFtps() -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_urischemeftps")
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_urischemegopher")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UriSchemeGopher() -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_urischemegopher")
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_urischemehttp")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UriSchemeHttp() -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_urischemehttp")
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_urischemehttps")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UriSchemeHttps() -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_urischemehttps")
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_urischemews")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UriSchemeWs() -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_urischemews")
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_urischemewss")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UriSchemeWss() -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_urischemewss")
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_urischememailto")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UriSchemeMailto() -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_urischememailto")
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_urischemenews")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UriSchemeNews() -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_urischemenews")
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_urischemenntp")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UriSchemeNntp() -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_urischemenntp")
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_urischemessh")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UriSchemeSsh() -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_urischemessh")
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_urischemetelnet")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UriSchemeTelnet() -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_urischemetelnet")
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_urischemenettcp")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UriSchemeNetTcp() -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_urischemenettcp")
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_urischemenetpipe")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UriSchemeNetPipe() -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_urischemenetpipe")
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("uri_get_schemedelimiter")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_SchemeDelimiter() -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("uri_get_schemedelimiter")
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
