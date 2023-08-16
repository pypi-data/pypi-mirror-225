# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...InteropHelpers.InteropUtils import InteropUtils


class LeadingEdgeTimestamp(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type LeadingEdgeTimestamp
        
        Returns
        ----------
        
        LeadingEdgeTimestamp:
            Instance wrapping the .net type LeadingEdgeTimestamp
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = LeadingEdgeTimestamp._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(LeadingEdgeTimestamp, cls).__new__(cls)
            LeadingEdgeTimestamp._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type LeadingEdgeTimestamp
        
        Returns
        ----------
        
        LeadingEdgeTimestamp:
            Instance wrapping the .net type LeadingEdgeTimestamp
        """
        if '_LeadingEdgeTimestamp_pointer' in dir(self):
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
        del LeadingEdgeTimestamp._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("leadingedgetimestamp_get_timestamp")
    _interop_func.restype = ctypes.c_longlong
    _interop_func.argtypes = [c_void_p]
    def get_Timestamp(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is long
        """
        result = InteropUtils.invoke("leadingedgetimestamp_get_timestamp", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("leadingedgetimestamp_addvalue")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_double, ctypes.c_ubyte]
    def AddValue(self, parameter: str, value: float, overwrite: bool = False) -> c_void_p:
        """
        Parameters
        ----------
        
        parameter: str
            Underlying .Net type is string
        
        value: float
            Underlying .Net type is double
        
        overwrite: bool
            (Optional) Underlying .Net type is Boolean. Defaults to False
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type LeadingEdgeTimestamp
        """
        parameter_ptr = InteropUtils.utf8_to_ptr(parameter)
        overwrite_bool = 1 if overwrite else 0
        
        result = InteropUtils.invoke("leadingedgetimestamp_addvalue", self._pointer, parameter_ptr, value, overwrite_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("leadingedgetimestamp_addvalue2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p, ctypes.c_ubyte]
    def AddValue2(self, parameter: str, value: str, overwrite: bool = False) -> c_void_p:
        """
        Parameters
        ----------
        
        parameter: str
            Underlying .Net type is string
        
        value: str
            Underlying .Net type is string
        
        overwrite: bool
            (Optional) Underlying .Net type is Boolean. Defaults to False
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type LeadingEdgeTimestamp
        """
        parameter_ptr = InteropUtils.utf8_to_ptr(parameter)
        value_ptr = InteropUtils.utf8_to_ptr(value)
        overwrite_bool = 1 if overwrite else 0
        
        result = InteropUtils.invoke("leadingedgetimestamp_addvalue2", self._pointer, parameter_ptr, value_ptr, overwrite_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("leadingedgetimestamp_addvalue3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p, ctypes.c_ubyte]
    def AddValue3(self, parameter: str, value: c_void_p, overwrite: bool = False) -> c_void_p:
        """
        Parameters
        ----------
        
        parameter: str
            Underlying .Net type is string
        
        value: c_void_p
            GC Handle Pointer to .Net type byte[]
        
        overwrite: bool
            (Optional) Underlying .Net type is Boolean. Defaults to False
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type LeadingEdgeTimestamp
        """
        parameter_ptr = InteropUtils.utf8_to_ptr(parameter)
        overwrite_bool = 1 if overwrite else 0
        
        result = InteropUtils.invoke("leadingedgetimestamp_addvalue3", self._pointer, parameter_ptr, value, overwrite_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("leadingedgetimestamp_get_epochincluded")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_EpochIncluded(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("leadingedgetimestamp_get_epochincluded", self._pointer)
        return result
