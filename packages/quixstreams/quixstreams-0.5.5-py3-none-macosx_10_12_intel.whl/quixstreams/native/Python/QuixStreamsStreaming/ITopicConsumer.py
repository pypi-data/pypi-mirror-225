# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from typing import Callable
from .States.TopicStateManager import TopicStateManager
from ..InteropHelpers.InteropUtils import InteropUtils


class ITopicConsumer(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ITopicConsumer
        
        Returns
        ----------
        
        ITopicConsumer:
            Instance wrapping the .net type ITopicConsumer
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = ITopicConsumer._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(ITopicConsumer, cls).__new__(cls)
            ITopicConsumer._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ITopicConsumer
        
        Returns
        ----------
        
        ITopicConsumer:
            Instance wrapping the .net type ITopicConsumer
        """
        if '_ITopicConsumer_pointer' in dir(self):
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
        del ITopicConsumer._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("itopicconsumer_subscribe")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def Subscribe(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("itopicconsumer_subscribe", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicconsumer_add_onstreamreceived")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnStreamReceived(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler<IStreamConsumer>
        
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
                print("Registering value_converter_func_wrapper in itopicconsumer_add_onstreamreceived, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO ITopicConsumer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in itopicconsumer_add_onstreamreceived, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("itopicconsumer_add_onstreamreceived", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicconsumer_remove_onstreamreceived")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnStreamReceived(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("itopicconsumer_remove_onstreamreceived", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicconsumer_add_onrevoking")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnRevoking(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
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
                print("Registering value_converter_func_wrapper in itopicconsumer_add_onrevoking, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO ITopicConsumer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in itopicconsumer_add_onrevoking, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("itopicconsumer_add_onrevoking", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicconsumer_remove_onrevoking")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnRevoking(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("itopicconsumer_remove_onrevoking", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicconsumer_add_onstreamsrevoked")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnStreamsRevoked(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler<IStreamConsumer[]>
        
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
                print("Registering value_converter_func_wrapper in itopicconsumer_add_onstreamsrevoked, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO ITopicConsumer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in itopicconsumer_add_onstreamsrevoked, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("itopicconsumer_add_onstreamsrevoked", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicconsumer_remove_onstreamsrevoked")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnStreamsRevoked(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("itopicconsumer_remove_onstreamsrevoked", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicconsumer_add_oncommitted")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnCommitted(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
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
                print("Registering value_converter_func_wrapper in itopicconsumer_add_oncommitted, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO ITopicConsumer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in itopicconsumer_add_oncommitted, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("itopicconsumer_add_oncommitted", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicconsumer_remove_oncommitted")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnCommitted(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("itopicconsumer_remove_oncommitted", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicconsumer_add_oncommitting")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnCommitting(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
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
                print("Registering value_converter_func_wrapper in itopicconsumer_add_oncommitting, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO ITopicConsumer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in itopicconsumer_add_oncommitting, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("itopicconsumer_add_oncommitting", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicconsumer_remove_oncommitting")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnCommitting(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("itopicconsumer_remove_oncommitting", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicconsumer_commit")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def Commit(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("itopicconsumer_commit", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicconsumer_add_ondisposed")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnDisposed(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
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
                print("Registering value_converter_func_wrapper in itopicconsumer_add_ondisposed, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO ITopicConsumer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in itopicconsumer_add_ondisposed, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("itopicconsumer_add_ondisposed", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicconsumer_remove_ondisposed")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnDisposed(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("itopicconsumer_remove_ondisposed", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("itopicconsumer_getstatemanager")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetStateManager(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TopicStateManager
        """
        result = InteropUtils.invoke("itopicconsumer_getstatemanager", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
