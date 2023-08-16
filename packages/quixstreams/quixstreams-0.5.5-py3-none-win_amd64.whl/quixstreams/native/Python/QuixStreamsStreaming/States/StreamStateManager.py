# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .StreamDictionaryState import StreamDictionaryState
from .StreamScalarState import StreamScalarState
from ...InteropHelpers.InteropUtils import InteropUtils


class StreamStateManager(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamStateManager
        
        Returns
        ----------
        
        StreamStateManager:
            Instance wrapping the .net type StreamStateManager
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = StreamStateManager._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(StreamStateManager, cls).__new__(cls)
            StreamStateManager._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamStateManager
        
        Returns
        ----------
        
        StreamStateManager:
            Instance wrapping the .net type StreamStateManager
        """
        if '_StreamStateManager_pointer' in dir(self):
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
        del StreamStateManager._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("streamstatemanager_constructor")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Constructor(streamId: str, stateStorage: c_void_p, loggerFactory: c_void_p, logPrefix: str) -> c_void_p:
        """
        Parameters
        ----------
        
        streamId: str
            Underlying .Net type is string
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        loggerFactory: c_void_p
            GC Handle Pointer to .Net type ILoggerFactory
        
        logPrefix: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StreamStateManager
        """
        streamId_ptr = InteropUtils.utf8_to_ptr(streamId)
        logPrefix_ptr = InteropUtils.utf8_to_ptr(logPrefix)
        
        result = InteropUtils.invoke("streamstatemanager_constructor", streamId_ptr, stateStorage, loggerFactory, logPrefix_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamstatemanager_getstates")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetStates(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IEnumerable<string>
        """
        result = InteropUtils.invoke("streamstatemanager_getstates", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamstatemanager_deletestates")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def DeleteStates(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("streamstatemanager_deletestates", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamstatemanager_deletestate")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def DeleteState(self, stateName: str) -> bool:
        """
        Parameters
        ----------
        
        stateName: str
            Underlying .Net type is string
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        stateName_ptr = InteropUtils.utf8_to_ptr(stateName)
        
        result = InteropUtils.invoke("streamstatemanager_deletestate", self._pointer, stateName_ptr)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamstatemanager_getdictionarystate")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def GetDictionaryState(self, stateName: str) -> c_void_p:
        """
        Parameters
        ----------
        
        stateName: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StreamDictionaryState
        """
        stateName_ptr = InteropUtils.utf8_to_ptr(stateName)
        
        result = InteropUtils.invoke("streamstatemanager_getdictionarystate", self._pointer, stateName_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamstatemanager_getscalarstate")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def GetScalarState(self, stateName: str) -> c_void_p:
        """
        Parameters
        ----------
        
        stateName: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StreamScalarState
        """
        stateName_ptr = InteropUtils.utf8_to_ptr(stateName)
        
        result = InteropUtils.invoke("streamstatemanager_getscalarstate", self._pointer, stateName_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
