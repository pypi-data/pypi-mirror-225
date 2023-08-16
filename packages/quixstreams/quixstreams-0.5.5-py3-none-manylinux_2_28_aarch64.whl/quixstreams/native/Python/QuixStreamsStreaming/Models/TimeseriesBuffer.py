# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from typing import Callable
from .TimeseriesDataTimestamp import TimeseriesDataTimestamp
from .TimeseriesData import TimeseriesData
from ...InteropHelpers.InteropUtils import InteropUtils


class TimeseriesBuffer(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TimeseriesBuffer
        
        Returns
        ----------
        
        TimeseriesBuffer:
            Instance wrapping the .net type TimeseriesBuffer
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = TimeseriesBuffer._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(TimeseriesBuffer, cls).__new__(cls)
            TimeseriesBuffer._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type TimeseriesBuffer
        
        Returns
        ----------
        
        TimeseriesBuffer:
            Instance wrapping the .net type TimeseriesBuffer
        """
        if '_TimeseriesBuffer_pointer' in dir(self):
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
        del TimeseriesBuffer._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("timeseriesbuffer_add_ondatareleased")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnDataReleased(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler<TimeseriesDataReadEventArgs>
        
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
                print("Registering value_converter_func_wrapper in timeseriesbuffer_add_ondatareleased, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO TimeseriesBuffer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in timeseriesbuffer_add_ondatareleased, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("timeseriesbuffer_add_ondatareleased", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_remove_ondatareleased")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnDataReleased(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("timeseriesbuffer_remove_ondatareleased", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_add_onrawreleased")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def add_OnRawReleased(self, value: Callable[[c_void_p, c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is EventHandler<TimeseriesDataRawReadEventArgs>
        
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
                print("Registering value_converter_func_wrapper in timeseriesbuffer_add_onrawreleased, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO TimeseriesBuffer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in timeseriesbuffer_add_onrawreleased, addr {}".format(value_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("timeseriesbuffer_add_onrawreleased", self._pointer, value_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_remove_onrawreleased")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def remove_OnRawReleased(self, value: c_void_p) -> None:
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
        InteropUtils.invoke("timeseriesbuffer_remove_onrawreleased", self._pointer, value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_get_packetsize")
    _interop_func.restype = InteropUtils.create_nullable(ctypes.c_int)
    _interop_func.argtypes = [c_void_p]
    def get_PacketSize(self) -> Optional[int]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[int]:
            Underlying .Net type is int?
        """
        result = InteropUtils.invoke("timeseriesbuffer_get_packetsize", self._pointer)
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_set_packetsize")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, InteropUtils.create_nullable(ctypes.c_int)]
    def set_PacketSize(self, value: Optional[int]) -> None:
        """
        Parameters
        ----------
        
        value: Optional[int]
            Underlying .Net type is int?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_nullable = InteropUtils.create_nullable(ctypes.c_int)(value)
        
        InteropUtils.invoke("timeseriesbuffer_set_packetsize", self._pointer, value_nullable)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_get_buffertimeout")
    _interop_func.restype = InteropUtils.create_nullable(ctypes.c_int)
    _interop_func.argtypes = [c_void_p]
    def get_BufferTimeout(self) -> Optional[int]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[int]:
            Underlying .Net type is int?
        """
        result = InteropUtils.invoke("timeseriesbuffer_get_buffertimeout", self._pointer)
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_set_buffertimeout")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, InteropUtils.create_nullable(ctypes.c_int)]
    def set_BufferTimeout(self, value: Optional[int]) -> None:
        """
        Parameters
        ----------
        
        value: Optional[int]
            Underlying .Net type is int?
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_nullable = InteropUtils.create_nullable(ctypes.c_int)(value)
        
        InteropUtils.invoke("timeseriesbuffer_set_buffertimeout", self._pointer, value_nullable)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_get_timespaninnanoseconds")
    _interop_func.restype = InteropUtils.create_nullable(ctypes.c_longlong)
    _interop_func.argtypes = [c_void_p]
    def get_TimeSpanInNanoseconds(self) -> Optional[int]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[int]:
            Underlying .Net type is long?
        """
        result = InteropUtils.invoke("timeseriesbuffer_get_timespaninnanoseconds", self._pointer)
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_set_timespaninnanoseconds")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, InteropUtils.create_nullable(ctypes.c_longlong)]
    def set_TimeSpanInNanoseconds(self, value: Optional[int]) -> None:
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
        
        InteropUtils.invoke("timeseriesbuffer_set_timespaninnanoseconds", self._pointer, value_nullable)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_get_timespaninmilliseconds")
    _interop_func.restype = InteropUtils.create_nullable(ctypes.c_longlong)
    _interop_func.argtypes = [c_void_p]
    def get_TimeSpanInMilliseconds(self) -> Optional[int]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[int]:
            Underlying .Net type is long?
        """
        result = InteropUtils.invoke("timeseriesbuffer_get_timespaninmilliseconds", self._pointer)
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_set_timespaninmilliseconds")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, InteropUtils.create_nullable(ctypes.c_longlong)]
    def set_TimeSpanInMilliseconds(self, value: Optional[int]) -> None:
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
        
        InteropUtils.invoke("timeseriesbuffer_set_timespaninmilliseconds", self._pointer, value_nullable)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_get_filter")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Filter(self) -> Callable[[c_void_p], bool]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Callable[[c_void_p], bool]:
            Underlying .Net type is Func<TimeseriesDataTimestamp, Boolean>
        """
        result = InteropUtils.invoke("timeseriesbuffer_get_filter", self._pointer)
        return Exception("NOT IMPLEMENTED YET")
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_set_filter")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_Filter(self, value: Callable[[c_void_p], bool]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p], bool]
            Underlying .Net type is Func<TimeseriesDataTimestamp, Boolean>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0: value(c_void_p(p0))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(ctypes.c_bool, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in timeseriesbuffer_set_filter, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO TimeseriesBuffer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in timeseriesbuffer_set_filter, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("timeseriesbuffer_set_filter", self._pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_get_customtriggerbeforeenqueue")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_CustomTriggerBeforeEnqueue(self) -> Callable[[c_void_p], bool]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Callable[[c_void_p], bool]:
            Underlying .Net type is Func<TimeseriesDataTimestamp, Boolean>
        """
        result = InteropUtils.invoke("timeseriesbuffer_get_customtriggerbeforeenqueue", self._pointer)
        return Exception("NOT IMPLEMENTED YET")
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_set_customtriggerbeforeenqueue")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_CustomTriggerBeforeEnqueue(self, value: Callable[[c_void_p], bool]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p], bool]
            Underlying .Net type is Func<TimeseriesDataTimestamp, Boolean>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0: value(c_void_p(p0))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(ctypes.c_bool, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in timeseriesbuffer_set_customtriggerbeforeenqueue, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO TimeseriesBuffer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in timeseriesbuffer_set_customtriggerbeforeenqueue, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("timeseriesbuffer_set_customtriggerbeforeenqueue", self._pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_get_customtrigger")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_CustomTrigger(self) -> Callable[[c_void_p], bool]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Callable[[c_void_p], bool]:
            Underlying .Net type is Func<TimeseriesData, Boolean>
        """
        result = InteropUtils.invoke("timeseriesbuffer_get_customtrigger", self._pointer)
        return Exception("NOT IMPLEMENTED YET")
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_set_customtrigger")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def set_CustomTrigger(self, value: Callable[[c_void_p], bool]) -> None:
        """
        Parameters
        ----------
        
        value: Callable[[c_void_p], bool]
            Underlying .Net type is Func<TimeseriesData, Boolean>
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        value_func_wrapper_addr = None
        if value is not None:
            value_converter = lambda p0: value(c_void_p(p0))

            value_converter_func_wrapper = ctypes.CFUNCTYPE(ctypes.c_bool, c_void_p)(value_converter)
            value_func_wrapper_addr = ctypes.cast(value_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering value_converter_func_wrapper in timeseriesbuffer_set_customtrigger, addr {}".format(value_func_wrapper_addr))
                value_func_wrapper_addr_val = value_func_wrapper_addr.value
                # TODO TimeseriesBuffer._weakrefs.append(weakref.ref(value_converter_func_wrapper, lambda x: print("De-referenced value_converter_func_wrapper in timeseriesbuffer_set_customtrigger, addr {}".format(value_func_wrapper_addr_val))))
        
        InteropUtils.invoke("timeseriesbuffer_set_customtrigger", self._pointer, value_func_wrapper_addr)
        return value_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timeseriesbuffer_dispose")
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
        InteropUtils.invoke("timeseriesbuffer_dispose", self._pointer)
