# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...SystemPrivateCoreLib.System.Threading.Tasks.Task import Task
from .IStateStorage import IStateStorage
from ...InteropHelpers.InteropUtils import InteropUtils


class InMemoryStorage(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type InMemoryStorage
        
        Returns
        ----------
        
        InMemoryStorage:
            Instance wrapping the .net type InMemoryStorage
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = InMemoryStorage._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(InMemoryStorage, cls).__new__(cls)
            InMemoryStorage._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type InMemoryStorage
        
        Returns
        ----------
        
        InMemoryStorage:
            Instance wrapping the .net type InMemoryStorage
        """
        if '_InMemoryStorage_pointer' in dir(self):
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
        del InMemoryStorage._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("inmemorystorage_constructor")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type InMemoryStorage
        """
        result = InteropUtils.invoke("inmemorystorage_constructor")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("inmemorystorage_saveraw")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def SaveRaw(self, key: str, data: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        key: str
            Underlying .Net type is string
        
        data: c_void_p
            GC Handle Pointer to .Net type byte[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("inmemorystorage_saveraw", self._pointer, key_ptr, data)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("inmemorystorage_loadraw")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def LoadRaw(self, key: str) -> c_void_p:
        """
        Parameters
        ----------
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<byte[]>
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("inmemorystorage_loadraw", self._pointer, key_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("inmemorystorage_removeasync")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def RemoveAsync(self, key: str) -> c_void_p:
        """
        Parameters
        ----------
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("inmemorystorage_removeasync", self._pointer, key_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("inmemorystorage_containskeyasync")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def ContainsKeyAsync(self, key: str) -> c_void_p:
        """
        Parameters
        ----------
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<Boolean>
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("inmemorystorage_containskeyasync", self._pointer, key_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("inmemorystorage_getallkeysasync")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetAllKeysAsync(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<string[]>
        """
        result = InteropUtils.invoke("inmemorystorage_getallkeysasync", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("inmemorystorage_clearasync")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def ClearAsync(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        result = InteropUtils.invoke("inmemorystorage_clearasync", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("inmemorystorage_count")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def Count(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<int>
        """
        result = InteropUtils.invoke("inmemorystorage_count", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("inmemorystorage_get_iscasesensitive")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsCaseSensitive(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("inmemorystorage_get_iscasesensitive", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("inmemorystorage_getorcreatesubstorage")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def GetOrCreateSubStorage(self, subStorageName: str) -> c_void_p:
        """
        Parameters
        ----------
        
        subStorageName: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IStateStorage
        """
        subStorageName_ptr = InteropUtils.utf8_to_ptr(subStorageName)
        
        result = InteropUtils.invoke("inmemorystorage_getorcreatesubstorage", self._pointer, subStorageName_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("inmemorystorage_deletesubstorage")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def DeleteSubStorage(self, subStorageName: str) -> bool:
        """
        Parameters
        ----------
        
        subStorageName: str
            Underlying .Net type is string
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        subStorageName_ptr = InteropUtils.utf8_to_ptr(subStorageName)
        
        result = InteropUtils.invoke("inmemorystorage_deletesubstorage", self._pointer, subStorageName_ptr)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("inmemorystorage_deletesubstorages")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def DeleteSubStorages(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("inmemorystorage_deletesubstorages", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("inmemorystorage_getsubstorages")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetSubStorages(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IEnumerable<string>
        """
        result = InteropUtils.invoke("inmemorystorage_getsubstorages", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
