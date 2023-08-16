# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ....SystemPrivateCoreLib.System.DateTime import DateTime
from ....InteropHelpers.InteropUtils import InteropUtils


class StreamPropertiesProducer(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamPropertiesProducer
        
        Returns
        ----------
        
        StreamPropertiesProducer:
            Instance wrapping the .net type StreamPropertiesProducer
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = StreamPropertiesProducer._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(StreamPropertiesProducer, cls).__new__(cls)
            StreamPropertiesProducer._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamPropertiesProducer
        
        Returns
        ----------
        
        StreamPropertiesProducer:
            Instance wrapping the .net type StreamPropertiesProducer
        """
        if '_StreamPropertiesProducer_pointer' in dir(self):
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
        del StreamPropertiesProducer._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("streampropertiesproducer_get_flushinterval")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_FlushInterval(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("streampropertiesproducer_get_flushinterval", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampropertiesproducer_set_flushinterval")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, ctypes.c_int]
    def set_FlushInterval(self, value: int) -> None:
        """
        Parameters
        ----------
        
        value: int
            Underlying .Net type is int
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streampropertiesproducer_set_flushinterval", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampropertiesproducer_get_name")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Name(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("streampropertiesproducer_get_name", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampropertiesproducer_set_name")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_Name(self, value: str) -> None:
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
        
        InteropUtils.invoke("streampropertiesproducer_set_name", self._pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampropertiesproducer_get_location")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Location(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("streampropertiesproducer_get_location", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampropertiesproducer_set_location")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_Location(self, value: str) -> None:
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
        
        InteropUtils.invoke("streampropertiesproducer_set_location", self._pointer, value_ptr)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampropertiesproducer_get_timeofrecording")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_TimeOfRecording(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime?
        """
        result = InteropUtils.invoke("streampropertiesproducer_get_timeofrecording", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampropertiesproducer_set_timeofrecording")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_TimeOfRecording(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type DateTime?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streampropertiesproducer_set_timeofrecording", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampropertiesproducer_get_metadata")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Metadata(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ObservableDictionary<string, string>
        """
        result = InteropUtils.invoke("streampropertiesproducer_get_metadata", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampropertiesproducer_get_parents")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Parents(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ObservableCollection<string>
        """
        result = InteropUtils.invoke("streampropertiesproducer_get_parents", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampropertiesproducer_addparent")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def AddParent(self, parentStreamId: str) -> None:
        """
        Parameters
        ----------
        
        parentStreamId: str
            Underlying .Net type is string
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        parentStreamId_ptr = InteropUtils.utf8_to_ptr(parentStreamId)
        
        InteropUtils.invoke("streampropertiesproducer_addparent", self._pointer, parentStreamId_ptr)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampropertiesproducer_removeparent")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def RemoveParent(self, parentStreamId: str) -> None:
        """
        Parameters
        ----------
        
        parentStreamId: str
            Underlying .Net type is string
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        parentStreamId_ptr = InteropUtils.utf8_to_ptr(parentStreamId)
        
        InteropUtils.invoke("streampropertiesproducer_removeparent", self._pointer, parentStreamId_ptr)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampropertiesproducer_flush")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def Flush(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streampropertiesproducer_flush", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streampropertiesproducer_dispose")
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
        InteropUtils.invoke("streampropertiesproducer_dispose", self._pointer)
