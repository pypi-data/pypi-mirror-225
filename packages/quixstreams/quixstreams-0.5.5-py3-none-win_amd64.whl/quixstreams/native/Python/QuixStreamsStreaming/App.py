# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from typing import Callable
from .States.AppStateManager import AppStateManager
from ..InteropHelpers.InteropUtils import InteropUtils


class App(object):
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("app_run")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Run(cancellationToken: c_void_p = None, beforeShutdown: Callable[[], None] = None) -> None:
        """
        Parameters
        ----------
        
        cancellationToken: c_void_p
            (Optional) GC Handle Pointer to .Net type CancellationToken. Defaults to None
        
        beforeShutdown: Callable[[], None]
            (Optional) Underlying .Net type is Action. Defaults to None
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        beforeShutdown_func_wrapper_addr = None
        if beforeShutdown is not None:
            beforeShutdown_converter = lambda : beforeShutdown()

            beforeShutdown_converter_func_wrapper = ctypes.CFUNCTYPE(None)(beforeShutdown_converter)
            beforeShutdown_func_wrapper_addr = ctypes.cast(beforeShutdown_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering beforeShutdown_converter_func_wrapper in app_run, addr {}".format(beforeShutdown_func_wrapper_addr))
                beforeShutdown_func_wrapper_addr_val = beforeShutdown_func_wrapper_addr.value
                # TODO App._weakrefs.append(weakref.ref(beforeShutdown_converter_func_wrapper, lambda x: print("De-referenced beforeShutdown_converter_func_wrapper in app_run, addr {}".format(beforeShutdown_func_wrapper_addr_val))))
        
        InteropUtils.invoke("app_run", cancellationToken, beforeShutdown_func_wrapper_addr)
        return beforeShutdown_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("app_setstatestorage")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def SetStateStorage(stateStorage: c_void_p) -> None:
        """
        Parameters
        ----------
        
        stateStorage: c_void_p
            GC Handle Pointer to .Net type IStateStorage
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("app_setstatestorage", stateStorage)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("app_getstatemanager")
    _interop_func.restype = c_void_p
    @staticmethod
    def GetStateManager() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type AppStateManager
        """
        result = InteropUtils.invoke("app_getstatemanager")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
