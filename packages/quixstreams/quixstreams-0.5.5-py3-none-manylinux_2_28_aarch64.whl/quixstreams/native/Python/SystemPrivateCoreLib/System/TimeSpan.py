# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...InteropHelpers.InteropUtils import InteropUtils


class TimeSpan(object):
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            Pointer to .Net type TimeSpan in memory as bytes
        
        Returns
        ----------
        
        TimeSpan:
            Instance wrapping the .net type TimeSpan
        """
        
        self._pointer = net_pointer
        
        if finalize:
            self._finalizer = weakref.finalize(self, self._finalizerfunc)
            self._finalizer.atexit = False
        else:
            self._finalizer = lambda: None
    
    def _finalizerfunc(self):
        InteropUtils.free_uptr(self._pointer)
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
    _interop_func = InteropUtils.get_function("timespan_constructor")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor(ticks: int) -> c_void_p:
        """
        Parameters
        ----------
        
        ticks: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        ticks_long = ctypes.c_longlong(ticks)
        
        result = InteropUtils.invoke("timespan_constructor", ticks_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_constructor2")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor2(hours: int, minutes: int, seconds: int) -> c_void_p:
        """
        Parameters
        ----------
        
        hours: int
            Underlying .Net type is int
        
        minutes: int
            Underlying .Net type is int
        
        seconds: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_constructor2", hours, minutes, seconds)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_constructor3")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor3(days: int, hours: int, minutes: int, seconds: int) -> c_void_p:
        """
        Parameters
        ----------
        
        days: int
            Underlying .Net type is int
        
        hours: int
            Underlying .Net type is int
        
        minutes: int
            Underlying .Net type is int
        
        seconds: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_constructor3", days, hours, minutes, seconds)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_constructor4")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor4(days: int, hours: int, minutes: int, seconds: int, milliseconds: int) -> c_void_p:
        """
        Parameters
        ----------
        
        days: int
            Underlying .Net type is int
        
        hours: int
            Underlying .Net type is int
        
        minutes: int
            Underlying .Net type is int
        
        seconds: int
            Underlying .Net type is int
        
        milliseconds: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_constructor4", days, hours, minutes, seconds, milliseconds)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_constructor5")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor5(days: int, hours: int, minutes: int, seconds: int, milliseconds: int, microseconds: int) -> c_void_p:
        """
        Parameters
        ----------
        
        days: int
            Underlying .Net type is int
        
        hours: int
            Underlying .Net type is int
        
        minutes: int
            Underlying .Net type is int
        
        seconds: int
            Underlying .Net type is int
        
        milliseconds: int
            Underlying .Net type is int
        
        microseconds: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_constructor5", days, hours, minutes, seconds, milliseconds, microseconds)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_ticks")
    _interop_func.restype = ctypes.c_longlong
    _interop_func.argtypes = [c_void_p]
    def get_Ticks(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("timespan_get_ticks", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_days")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Days(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_get_days", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_hours")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Hours(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_get_hours", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_milliseconds")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Milliseconds(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_get_milliseconds", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_microseconds")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Microseconds(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_get_microseconds", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_nanoseconds")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Nanoseconds(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_get_nanoseconds", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_minutes")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Minutes(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_get_minutes", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_seconds")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Seconds(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_get_seconds", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_totaldays")
    _interop_func.restype = ctypes.c_double
    _interop_func.argtypes = [c_void_p]
    def get_TotalDays(self) -> float:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("timespan_get_totaldays", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_totalhours")
    _interop_func.restype = ctypes.c_double
    _interop_func.argtypes = [c_void_p]
    def get_TotalHours(self) -> float:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("timespan_get_totalhours", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_totalmilliseconds")
    _interop_func.restype = ctypes.c_double
    _interop_func.argtypes = [c_void_p]
    def get_TotalMilliseconds(self) -> float:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("timespan_get_totalmilliseconds", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_totalmicroseconds")
    _interop_func.restype = ctypes.c_double
    _interop_func.argtypes = [c_void_p]
    def get_TotalMicroseconds(self) -> float:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("timespan_get_totalmicroseconds", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_totalnanoseconds")
    _interop_func.restype = ctypes.c_double
    _interop_func.argtypes = [c_void_p]
    def get_TotalNanoseconds(self) -> float:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("timespan_get_totalnanoseconds", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_totalminutes")
    _interop_func.restype = ctypes.c_double
    _interop_func.argtypes = [c_void_p]
    def get_TotalMinutes(self) -> float:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("timespan_get_totalminutes", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_totalseconds")
    _interop_func.restype = ctypes.c_double
    _interop_func.argtypes = [c_void_p]
    def get_TotalSeconds(self) -> float:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("timespan_get_totalseconds", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_add")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Add(self, ts: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        ts: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_add", self._pointer, ts)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_compare")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Compare(t1: c_void_p, t2: c_void_p) -> int:
        """
        Parameters
        ----------
        
        t1: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        t2: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_compare", t1, t2)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_compareto")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p, c_void_p]
    def CompareTo(self, value: c_void_p) -> int:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_compareto", self._pointer, value)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_compareto2")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p, c_void_p]
    def CompareTo2(self, value: c_void_p) -> int:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_compareto2", self._pointer, value)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_fromdays")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [ctypes.c_double]
    @staticmethod
    def FromDays(value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_fromdays", value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_duration")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def Duration(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_duration", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_equals")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Equals(self, value: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("timespan_equals", self._pointer, value)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_equals2")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Equals2(self, obj: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        obj: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("timespan_equals2", self._pointer, obj)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_equals3")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Equals3(t1: c_void_p, t2: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        t1: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        t2: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("timespan_equals3", t1, t2)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_gethashcode")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def GetHashCode(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("timespan_gethashcode", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_fromhours")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [ctypes.c_double]
    @staticmethod
    def FromHours(value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_fromhours", value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_frommilliseconds")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [ctypes.c_double]
    @staticmethod
    def FromMilliseconds(value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_frommilliseconds", value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_frommicroseconds")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [ctypes.c_double]
    @staticmethod
    def FromMicroseconds(value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_frommicroseconds", value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_fromminutes")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [ctypes.c_double]
    @staticmethod
    def FromMinutes(value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_fromminutes", value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_negate")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def Negate(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_negate", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_fromseconds")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [ctypes.c_double]
    @staticmethod
    def FromSeconds(value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_fromseconds", value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_subtract")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Subtract(self, ts: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        ts: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_subtract", self._pointer, ts)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_multiply")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_double]
    def Multiply(self, factor: float) -> c_void_p:
        """
        Parameters
        ----------
        
        factor: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_multiply", self._pointer, factor)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_divide")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_double]
    def Divide(self, divisor: float) -> c_void_p:
        """
        Parameters
        ----------
        
        divisor: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_divide", self._pointer, divisor)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_divide2")
    _interop_func.restype = ctypes.c_double
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Divide2(self, ts: c_void_p) -> float:
        """
        Parameters
        ----------
        
        ts: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("timespan_divide2", self._pointer, ts)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_fromticks")
    _interop_func.restype = c_void_p
    @staticmethod
    def FromTicks(value: int) -> c_void_p:
        """
        Parameters
        ----------
        
        value: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        value_long = ctypes.c_longlong(value)
        
        result = InteropUtils.invoke("timespan_fromticks", value_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_parse")
    _interop_func.restype = c_void_p
    @staticmethod
    def Parse(s: str) -> c_void_p:
        """
        Parameters
        ----------
        
        s: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        s_ptr = InteropUtils.utf8_to_ptr(s)
        
        result = InteropUtils.invoke("timespan_parse", s_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_parse2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Parse2(input: str, formatProvider: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        input: str
            Underlying .Net type is string
        
        formatProvider: c_void_p
            GC Handle Pointer to .Net type IFormatProvider
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        input_ptr = InteropUtils.utf8_to_ptr(input)
        
        result = InteropUtils.invoke("timespan_parse2", input_ptr, formatProvider)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_parseexact")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def ParseExact(input: str, format: str, formatProvider: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        input: str
            Underlying .Net type is string
        
        format: str
            Underlying .Net type is string
        
        formatProvider: c_void_p
            GC Handle Pointer to .Net type IFormatProvider
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        input_ptr = InteropUtils.utf8_to_ptr(input)
        format_ptr = InteropUtils.utf8_to_ptr(format)
        
        result = InteropUtils.invoke("timespan_parseexact", input_ptr, format_ptr, formatProvider)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_parseexact2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def ParseExact2(input: str, formats: c_void_p, formatProvider: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        input: str
            Underlying .Net type is string
        
        formats: c_void_p
            GC Handle Pointer to .Net type string[]
        
        formatProvider: c_void_p
            GC Handle Pointer to .Net type IFormatProvider
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        input_ptr = InteropUtils.utf8_to_ptr(input)
        
        result = InteropUtils.invoke("timespan_parseexact2", input_ptr, formats, formatProvider)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_tryparse")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def TryParse(s: str, result: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        s: str
            Underlying .Net type is string
        
        result: c_void_p
            GC Handle Pointer to .Net type TimeSpan&
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        s_ptr = InteropUtils.utf8_to_ptr(s)
        
        result2 = InteropUtils.invoke("timespan_tryparse", s_ptr, result)
        return result2
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_tryparse3")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def TryParse3(input: str, formatProvider: c_void_p, result: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        input: str
            Underlying .Net type is string
        
        formatProvider: c_void_p
            GC Handle Pointer to .Net type IFormatProvider
        
        result: c_void_p
            GC Handle Pointer to .Net type TimeSpan&
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        input_ptr = InteropUtils.utf8_to_ptr(input)
        
        result2 = InteropUtils.invoke("timespan_tryparse3", input_ptr, formatProvider, result)
        return result2
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_tryparseexact")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
    @staticmethod
    def TryParseExact(input: str, format: str, formatProvider: c_void_p, result: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        input: str
            Underlying .Net type is string
        
        format: str
            Underlying .Net type is string
        
        formatProvider: c_void_p
            GC Handle Pointer to .Net type IFormatProvider
        
        result: c_void_p
            GC Handle Pointer to .Net type TimeSpan&
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        input_ptr = InteropUtils.utf8_to_ptr(input)
        format_ptr = InteropUtils.utf8_to_ptr(format)
        
        result2 = InteropUtils.invoke("timespan_tryparseexact", input_ptr, format_ptr, formatProvider, result)
        return result2
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_tryparseexact3")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
    @staticmethod
    def TryParseExact3(input: str, formats: c_void_p, formatProvider: c_void_p, result: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        input: str
            Underlying .Net type is string
        
        formats: c_void_p
            GC Handle Pointer to .Net type string[]
        
        formatProvider: c_void_p
            GC Handle Pointer to .Net type IFormatProvider
        
        result: c_void_p
            GC Handle Pointer to .Net type TimeSpan&
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        input_ptr = InteropUtils.utf8_to_ptr(input)
        
        result2 = InteropUtils.invoke("timespan_tryparseexact3", input_ptr, formats, formatProvider, result)
        return result2
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_tostring")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def ToString(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("timespan_tostring", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_tostring2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def ToString2(self, format: str) -> str:
        """
        Parameters
        ----------
        
        format: str
            Underlying .Net type is string
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        format_ptr = InteropUtils.utf8_to_ptr(format)
        
        result = InteropUtils.invoke("timespan_tostring2", self._pointer, format_ptr)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_tostring3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def ToString3(self, format: str, formatProvider: c_void_p) -> str:
        """
        Parameters
        ----------
        
        format: str
            Underlying .Net type is string
        
        formatProvider: c_void_p
            GC Handle Pointer to .Net type IFormatProvider
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        format_ptr = InteropUtils.utf8_to_ptr(format)
        
        result = InteropUtils.invoke("timespan_tostring3", self._pointer, format_ptr, formatProvider)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_op_equality")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Equality(t1: c_void_p, t2: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        t1: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        t2: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("timespan_op_equality", t1, t2)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_op_inequality")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Inequality(t1: c_void_p, t2: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        t1: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        t2: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("timespan_op_inequality", t1, t2)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_zero")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_Zero() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_get_zero")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_maxvalue")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_MaxValue() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_get_maxvalue")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_minvalue")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_MinValue() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("timespan_get_minvalue")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_nanosecondspertick")
    _interop_func.restype = ctypes.c_longlong
    @staticmethod
    def get_NanosecondsPerTick() -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("timespan_get_nanosecondspertick")
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_tickspermicrosecond")
    _interop_func.restype = ctypes.c_longlong
    @staticmethod
    def get_TicksPerMicrosecond() -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("timespan_get_tickspermicrosecond")
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_tickspermillisecond")
    _interop_func.restype = ctypes.c_longlong
    @staticmethod
    def get_TicksPerMillisecond() -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("timespan_get_tickspermillisecond")
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_tickspersecond")
    _interop_func.restype = ctypes.c_longlong
    @staticmethod
    def get_TicksPerSecond() -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("timespan_get_tickspersecond")
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_ticksperminute")
    _interop_func.restype = ctypes.c_longlong
    @staticmethod
    def get_TicksPerMinute() -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("timespan_get_ticksperminute")
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_ticksperhour")
    _interop_func.restype = ctypes.c_longlong
    @staticmethod
    def get_TicksPerHour() -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("timespan_get_ticksperhour")
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("timespan_get_ticksperday")
    _interop_func.restype = ctypes.c_longlong
    @staticmethod
    def get_TicksPerDay() -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("timespan_get_ticksperday")
        return result
