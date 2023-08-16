# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ..SystemPrivateCoreLib.System.Threading.Tasks.Task import Task
from typing import Callable
from ..InteropHelpers.InteropUtils import InteropUtils


class IStreamPipeline(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type IStreamPipeline
        
        Returns
        ----------
        
        IStreamPipeline:
            Instance wrapping the .net type IStreamPipeline
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = IStreamPipeline._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(IStreamPipeline, cls).__new__(cls)
            IStreamPipeline._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type IStreamPipeline
        
        Returns
        ----------
        
        IStreamPipeline:
            Instance wrapping the .net type IStreamPipeline
        """
        if '_IStreamPipeline_pointer' in dir(self):
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
        del IStreamPipeline._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("istreampipeline_get_streamid")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_StreamId(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("istreampipeline_get_streamid", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("istreampipeline_get_sourcemetadata")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_SourceMetadata(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Dictionary<string, string>
        """
        result = InteropUtils.invoke("istreampipeline_get_sourcemetadata", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("istreampipeline_set_sourcemetadata")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_SourceMetadata(self, value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Dictionary<string, string>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("istreampipeline_set_sourcemetadata", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("istreampipeline_send")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Send(self, package: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        package: c_void_p
            GC Handle Pointer to .Net type StreamPackage
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        result = InteropUtils.invoke("istreampipeline_send", self._pointer, package)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("istreampipeline_subscribe")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Subscribe(self, onStreamPackage: Callable[[c_void_p, c_void_p], c_void_p]) -> c_void_p:
        """
        Parameters
        ----------
        
        onStreamPackage: Callable[[c_void_p, c_void_p], c_void_p]
            Underlying .Net type is Func<IStreamPipeline, StreamPackage, Task>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IStreamPipeline
        """
        onStreamPackage_func_wrapper_addr = None
        if onStreamPackage is not None:
            onStreamPackage_converter = lambda p0, p1: onStreamPackage(c_void_p(p0), c_void_p(p1))

            onStreamPackage_converter_func_wrapper = ctypes.CFUNCTYPE(c_void_p, c_void_p, c_void_p)(onStreamPackage_converter)
            onStreamPackage_func_wrapper_addr = ctypes.cast(onStreamPackage_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering onStreamPackage_converter_func_wrapper in istreampipeline_subscribe, addr {}".format(onStreamPackage_func_wrapper_addr))
                onStreamPackage_func_wrapper_addr_val = onStreamPackage_func_wrapper_addr.value
                # TODO IStreamPipeline._weakrefs.append(weakref.ref(onStreamPackage_converter_func_wrapper, lambda x: print("De-referenced onStreamPackage_converter_func_wrapper in istreampipeline_subscribe, addr {}".format(onStreamPackage_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("istreampipeline_subscribe", self._pointer, onStreamPackage_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, onStreamPackage_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("istreampipeline_subscribe3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Subscribe3(self, onStreamPackage: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        onStreamPackage: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is Action<IStreamPipeline, StreamPackage>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IStreamPipeline
        """
        onStreamPackage_func_wrapper_addr = None
        if onStreamPackage is not None:
            onStreamPackage_converter = lambda p0, p1: onStreamPackage(c_void_p(p0), c_void_p(p1))

            onStreamPackage_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p, c_void_p)(onStreamPackage_converter)
            onStreamPackage_func_wrapper_addr = ctypes.cast(onStreamPackage_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering onStreamPackage_converter_func_wrapper in istreampipeline_subscribe3, addr {}".format(onStreamPackage_func_wrapper_addr))
                onStreamPackage_func_wrapper_addr_val = onStreamPackage_func_wrapper_addr.value
                # TODO IStreamPipeline._weakrefs.append(weakref.ref(onStreamPackage_converter_func_wrapper, lambda x: print("De-referenced onStreamPackage_converter_func_wrapper in istreampipeline_subscribe3, addr {}".format(onStreamPackage_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("istreampipeline_subscribe3", self._pointer, onStreamPackage_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, onStreamPackage_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("istreampipeline_close")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def Close(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("istreampipeline_close", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("istreampipeline_add_onclosing")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnClosing(self, value: Callable[[], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        value: Callable[[], None]
            Underlying .Net type is Action
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IntPtr
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda : value()

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in istreampipeline_add_onclosing, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO IStreamPipeline._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in istreampipeline_add_onclosing, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("istreampipeline_add_onclosing", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("istreampipeline_remove_onclosing")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnClosing(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("istreampipeline_remove_onclosing", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("istreampipeline_add_onclosed")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnClosed(self, value: Callable[[], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        value: Callable[[], None]
            Underlying .Net type is Action
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IntPtr
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda : value()

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in istreampipeline_add_onclosed, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO IStreamPipeline._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in istreampipeline_add_onclosed, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("istreampipeline_add_onclosed", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("istreampipeline_remove_onclosed")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnClosed(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("istreampipeline_remove_onclosed", self._pointer, value)
