# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from typing import Callable
from ...InteropHelpers.InteropUtils import InteropUtils


class TelemetryKafkaConsumer(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TelemetryKafkaConsumer
        
        Returns
        ----------
        
        TelemetryKafkaConsumer:
            Instance wrapping the .net type TelemetryKafkaConsumer
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = TelemetryKafkaConsumer._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(TelemetryKafkaConsumer, cls).__new__(cls)
            TelemetryKafkaConsumer._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TelemetryKafkaConsumer
        
        Returns
        ----------
        
        TelemetryKafkaConsumer:
            Instance wrapping the .net type TelemetryKafkaConsumer
        """
        if '_TelemetryKafkaConsumer_pointer' in dir(self):
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
        del TelemetryKafkaConsumer._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("telemetrykafkaconsumer_constructor")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Constructor(telemetryKafkaConsumerConfiguration: c_void_p, topic: str) -> c_void_p:
        """
        Parameters
        ----------
        
        telemetryKafkaConsumerConfiguration: c_void_p
            GC Handle Pointer to .Net type TelemetryKafkaConsumerConfiguration
        
        topic: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TelemetryKafkaConsumer
        """
        topic_ptr = InteropUtils.utf8_to_ptr(topic)
        
        result = InteropUtils.invoke("telemetrykafkaconsumer_constructor", telemetryKafkaConsumerConfiguration, topic_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaconsumer_add_onreceiveexception")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnReceiveException(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler<Exception>
        
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
                print("Registering value_converter_func_wrapper in telemetrykafkaconsumer_add_onreceiveexception, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO TelemetryKafkaConsumer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in telemetrykafkaconsumer_add_onreceiveexception, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("telemetrykafkaconsumer_add_onreceiveexception", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaconsumer_remove_onreceiveexception")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnReceiveException(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("telemetrykafkaconsumer_remove_onreceiveexception", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaconsumer_add_onstreamsrevoked")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnStreamsRevoked(self, value: Callable[[c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p], None]
            Underlying .Net type is Action<IStreamPipeline[]>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type IntPtr
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0: value(c_void_p(p0))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in telemetrykafkaconsumer_add_onstreamsrevoked, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO TelemetryKafkaConsumer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in telemetrykafkaconsumer_add_onstreamsrevoked, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("telemetrykafkaconsumer_add_onstreamsrevoked", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaconsumer_remove_onstreamsrevoked")
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
        InteropUtils.invoke("telemetrykafkaconsumer_remove_onstreamsrevoked", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaconsumer_add_onrevoking")
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
                print("Registering value_converter_func_wrapper in telemetrykafkaconsumer_add_onrevoking, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO TelemetryKafkaConsumer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in telemetrykafkaconsumer_add_onrevoking, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("telemetrykafkaconsumer_add_onrevoking", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaconsumer_remove_onrevoking")
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
        InteropUtils.invoke("telemetrykafkaconsumer_remove_onrevoking", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaconsumer_add_oncommitted")
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
                print("Registering value_converter_func_wrapper in telemetrykafkaconsumer_add_oncommitted, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO TelemetryKafkaConsumer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in telemetrykafkaconsumer_add_oncommitted, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("telemetrykafkaconsumer_add_oncommitted", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaconsumer_remove_oncommitted")
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
        InteropUtils.invoke("telemetrykafkaconsumer_remove_oncommitted", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaconsumer_add_oncommitting")
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
                print("Registering value_converter_func_wrapper in telemetrykafkaconsumer_add_oncommitting, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO TelemetryKafkaConsumer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in telemetrykafkaconsumer_add_oncommitting, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("telemetrykafkaconsumer_add_oncommitting", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaconsumer_remove_oncommitting")
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
        InteropUtils.invoke("telemetrykafkaconsumer_remove_oncommitting", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaconsumer_start")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def Start(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("telemetrykafkaconsumer_start", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaconsumer_foreach")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def ForEach(self, streamPipelineFactoryHandler: Callable[[str], c_void_p]) -> None:
        """
        Parameters
        ----------
        
        streamPipelineFactoryHandler: Callable[[str], c_void_p]
            Underlying .Net type is Func<string, IStreamPipeline>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        streamPipelineFactoryHandler_func_wrapper_addr = None
        if streamPipelineFactoryHandler is not None:
            streamPipelineFactoryHandler_converter = lambda p0: streamPipelineFactoryHandler(str(p0))

            streamPipelineFactoryHandler_converter_func_wrapper = ctypes.CFUNCTYPE(c_void_p, ctypes.c_char_p)(streamPipelineFactoryHandler_converter)
            streamPipelineFactoryHandler_func_wrapper_addr = ctypes.cast(streamPipelineFactoryHandler_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering streamPipelineFactoryHandler_converter_func_wrapper in telemetrykafkaconsumer_foreach, addr {}".format(streamPipelineFactoryHandler_func_wrapper_addr))
                streamPipelineFactoryHandler_func_wrapper_addr_val = streamPipelineFactoryHandler_func_wrapper_addr.value
                # TODO TelemetryKafkaConsumer._weakrefs.append(weakref.ref(streamPipelineFactoryHandler_converter_func_wrapper, lambda x: print("De-referenced streamPipelineFactoryHandler_converter_func_wrapper in telemetrykafkaconsumer_foreach, addr {}".format(streamPipelineFactoryHandler_func_wrapper_addr_val))))
        
        InteropUtils.invoke("telemetrykafkaconsumer_foreach", self._pointer, streamPipelineFactoryHandler_func_wrapper_addr)
        return streamPipelineFactoryHandler_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaconsumer_stop")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def Stop(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("telemetrykafkaconsumer_stop", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaconsumer_dispose")
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
        InteropUtils.invoke("telemetrykafkaconsumer_dispose", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaconsumer_commit")
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
        InteropUtils.invoke("telemetrykafkaconsumer_commit", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("telemetrykafkaconsumer_get_topic")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Topic(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("telemetrykafkaconsumer_get_topic", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
