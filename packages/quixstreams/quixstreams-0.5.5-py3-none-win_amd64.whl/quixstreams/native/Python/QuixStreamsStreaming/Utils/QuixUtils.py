# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from ...InteropHelpers.InteropUtils import InteropUtils


class QuixUtils(object):
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("quixutils_trygetworkspaceidprefix")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def TryGetWorkspaceIdPrefix(topicId: str, workspaceId: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        topicId: str
            Underlying .Net type is string
        
        workspaceId: c_void_p
            GC Handle Pointer to .Net type String&
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        topicId_ptr = InteropUtils.utf8_to_ptr(topicId)
        
        result = InteropUtils.invoke("quixutils_trygetworkspaceidprefix", topicId_ptr, workspaceId)
        return result
