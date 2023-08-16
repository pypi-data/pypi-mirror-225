# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...MicrosoftExtensionsLoggingAbstractions.Microsoft.Extensions.Logging.ILoggerFactory import ILoggerFactory
from ...MicrosoftExtensionsLoggingAbstractions.Microsoft.Extensions.Logging.LogLevel import LogLevel
from ...InteropHelpers.InteropUtils import InteropUtils


class Logging(object):
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("logging_createprefixedfactory")
    _interop_func.restype = c_void_p
    @staticmethod
    def CreatePrefixedFactory(prefix: str) -> c_void_p:
        """
        Parameters
        ----------
        
        prefix: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ILoggerFactory
        """
        prefix_ptr = InteropUtils.utf8_to_ptr(prefix)
        
        result = InteropUtils.invoke("logging_createprefixedfactory", prefix_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("logging_updatefactory")
    _interop_func.restype = None
    @staticmethod
    def UpdateFactory(logLevel: LogLevel) -> None:
        """
        Parameters
        ----------
        
        logLevel: LogLevel
            Underlying .Net type is LogLevel
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("logging_updatefactory", logLevel.value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("logging_get_factory")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_Factory() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type ILoggerFactory
        """
        result = InteropUtils.invoke("logging_get_factory")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("logging_set_factory")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def set_Factory(value: c_void_p) -> None:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type ILoggerFactory
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("logging_set_factory", value)
