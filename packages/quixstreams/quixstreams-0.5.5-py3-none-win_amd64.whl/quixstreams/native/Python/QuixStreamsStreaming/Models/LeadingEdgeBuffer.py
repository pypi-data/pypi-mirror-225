# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from typing import Callable
from .LeadingEdgeTimestamp import LeadingEdgeTimestamp
from ...InteropHelpers.InteropUtils import InteropUtils


class LeadingEdgeBuffer(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type LeadingEdgeBuffer
        
        Returns
        ----------
        
        LeadingEdgeBuffer:
            Instance wrapping the .net type LeadingEdgeBuffer
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = LeadingEdgeBuffer._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(LeadingEdgeBuffer, cls).__new__(cls)
            LeadingEdgeBuffer._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type LeadingEdgeBuffer
        
        Returns
        ----------
        
        LeadingEdgeBuffer:
            Instance wrapping the .net type LeadingEdgeBuffer
        """
        if '_LeadingEdgeBuffer_pointer' in dir(self):
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
        del LeadingEdgeBuffer._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("leadingedgebuffer_add_onbackfill")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnBackfill(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler<TimeseriesData>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IntPtr
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0, p1: value(c_void_p(p0), c_void_p(p1))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in leadingedgebuffer_add_onbackfill, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO LeadingEdgeBuffer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in leadingedgebuffer_add_onbackfill, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("leadingedgebuffer_add_onbackfill", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("leadingedgebuffer_remove_onbackfill")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnBackfill(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type IntPtr
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("leadingedgebuffer_remove_onbackfill", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("leadingedgebuffer_add_onpublish")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnPublish(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler<TimeseriesData>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IntPtr
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0, p1: value(c_void_p(p0), c_void_p(p1))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in leadingedgebuffer_add_onpublish, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO LeadingEdgeBuffer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in leadingedgebuffer_add_onpublish, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("leadingedgebuffer_add_onpublish", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("leadingedgebuffer_remove_onpublish")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnPublish(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type IntPtr
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("leadingedgebuffer_remove_onpublish", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("leadingedgebuffer_get_epoch")
    _interop_func.restype = InteropUtils.create_nullable(ctypes.c_longlong)
    _interop_func.argtypes = [c_void_p]
    def get_Epoch(self) -> Optional[int]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[int]:
            Underlying .Net type is long?
        """
        result = InteropUtils.invoke("leadingedgebuffer_get_epoch", self._pointer)
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("leadingedgebuffer_set_epoch")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, InteropUtils.create_nullable(ctypes.c_longlong)]
    def set_Epoch(self, value: Optional[int]) -> None:
        """
        Parameters
        ----------
        
        value: Optional[int]
            Underlying .Net type is long?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_nullable = InteropUtils.create_nullable(ctypes.c_longlong)(value)
        
        InteropUtils.invoke("leadingedgebuffer_set_epoch", self._pointer, value_nullable)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("leadingedgebuffer_getorcreatetimestamp")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_longlong, c_void_p]
    def GetOrCreateTimestamp(self, timestampInNanoseconds: int, tags: c_void_p = None) -> c_void_p:
        """
        Parameters
        ----------
        
        timestampInNanoseconds: int
            Underlying .Net type is long
        
        tags: c_void_p
            (Optional) GC Handle Pointer to .Net type Dictionary<string, string>. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type LeadingEdgeTimestamp
        """
        timestampInNanoseconds_long = ctypes.c_longlong(timestampInNanoseconds)
        
        result = InteropUtils.invoke("leadingedgebuffer_getorcreatetimestamp", self._pointer, timestampInNanoseconds_long, tags)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("leadingedgebuffer_flush")
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
        InteropUtils.invoke("leadingedgebuffer_flush", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("leadingedgebuffer_publish")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def Publish(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("leadingedgebuffer_publish", self._pointer)
