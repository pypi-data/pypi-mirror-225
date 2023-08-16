# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from typing import Callable
from ...QuixStreamsState.StateValue import StateValue
from ...InteropHelpers.InteropUtils import InteropUtils


class StreamScalarState(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamScalarState
        
        Returns
        ----------
        
        StreamScalarState:
            Instance wrapping the .net type StreamScalarState
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = StreamScalarState._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(StreamScalarState, cls).__new__(cls)
            StreamScalarState._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamScalarState
        
        Returns
        ----------
        
        StreamScalarState:
            Instance wrapping the .net type StreamScalarState
        """
        if '_StreamScalarState_pointer' in dir(self):
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
        del StreamScalarState._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("streamscalarstate_add_onflushing")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnFlushing(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler
        
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
                print("Registering value_converter_func_wrapper in streamscalarstate_add_onflushing, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO StreamScalarState._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in streamscalarstate_add_onflushing, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("streamscalarstate_add_onflushing", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamscalarstate_remove_onflushing")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnFlushing(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("streamscalarstate_remove_onflushing", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamscalarstate_add_onflushed")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnFlushed(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler
        
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
                print("Registering value_converter_func_wrapper in streamscalarstate_add_onflushed, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO StreamScalarState._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in streamscalarstate_add_onflushed, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("streamscalarstate_add_onflushed", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamscalarstate_remove_onflushed")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnFlushed(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("streamscalarstate_remove_onflushed", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamscalarstate_clear")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def Clear(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streamscalarstate_clear", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamscalarstate_get_value")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Value(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StateValue
        """
        result = InteropUtils.invoke("streamscalarstate_get_value", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamscalarstate_set_value")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_Value(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type StateValue
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streamscalarstate_set_value", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamscalarstate_flush")
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
        InteropUtils.invoke("streamscalarstate_flush", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamscalarstate_reset")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def Reset(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streamscalarstate_reset", self._pointer)
