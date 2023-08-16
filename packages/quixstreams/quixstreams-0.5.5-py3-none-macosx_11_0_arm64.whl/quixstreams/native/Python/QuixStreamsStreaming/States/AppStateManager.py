# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .TopicStateManager import TopicStateManager
from ...InteropHelpers.InteropUtils import InteropUtils


class AppStateManager(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type AppStateManager
        
        Returns
        ----------
        
        AppStateManager:
            Instance wrapping the .net type AppStateManager
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = AppStateManager._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(AppStateManager, cls).__new__(cls)
            AppStateManager._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type AppStateManager
        
        Returns
        ----------
        
        AppStateManager:
            Instance wrapping the .net type AppStateManager
        """
        if '_AppStateManager_pointer' in dir(self):
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
        del AppStateManager._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("appstatemanager_constructor")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Constructor(storage: c_void_p, loggerFactory: c_void_p = None) -> c_void_p:
        """
        Parameters
        ----------
        
        storage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        loggerFactory: c_void_p
            (Optional) GC Handle Pointer to .Net type ILoggerFactory. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type AppStateManager
        """
        result = InteropUtils.invoke("appstatemanager_constructor", storage, loggerFactory)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("appstatemanager_gettopicstates")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetTopicStates(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IEnumerable<string>
        """
        result = InteropUtils.invoke("appstatemanager_gettopicstates", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("appstatemanager_deletetopicstates")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def DeleteTopicStates(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("appstatemanager_deletetopicstates", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("appstatemanager_deletetopicstate")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def DeleteTopicState(self, topicName: str) -> bool:
        """
        Parameters
        ----------
        
        topicName: str
            Underlying .Net type is string
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        topicName_ptr = InteropUtils.utf8_to_ptr(topicName)
        
        result = InteropUtils.invoke("appstatemanager_deletetopicstate", self._pointer, topicName_ptr)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("appstatemanager_gettopicstatemanager")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def GetTopicStateManager(self, topicName: str) -> c_void_p:
        """
        Parameters
        ----------
        
        topicName: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TopicStateManager
        """
        topicName_ptr = InteropUtils.utf8_to_ptr(topicName)
        
        result = InteropUtils.invoke("appstatemanager_gettopicstatemanager", self._pointer, topicName_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
