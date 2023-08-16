# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...QuixStreamsTelemetry.Models.CodecType import CodecType
from ...InteropHelpers.InteropUtils import InteropUtils


class CodecSettings(object):
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("codecsettings_setglobalcodectype")
    _interop_func.restype = None
    @staticmethod
    def SetGlobalCodecType(codecType: CodecType) -> None:
        """
        Parameters
        ----------
        
        codecType: CodecType
            Underlying .Net type is CodecType
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("codecsettings_setglobalcodectype", codecType.value)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("codecsettings_get_currentcodec")
    _interop_func.restype = ctypes.c_int
    @staticmethod
    def get_CurrentCodec() -> CodecType:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        CodecType:
            Underlying .Net type is CodecType
        """
        result = InteropUtils.invoke("codecsettings_get_currentcodec")
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("codecsettings_set_currentcodec")
    _interop_func.restype = None
    @staticmethod
    def set_CurrentCodec(value: CodecType) -> None:
        """
        Parameters
        ----------
        
        value: CodecType
            Underlying .Net type is CodecType
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("codecsettings_set_currentcodec", value.value)
