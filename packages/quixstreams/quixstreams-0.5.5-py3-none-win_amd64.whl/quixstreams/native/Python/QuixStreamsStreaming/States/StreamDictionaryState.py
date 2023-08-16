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


class StreamDictionaryState(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamDictionaryState
        
        Returns
        ----------
        
        StreamDictionaryState:
            Instance wrapping the .net type StreamDictionaryState
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = StreamDictionaryState._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(StreamDictionaryState, cls).__new__(cls)
            StreamDictionaryState._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type StreamDictionaryState
        
        Returns
        ----------
        
        StreamDictionaryState:
            Instance wrapping the .net type StreamDictionaryState
        """
        if '_StreamDictionaryState_pointer' in dir(self):
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
        del StreamDictionaryState._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("streamdictionarystate_add_onflushing")
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
                print("Registering value_converter_func_wrapper in streamdictionarystate_add_onflushing, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO StreamDictionaryState._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in streamdictionarystate_add_onflushing, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("streamdictionarystate_add_onflushing", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_remove_onflushing")
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
        InteropUtils.invoke("streamdictionarystate_remove_onflushing", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_add_onflushed")
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
                print("Registering value_converter_func_wrapper in streamdictionarystate_add_onflushed, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO StreamDictionaryState._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in streamdictionarystate_add_onflushed, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("streamdictionarystate_add_onflushed", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_remove_onflushed")
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
        InteropUtils.invoke("streamdictionarystate_remove_onflushed", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_contains")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Contains(self, key: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        key: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("streamdictionarystate_contains", self._pointer, key)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_remove")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Remove(self, key: c_void_p) -> None:
        """
        Parameters
        ----------
        
        key: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streamdictionarystate_remove", self._pointer, key)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_get_isfixedsize")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsFixedSize(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("streamdictionarystate_get_isfixedsize", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_getenumerator")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetEnumerator(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IEnumerator<KeyValuePair<string, StateValue>>
        """
        result = InteropUtils.invoke("streamdictionarystate_getenumerator", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_add")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Add(self, item: c_void_p) -> None:
        """
        Parameters
        ----------
        
        item: c_void_p
            GC Handle Pointer to .Net type KeyValuePair<string, StateValue>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streamdictionarystate_add", self._pointer, item)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_add2")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def Add2(self, key: c_void_p, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        key: c_void_p
            GC Handle Pointer to .Net type Object
        
        value: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streamdictionarystate_add2", self._pointer, key, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_clear")
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
        InteropUtils.invoke("streamdictionarystate_clear", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_contains2")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Contains2(self, item: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        item: c_void_p
            GC Handle Pointer to .Net type KeyValuePair<string, StateValue>
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("streamdictionarystate_contains2", self._pointer, item)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_copyto")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_int]
    def CopyTo(self, array: c_void_p, arrayIndex: int) -> None:
        """
        Parameters
        ----------
        
        array: c_void_p
            GC Handle Pointer to .Net type KeyValuePair<string, StateValue>[]
        
        arrayIndex: int
            Underlying .Net type is int
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streamdictionarystate_copyto", self._pointer, array, arrayIndex)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_remove2")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Remove2(self, item: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        item: c_void_p
            GC Handle Pointer to .Net type KeyValuePair<string, StateValue>
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("streamdictionarystate_remove2", self._pointer, item)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_copyto2")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_int]
    def CopyTo2(self, array: c_void_p, index: int) -> None:
        """
        Parameters
        ----------
        
        array: c_void_p
            GC Handle Pointer to .Net type Array
        
        index: int
            Underlying .Net type is int
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streamdictionarystate_copyto2", self._pointer, array, index)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_get_count")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Count(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("streamdictionarystate_get_count", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_get_issynchronized")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsSynchronized(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("streamdictionarystate_get_issynchronized", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_get_syncroot")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_SyncRoot(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Object
        """
        result = InteropUtils.invoke("streamdictionarystate_get_syncroot", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_get_isreadonly")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsReadOnly(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("streamdictionarystate_get_isreadonly", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_get_item")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def get_Item(self, key: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        key: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Object
        """
        result = InteropUtils.invoke("streamdictionarystate_get_item", self._pointer, key)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_set_item")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def set_Item(self, key: c_void_p, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        key: c_void_p
            GC Handle Pointer to .Net type Object
        
        value: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("streamdictionarystate_set_item", self._pointer, key, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_add3")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def Add3(self, key: str, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        key: str
            Underlying .Net type is string
        
        value: c_void_p
            GC Handle Pointer to .Net type StateValue
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        InteropUtils.invoke("streamdictionarystate_add3", self._pointer, key_ptr, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_containskey")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def ContainsKey(self, key: str) -> bool:
        """
        Parameters
        ----------
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("streamdictionarystate_containskey", self._pointer, key_ptr)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_remove3")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Remove3(self, key: str) -> bool:
        """
        Parameters
        ----------
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("streamdictionarystate_remove3", self._pointer, key_ptr)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_trygetvalue")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def TryGetValue(self, key: str, value: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        key: str
            Underlying .Net type is string
        
        value: c_void_p
            GC Handle Pointer to .Net type StateValue&
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("streamdictionarystate_trygetvalue", self._pointer, key_ptr, value)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_get_item2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def get_Item2(self, key: str) -> c_void_p:
        """
        Parameters
        ----------
        
        key: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StateValue
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        result = InteropUtils.invoke("streamdictionarystate_get_item2", self._pointer, key_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_set_item2")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def set_Item2(self, key: str, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        key: str
            Underlying .Net type is string
        
        value: c_void_p
            GC Handle Pointer to .Net type StateValue
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        key_ptr = InteropUtils.utf8_to_ptr(key)
        
        InteropUtils.invoke("streamdictionarystate_set_item2", self._pointer, key_ptr, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_get_keys")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Keys(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ICollection<string>
        """
        result = InteropUtils.invoke("streamdictionarystate_get_keys", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_get_values")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Values(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ICollection<StateValue>
        """
        result = InteropUtils.invoke("streamdictionarystate_get_values", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_flush")
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
        InteropUtils.invoke("streamdictionarystate_flush", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("streamdictionarystate_reset")
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
        InteropUtils.invoke("streamdictionarystate_reset", self._pointer)
