# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .ITopicConsumer import ITopicConsumer
from .IStreamConsumer import IStreamConsumer
from ..QuixStreamsTelemetry.Models.StreamPackage import StreamPackage
from ..InteropHelpers.InteropUtils import InteropUtils


class PackageReceivedEventArgs(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type PackageReceivedEventArgs
        
        Returns
        ----------
        
        PackageReceivedEventArgs:
            Instance wrapping the .net type PackageReceivedEventArgs
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = PackageReceivedEventArgs._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(PackageReceivedEventArgs, cls).__new__(cls)
            PackageReceivedEventArgs._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type PackageReceivedEventArgs
        
        Returns
        ----------
        
        PackageReceivedEventArgs:
            Instance wrapping the .net type PackageReceivedEventArgs
        """
        if '_PackageReceivedEventArgs_pointer' in dir(self):
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
        del PackageReceivedEventArgs._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("packagereceivedeventargs_constructor")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Constructor(topicConsumer: c_void_p, consumer: c_void_p, package: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        topicConsumer: c_void_p
            GC Handle Pointer to .Net type ITopicConsumer
        
        consumer: c_void_p
            GC Handle Pointer to .Net type IStreamConsumer
        
        package: c_void_p
            GC Handle Pointer to .Net type StreamPackage
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type PackageReceivedEventArgs
        """
        result = InteropUtils.invoke("packagereceivedeventargs_constructor", topicConsumer, consumer, package)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("packagereceivedeventargs_get_topicconsumer")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_TopicConsumer(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ITopicConsumer
        """
        result = InteropUtils.invoke("packagereceivedeventargs_get_topicconsumer", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("packagereceivedeventargs_get_stream")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Stream(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IStreamConsumer
        """
        result = InteropUtils.invoke("packagereceivedeventargs_get_stream", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("packagereceivedeventargs_get_package")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Package(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type StreamPackage
        """
        result = InteropUtils.invoke("packagereceivedeventargs_get_package", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
