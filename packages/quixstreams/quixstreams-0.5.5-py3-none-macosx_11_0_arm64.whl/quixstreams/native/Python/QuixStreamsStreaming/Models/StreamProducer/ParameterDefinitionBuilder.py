# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ....InteropHelpers.InteropUtils import InteropUtils


class ParameterDefinitionBuilder(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterDefinitionBuilder
        
        Returns
        ----------
        
        ParameterDefinitionBuilder:
            Instance wrapping the .net type ParameterDefinitionBuilder
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = ParameterDefinitionBuilder._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(ParameterDefinitionBuilder, cls).__new__(cls)
            ParameterDefinitionBuilder._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type ParameterDefinitionBuilder
        
        Returns
        ----------
        
        ParameterDefinitionBuilder:
            Instance wrapping the .net type ParameterDefinitionBuilder
        """
        if '_ParameterDefinitionBuilder_pointer' in dir(self):
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
        del ParameterDefinitionBuilder._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("parameterdefinitionbuilder_constructor")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Constructor(streamTimeseriesProducer: c_void_p, location: str, definition: c_void_p = None) -> c_void_p:
        """
        Parameters
        ----------
        
        streamTimeseriesProducer: c_void_p
            GC Handle Pointer to .Net type StreamTimeseriesProducer
        
        location: str
            Underlying .Net type is string
        
        definition: c_void_p
            (Optional) GC Handle Pointer to .Net type ParameterDefinition. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDefinitionBuilder
        """
        location_ptr = InteropUtils.utf8_to_ptr(location)
        
        result = InteropUtils.invoke("parameterdefinitionbuilder_constructor", streamTimeseriesProducer, location_ptr, definition)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parameterdefinitionbuilder_setrange")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_double, ctypes.c_double]
    def SetRange(self, minimumValue: float, maximumValue: float) -> c_void_p:
        """
        Parameters
        ----------
        
        minimumValue: float
            Underlying .Net type is double
        
        maximumValue: float
            Underlying .Net type is double
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDefinitionBuilder
        """
        result = InteropUtils.invoke("parameterdefinitionbuilder_setrange", self._pointer, minimumValue, maximumValue)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parameterdefinitionbuilder_setunit")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def SetUnit(self, unit: str) -> c_void_p:
        """
        Parameters
        ----------
        
        unit: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDefinitionBuilder
        """
        unit_ptr = InteropUtils.utf8_to_ptr(unit)
        
        result = InteropUtils.invoke("parameterdefinitionbuilder_setunit", self._pointer, unit_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parameterdefinitionbuilder_setformat")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def SetFormat(self, format: str) -> c_void_p:
        """
        Parameters
        ----------
        
        format: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDefinitionBuilder
        """
        format_ptr = InteropUtils.utf8_to_ptr(format)
        
        result = InteropUtils.invoke("parameterdefinitionbuilder_setformat", self._pointer, format_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parameterdefinitionbuilder_setcustomproperties")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def SetCustomProperties(self, customProperties: str) -> c_void_p:
        """
        Parameters
        ----------
        
        customProperties: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDefinitionBuilder
        """
        customProperties_ptr = InteropUtils.utf8_to_ptr(customProperties)
        
        result = InteropUtils.invoke("parameterdefinitionbuilder_setcustomproperties", self._pointer, customProperties_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("parameterdefinitionbuilder_adddefinition")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
    def AddDefinition(self, parameterId: str, name: str = None, description: str = None) -> c_void_p:
        """
        Parameters
        ----------
        
        parameterId: str
            Underlying .Net type is string
        
        name: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        description: str
            (Optional) Underlying .Net type is string. Defaults to None
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ParameterDefinitionBuilder
        """
        parameterId_ptr = InteropUtils.utf8_to_ptr(parameterId)
        name_ptr = InteropUtils.utf8_to_ptr(name)
        description_ptr = InteropUtils.utf8_to_ptr(description)
        
        result = InteropUtils.invoke("parameterdefinitionbuilder_adddefinition", self._pointer, parameterId_ptr, name_ptr, description_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
