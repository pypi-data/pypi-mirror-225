# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .TimeSpan import TimeSpan
from .TypeCode import TypeCode
from ...InteropHelpers.InteropUtils import InteropUtils


class DateTime(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        ----------
        
        DateTime:
            Instance wrapping the .net type DateTime
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = DateTime._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(DateTime, cls).__new__(cls)
            DateTime._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        ----------
        
        DateTime:
            Instance wrapping the .net type DateTime
        """
        if '_DateTime_pointer' in dir(self):
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
        del DateTime._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("datetime_constructor")
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
            GC Handle Pointer to .Net type DateTime
        """
        ticks_long = ctypes.c_longlong(ticks)
        
        result = InteropUtils.invoke("datetime_constructor", ticks_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_constructor5")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor5(year: int, month: int, day: int) -> c_void_p:
        """
        Parameters
        ----------
        
        year: int
            Underlying .Net type is int
        
        month: int
            Underlying .Net type is int
        
        day: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_constructor5", year, month, day)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_constructor8")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor8(year: int, month: int, day: int, hour: int, minute: int, second: int) -> c_void_p:
        """
        Parameters
        ----------
        
        year: int
            Underlying .Net type is int
        
        month: int
            Underlying .Net type is int
        
        day: int
            Underlying .Net type is int
        
        hour: int
            Underlying .Net type is int
        
        minute: int
            Underlying .Net type is int
        
        second: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_constructor8", year, month, day, hour, minute, second)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_constructor11")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor11(year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int) -> c_void_p:
        """
        Parameters
        ----------
        
        year: int
            Underlying .Net type is int
        
        month: int
            Underlying .Net type is int
        
        day: int
            Underlying .Net type is int
        
        hour: int
            Underlying .Net type is int
        
        minute: int
            Underlying .Net type is int
        
        second: int
            Underlying .Net type is int
        
        millisecond: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_constructor11", year, month, day, hour, minute, second, millisecond)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_constructor14")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor14(year: int, month: int, day: int, hour: int, minute: int, second: int, millisecond: int, microsecond: int) -> c_void_p:
        """
        Parameters
        ----------
        
        year: int
            Underlying .Net type is int
        
        month: int
            Underlying .Net type is int
        
        day: int
            Underlying .Net type is int
        
        hour: int
            Underlying .Net type is int
        
        minute: int
            Underlying .Net type is int
        
        second: int
            Underlying .Net type is int
        
        millisecond: int
            Underlying .Net type is int
        
        microsecond: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_constructor14", year, month, day, hour, minute, second, millisecond, microsecond)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_add")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Add(self, value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_add", self._pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_adddays")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_double]
    def AddDays(self, value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_adddays", self._pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_addhours")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_double]
    def AddHours(self, value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_addhours", self._pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_addmilliseconds")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_double]
    def AddMilliseconds(self, value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_addmilliseconds", self._pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_addmicroseconds")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_double]
    def AddMicroseconds(self, value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_addmicroseconds", self._pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_addminutes")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_double]
    def AddMinutes(self, value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_addminutes", self._pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_addmonths")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_int]
    def AddMonths(self, months: int) -> c_void_p:
        """
        Parameters
        ----------
        
        months: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_addmonths", self._pointer, months)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_addseconds")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_double]
    def AddSeconds(self, value: float) -> c_void_p:
        """
        Parameters
        ----------
        
        value: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_addseconds", self._pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_addticks")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_longlong]
    def AddTicks(self, value: int) -> c_void_p:
        """
        Parameters
        ----------
        
        value: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        value_long = ctypes.c_longlong(value)
        
        result = InteropUtils.invoke("datetime_addticks", self._pointer, value_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_addyears")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_int]
    def AddYears(self, value: int) -> c_void_p:
        """
        Parameters
        ----------
        
        value: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_addyears", self._pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_compare")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Compare(t1: c_void_p, t2: c_void_p) -> int:
        """
        Parameters
        ----------
        
        t1: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        t2: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_compare", t1, t2)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_compareto")
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
        result = InteropUtils.invoke("datetime_compareto", self._pointer, value)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_compareto2")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p, c_void_p]
    def CompareTo2(self, value: c_void_p) -> int:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_compareto2", self._pointer, value)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_daysinmonth")
    _interop_func.restype = ctypes.c_int
    @staticmethod
    def DaysInMonth(year: int, month: int) -> int:
        """
        Parameters
        ----------
        
        year: int
            Underlying .Net type is int
        
        month: int
            Underlying .Net type is int
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_daysinmonth", year, month)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_equals")
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
        result = InteropUtils.invoke("datetime_equals", self._pointer, value)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_equals2")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Equals2(self, value: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("datetime_equals2", self._pointer, value)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_equals3")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Equals3(t1: c_void_p, t2: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        t1: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        t2: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("datetime_equals3", t1, t2)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_frombinary")
    _interop_func.restype = c_void_p
    @staticmethod
    def FromBinary(dateData: int) -> c_void_p:
        """
        Parameters
        ----------
        
        dateData: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        dateData_long = ctypes.c_longlong(dateData)
        
        result = InteropUtils.invoke("datetime_frombinary", dateData_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_fromfiletime")
    _interop_func.restype = c_void_p
    @staticmethod
    def FromFileTime(fileTime: int) -> c_void_p:
        """
        Parameters
        ----------
        
        fileTime: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        fileTime_long = ctypes.c_longlong(fileTime)
        
        result = InteropUtils.invoke("datetime_fromfiletime", fileTime_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_fromfiletimeutc")
    _interop_func.restype = c_void_p
    @staticmethod
    def FromFileTimeUtc(fileTime: int) -> c_void_p:
        """
        Parameters
        ----------
        
        fileTime: int
            Underlying .Net type is long
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        fileTime_long = ctypes.c_longlong(fileTime)
        
        result = InteropUtils.invoke("datetime_fromfiletimeutc", fileTime_long)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_fromoadate")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [ctypes.c_double]
    @staticmethod
    def FromOADate(d: float) -> c_void_p:
        """
        Parameters
        ----------
        
        d: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_fromoadate", d)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_isdaylightsavingtime")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def IsDaylightSavingTime(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("datetime_isdaylightsavingtime", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_tobinary")
    _interop_func.restype = ctypes.c_longlong
    _interop_func.argtypes = [c_void_p]
    def ToBinary(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("datetime_tobinary", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_date")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Date(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_get_date", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_day")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Day(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_day", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_dayofyear")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_DayOfYear(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_dayofyear", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_gethashcode")
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
        result = InteropUtils.invoke("datetime_gethashcode", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_hour")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Hour(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_hour", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_millisecond")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Millisecond(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_millisecond", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_microsecond")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Microsecond(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_microsecond", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_nanosecond")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Nanosecond(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_nanosecond", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_minute")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Minute(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_minute", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_month")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Month(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_month", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_now")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_Now() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_get_now")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_second")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Second(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_second", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_ticks")
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
        result = InteropUtils.invoke("datetime_get_ticks", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_timeofday")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_TimeOfDay(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("datetime_get_timeofday", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_today")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_Today() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_get_today")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_year")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Year(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("datetime_get_year", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_isleapyear")
    _interop_func.restype = ctypes.c_ubyte
    @staticmethod
    def IsLeapYear(year: int) -> bool:
        """
        Parameters
        ----------
        
        year: int
            Underlying .Net type is int
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("datetime_isleapyear", year)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_parse")
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
            GC Handle Pointer to .Net type DateTime
        """
        s_ptr = InteropUtils.utf8_to_ptr(s)
        
        result = InteropUtils.invoke("datetime_parse", s_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_parse2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Parse2(s: str, provider: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        s: str
            Underlying .Net type is string
        
        provider: c_void_p
            GC Handle Pointer to .Net type IFormatProvider
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        s_ptr = InteropUtils.utf8_to_ptr(s)
        
        result = InteropUtils.invoke("datetime_parse2", s_ptr, provider)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_parseexact")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def ParseExact(s: str, format: str, provider: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        s: str
            Underlying .Net type is string
        
        format: str
            Underlying .Net type is string
        
        provider: c_void_p
            GC Handle Pointer to .Net type IFormatProvider
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        s_ptr = InteropUtils.utf8_to_ptr(s)
        format_ptr = InteropUtils.utf8_to_ptr(format)
        
        result = InteropUtils.invoke("datetime_parseexact", s_ptr, format_ptr, provider)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_subtract")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Subtract(self, value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type TimeSpan
        """
        result = InteropUtils.invoke("datetime_subtract", self._pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_subtract2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Subtract2(self, value: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_subtract2", self._pointer, value)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_tooadate")
    _interop_func.restype = ctypes.c_double
    _interop_func.argtypes = [c_void_p]
    def ToOADate(self) -> float:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        float:
            Underlying .Net type is double
        """
        result = InteropUtils.invoke("datetime_tooadate", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_tofiletime")
    _interop_func.restype = ctypes.c_longlong
    _interop_func.argtypes = [c_void_p]
    def ToFileTime(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("datetime_tofiletime", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_tofiletimeutc")
    _interop_func.restype = ctypes.c_longlong
    _interop_func.argtypes = [c_void_p]
    def ToFileTimeUtc(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("datetime_tofiletimeutc", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_tolocaltime")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def ToLocalTime(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_tolocaltime", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_tolongdatestring")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def ToLongDateString(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("datetime_tolongdatestring", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_tolongtimestring")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def ToLongTimeString(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("datetime_tolongtimestring", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_toshortdatestring")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def ToShortDateString(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("datetime_toshortdatestring", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_toshorttimestring")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def ToShortTimeString(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("datetime_toshorttimestring", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_tostring")
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
        result = InteropUtils.invoke("datetime_tostring", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_tostring2")
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
        
        result = InteropUtils.invoke("datetime_tostring2", self._pointer, format_ptr)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_tostring3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def ToString3(self, provider: c_void_p) -> str:
        """
        Parameters
        ----------
        
        provider: c_void_p
            GC Handle Pointer to .Net type IFormatProvider
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("datetime_tostring3", self._pointer, provider)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_tostring4")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def ToString4(self, format: str, provider: c_void_p) -> str:
        """
        Parameters
        ----------
        
        format: str
            Underlying .Net type is string
        
        provider: c_void_p
            GC Handle Pointer to .Net type IFormatProvider
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        format_ptr = InteropUtils.utf8_to_ptr(format)
        
        result = InteropUtils.invoke("datetime_tostring4", self._pointer, format_ptr, provider)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_touniversaltime")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def ToUniversalTime(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_touniversaltime", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_tryparse")
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
            GC Handle Pointer to .Net type DateTime&
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        s_ptr = InteropUtils.utf8_to_ptr(s)
        
        result2 = InteropUtils.invoke("datetime_tryparse", s_ptr, result)
        return result2
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_op_equality")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Equality(d1: c_void_p, d2: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        d1: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        d2: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("datetime_op_equality", d1, d2)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_op_inequality")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Inequality(d1: c_void_p, d2: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        d1: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        d2: c_void_p
            GC Handle Pointer to .Net type DateTime
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("datetime_op_inequality", d1, d2)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_deconstruct2")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
    def Deconstruct2(self, year: c_void_p, month: c_void_p, day: c_void_p) -> None:
        """
        Parameters
        ----------
        
        year: c_void_p
            GC Handle Pointer to .Net type Int32&
        
        month: c_void_p
            GC Handle Pointer to .Net type Int32&
        
        day: c_void_p
            GC Handle Pointer to .Net type Int32&
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("datetime_deconstruct2", self._pointer, year, month, day)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_getdatetimeformats")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetDateTimeFormats(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type string[]
        """
        result = InteropUtils.invoke("datetime_getdatetimeformats", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_getdatetimeformats2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def GetDateTimeFormats2(self, provider: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        provider: c_void_p
            GC Handle Pointer to .Net type IFormatProvider
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type string[]
        """
        result = InteropUtils.invoke("datetime_getdatetimeformats2", self._pointer, provider)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_gettypecode")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def GetTypeCode(self) -> TypeCode:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        TypeCode:
            Underlying .Net type is TypeCode
        """
        result = InteropUtils.invoke("datetime_gettypecode", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_tryparse5")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def TryParse5(s: str, provider: c_void_p, result: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        s: str
            Underlying .Net type is string
        
        provider: c_void_p
            GC Handle Pointer to .Net type IFormatProvider
        
        result: c_void_p
            GC Handle Pointer to .Net type DateTime&
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        s_ptr = InteropUtils.utf8_to_ptr(s)
        
        result2 = InteropUtils.invoke("datetime_tryparse5", s_ptr, provider, result)
        return result2
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_utcnow")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UtcNow() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_get_utcnow")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_minvalue")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_MinValue() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_get_minvalue")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_maxvalue")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_MaxValue() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_get_maxvalue")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("datetime_get_unixepoch")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_UnixEpoch() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type DateTime
        """
        result = InteropUtils.invoke("datetime_get_unixepoch")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
