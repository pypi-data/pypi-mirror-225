# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from .TypeCode import TypeCode
from ...InteropHelpers.InteropUtils import InteropUtils


class Type(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        ----------
        
        Type:
            Instance wrapping the .net type Type
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = Type._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(Type, cls).__new__(cls)
            Type._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        ----------
        
        Type:
            Instance wrapping the .net type Type
        """
        if '_Type_pointer' in dir(self):
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
        del Type._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("type_get_isinterface")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsInterface(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isinterface", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_gettype")
    _interop_func.restype = c_void_p
    @staticmethod
    def GetType(typeName: str, throwOnError: bool, ignoreCase: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        typeName: str
            Underlying .Net type is string
        
        throwOnError: bool
            Underlying .Net type is Boolean
        
        ignoreCase: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        typeName_ptr = InteropUtils.utf8_to_ptr(typeName)
        throwOnError_bool = 1 if throwOnError else 0
        ignoreCase_bool = 1 if ignoreCase else 0
        
        result = InteropUtils.invoke("type_gettype", typeName_ptr, throwOnError_bool, ignoreCase_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_gettype2")
    _interop_func.restype = c_void_p
    @staticmethod
    def GetType2(typeName: str, throwOnError: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        typeName: str
            Underlying .Net type is string
        
        throwOnError: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        typeName_ptr = InteropUtils.utf8_to_ptr(typeName)
        throwOnError_bool = 1 if throwOnError else 0
        
        result = InteropUtils.invoke("type_gettype2", typeName_ptr, throwOnError_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_gettype3")
    _interop_func.restype = c_void_p
    @staticmethod
    def GetType3(typeName: str) -> c_void_p:
        """
        Parameters
        ----------
        
        typeName: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        typeName_ptr = InteropUtils.utf8_to_ptr(typeName)
        
        result = InteropUtils.invoke("type_gettype3", typeName_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_gettype7")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetType7(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_gettype7", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_namespace")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Namespace(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("type_get_namespace", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_assemblyqualifiedname")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_AssemblyQualifiedName(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("type_get_assemblyqualifiedname", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_fullname")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_FullName(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("type_get_fullname", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isnested")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsNested(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isnested", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_declaringtype")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_DeclaringType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_get_declaringtype", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_reflectedtype")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_ReflectedType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_get_reflectedtype", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_underlyingsystemtype")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_UnderlyingSystemType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_get_underlyingsystemtype", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_istypedefinition")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsTypeDefinition(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_istypedefinition", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isarray")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsArray(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isarray", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isbyref")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsByRef(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isbyref", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_ispointer")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsPointer(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_ispointer", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isconstructedgenerictype")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsConstructedGenericType(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isconstructedgenerictype", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isgenericparameter")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsGenericParameter(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isgenericparameter", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isgenerictypeparameter")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsGenericTypeParameter(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isgenerictypeparameter", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isgenericmethodparameter")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsGenericMethodParameter(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isgenericmethodparameter", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isgenerictype")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsGenericType(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isgenerictype", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isgenerictypedefinition")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsGenericTypeDefinition(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isgenerictypedefinition", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isszarray")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsSZArray(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isszarray", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isvariableboundarray")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsVariableBoundArray(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isvariableboundarray", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isbyreflike")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsByRefLike(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isbyreflike", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isfunctionpointer")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsFunctionPointer(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isfunctionpointer", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isunmanagedfunctionpointer")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsUnmanagedFunctionPointer(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isunmanagedfunctionpointer", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_haselementtype")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_HasElementType(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_haselementtype", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getelementtype")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetElementType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_getelementtype", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getarrayrank")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def GetArrayRank(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("type_getarrayrank", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getgenerictypedefinition")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetGenericTypeDefinition(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_getgenerictypedefinition", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_generictypearguments")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_GenericTypeArguments(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_get_generictypearguments", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getgenericarguments")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetGenericArguments(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_getgenericarguments", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getoptionalcustommodifiers")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetOptionalCustomModifiers(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_getoptionalcustommodifiers", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getrequiredcustommodifiers")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetRequiredCustomModifiers(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_getrequiredcustommodifiers", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_genericparameterposition")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_GenericParameterPosition(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("type_get_genericparameterposition", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getgenericparameterconstraints")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetGenericParameterConstraints(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_getgenericparameterconstraints", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isabstract")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsAbstract(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isabstract", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isimport")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsImport(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isimport", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_issealed")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsSealed(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_issealed", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isspecialname")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsSpecialName(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isspecialname", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isclass")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsClass(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isclass", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isnestedassembly")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsNestedAssembly(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isnestedassembly", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isnestedfamandassem")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsNestedFamANDAssem(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isnestedfamandassem", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isnestedfamily")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsNestedFamily(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isnestedfamily", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isnestedfamorassem")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsNestedFamORAssem(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isnestedfamorassem", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isnestedprivate")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsNestedPrivate(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isnestedprivate", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isnestedpublic")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsNestedPublic(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isnestedpublic", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isnotpublic")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsNotPublic(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isnotpublic", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_ispublic")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsPublic(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_ispublic", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isautolayout")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsAutoLayout(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isautolayout", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isexplicitlayout")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsExplicitLayout(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isexplicitlayout", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_islayoutsequential")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsLayoutSequential(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_islayoutsequential", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isansiclass")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsAnsiClass(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isansiclass", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isautoclass")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsAutoClass(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isautoclass", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isunicodeclass")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsUnicodeClass(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isunicodeclass", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_iscomobject")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsCOMObject(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_iscomobject", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_iscontextful")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsContextful(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_iscontextful", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isenum")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsEnum(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isenum", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_ismarshalbyref")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsMarshalByRef(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_ismarshalbyref", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isprimitive")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsPrimitive(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isprimitive", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isvaluetype")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsValueType(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isvaluetype", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_isassignableto")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def IsAssignableTo(self, targetType: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        targetType: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_isassignableto", self._pointer, targetType)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_issignaturetype")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsSignatureType(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_issignaturetype", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_issecuritycritical")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsSecurityCritical(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_issecuritycritical", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_issecuritysafecritical")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsSecuritySafeCritical(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_issecuritysafecritical", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_issecuritytransparent")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsSecurityTransparent(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_issecuritytransparent", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getfunctionpointercallingconventions")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetFunctionPointerCallingConventions(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_getfunctionpointercallingconventions", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getfunctionpointerreturntype")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetFunctionPointerReturnType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_getfunctionpointerreturntype", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getfunctionpointerparametertypes")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetFunctionPointerParameterTypes(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_getfunctionpointerparametertypes", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getnestedtype")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def GetNestedType(self, name: str) -> c_void_p:
        """
        Parameters
        ----------
        
        name: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        name_ptr = InteropUtils.utf8_to_ptr(name)
        
        result = InteropUtils.invoke("type_getnestedtype", self._pointer, name_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getnestedtypes")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetNestedTypes(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_getnestedtypes", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_gettypearray")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def GetTypeArray(args: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        args: c_void_p
            GC Handle Pointer to .Net type Object[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_gettypearray", args)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_gettypecode")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def GetTypeCode(type: c_void_p) -> TypeCode:
        """
        Parameters
        ----------
        
        type: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        TypeCode:
            Underlying .Net type is TypeCode
        """
        result = InteropUtils.invoke("type_gettypecode", type)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_gettypefromprogid")
    _interop_func.restype = c_void_p
    @staticmethod
    def GetTypeFromProgID(progID: str) -> c_void_p:
        """
        Parameters
        ----------
        
        progID: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        progID_ptr = InteropUtils.utf8_to_ptr(progID)
        
        result = InteropUtils.invoke("type_gettypefromprogid", progID_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_gettypefromprogid2")
    _interop_func.restype = c_void_p
    @staticmethod
    def GetTypeFromProgID2(progID: str, throwOnError: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        progID: str
            Underlying .Net type is string
        
        throwOnError: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        progID_ptr = InteropUtils.utf8_to_ptr(progID)
        throwOnError_bool = 1 if throwOnError else 0
        
        result = InteropUtils.invoke("type_gettypefromprogid2", progID_ptr, throwOnError_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_gettypefromprogid3")
    _interop_func.restype = c_void_p
    @staticmethod
    def GetTypeFromProgID3(progID: str, server: str) -> c_void_p:
        """
        Parameters
        ----------
        
        progID: str
            Underlying .Net type is string
        
        server: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        progID_ptr = InteropUtils.utf8_to_ptr(progID)
        server_ptr = InteropUtils.utf8_to_ptr(server)
        
        result = InteropUtils.invoke("type_gettypefromprogid3", progID_ptr, server_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_gettypefromprogid4")
    _interop_func.restype = c_void_p
    @staticmethod
    def GetTypeFromProgID4(progID: str, server: str, throwOnError: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        progID: str
            Underlying .Net type is string
        
        server: str
            Underlying .Net type is string
        
        throwOnError: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        progID_ptr = InteropUtils.utf8_to_ptr(progID)
        server_ptr = InteropUtils.utf8_to_ptr(server)
        throwOnError_bool = 1 if throwOnError else 0
        
        result = InteropUtils.invoke("type_gettypefromprogid4", progID_ptr, server_ptr, throwOnError_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_basetype")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_BaseType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_get_basetype", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getinterface")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def GetInterface(self, name: str) -> c_void_p:
        """
        Parameters
        ----------
        
        name: str
            Underlying .Net type is string
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        name_ptr = InteropUtils.utf8_to_ptr(name)
        
        result = InteropUtils.invoke("type_getinterface", self._pointer, name_ptr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getinterface2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_ubyte]
    def GetInterface2(self, name: str, ignoreCase: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        name: str
            Underlying .Net type is string
        
        ignoreCase: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        name_ptr = InteropUtils.utf8_to_ptr(name)
        ignoreCase_bool = 1 if ignoreCase else 0
        
        result = InteropUtils.invoke("type_getinterface2", self._pointer, name_ptr, ignoreCase_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getinterfaces")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetInterfaces(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_getinterfaces", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_isinstanceoftype")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def IsInstanceOfType(self, o: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        o: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_isinstanceoftype", self._pointer, o)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_isequivalentto")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def IsEquivalentTo(self, other: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        other: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_isequivalentto", self._pointer, other)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getenumunderlyingtype")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetEnumUnderlyingType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_getenumunderlyingtype", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getenumvalues")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetEnumValues(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Array
        """
        result = InteropUtils.invoke("type_getenumvalues", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getenumvaluesasunderlyingtype")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetEnumValuesAsUnderlyingType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Array
        """
        result = InteropUtils.invoke("type_getenumvaluesasunderlyingtype", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_makearraytype")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def MakeArrayType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_makearraytype", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_makearraytype2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_int]
    def MakeArrayType2(self, rank: int) -> c_void_p:
        """
        Parameters
        ----------
        
        rank: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_makearraytype2", self._pointer, rank)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_makebyreftype")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def MakeByRefType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_makebyreftype", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_makegenerictype")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def MakeGenericType(self, typeArguments: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        typeArguments: c_void_p
            GC Handle Pointer to .Net type Type[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_makegenerictype", self._pointer, typeArguments)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_makepointertype")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def MakePointerType(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_makepointertype", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_makegenericsignaturetype")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def MakeGenericSignatureType(genericTypeDefinition: c_void_p, typeArguments: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        genericTypeDefinition: c_void_p
            GC Handle Pointer to .Net type Type
        
        typeArguments: c_void_p
            GC Handle Pointer to .Net type Type[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_makegenericsignaturetype", genericTypeDefinition, typeArguments)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_makegenericmethodparameter")
    _interop_func.restype = c_void_p
    @staticmethod
    def MakeGenericMethodParameter(position: int) -> c_void_p:
        """
        Parameters
        ----------
        
        position: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        result = InteropUtils.invoke("type_makegenericmethodparameter", position)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_tostring")
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
        result = InteropUtils.invoke("type_tostring", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_equals")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Equals(self, o: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        o: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_equals", self._pointer, o)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_gethashcode")
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
        result = InteropUtils.invoke("type_gethashcode", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_equals2")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Equals2(self, o: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        o: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_equals2", self._pointer, o)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_op_equality")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Equality(left: c_void_p, right: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        left: c_void_p
            GC Handle Pointer to .Net type Type
        
        right: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_op_equality", left, right)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_op_inequality")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def op_Inequality(left: c_void_p, right: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        left: c_void_p
            GC Handle Pointer to .Net type Type
        
        right: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_op_inequality", left, right)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_reflectiononlygettype")
    _interop_func.restype = c_void_p
    @staticmethod
    def ReflectionOnlyGetType(typeName: str, throwIfNotFound: bool, ignoreCase: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        typeName: str
            Underlying .Net type is string
        
        throwIfNotFound: bool
            Underlying .Net type is Boolean
        
        ignoreCase: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type
        """
        typeName_ptr = InteropUtils.utf8_to_ptr(typeName)
        throwIfNotFound_bool = 1 if throwIfNotFound else 0
        ignoreCase_bool = 1 if ignoreCase else 0
        
        result = InteropUtils.invoke("type_reflectiononlygettype", typeName_ptr, throwIfNotFound_bool, ignoreCase_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_isenumdefined")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def IsEnumDefined(self, value: c_void_p) -> bool:
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
        result = InteropUtils.invoke("type_isenumdefined", self._pointer, value)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getenumname")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def GetEnumName(self, value: c_void_p) -> str:
        """
        Parameters
        ----------
        
        value: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("type_getenumname", self._pointer, value)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getenumnames")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def GetEnumNames(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type string[]
        """
        result = InteropUtils.invoke("type_getenumnames", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isserializable")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsSerializable(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isserializable", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_containsgenericparameters")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_ContainsGenericParameters(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_containsgenericparameters", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_isvisible")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsVisible(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_isvisible", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_issubclassof")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def IsSubclassOf(self, c: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        c: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_issubclassof", self._pointer, c)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_isassignablefrom")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def IsAssignableFrom(self, c: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        c: c_void_p
            GC Handle Pointer to .Net type Type
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_isassignablefrom", self._pointer, c)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_name")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_Name(self) -> str:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        str:
            Underlying .Net type is string
        """
        result = InteropUtils.invoke("type_get_name", self._pointer)
        result = c_void_p(result) if result is not None else None
        result_str = InteropUtils.uptr_to_utf8(result)
        return result_str
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_isdefined")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_ubyte]
    def IsDefined(self, attributeType: c_void_p, inherit: bool) -> bool:
        """
        Parameters
        ----------
        
        attributeType: c_void_p
            GC Handle Pointer to .Net type Type
        
        inherit: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        inherit_bool = 1 if inherit else 0
        
        result = InteropUtils.invoke("type_isdefined", self._pointer, attributeType, inherit_bool)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getcustomattributes")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, ctypes.c_ubyte]
    def GetCustomAttributes(self, inherit: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        inherit: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Object[]
        """
        inherit_bool = 1 if inherit else 0
        
        result = InteropUtils.invoke("type_getcustomattributes", self._pointer, inherit_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_getcustomattributes2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, ctypes.c_ubyte]
    def GetCustomAttributes2(self, attributeType: c_void_p, inherit: bool) -> c_void_p:
        """
        Parameters
        ----------
        
        attributeType: c_void_p
            GC Handle Pointer to .Net type Type
        
        inherit: bool
            Underlying .Net type is Boolean
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Object[]
        """
        inherit_bool = 1 if inherit else 0
        
        result = InteropUtils.invoke("type_getcustomattributes2", self._pointer, attributeType, inherit_bool)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_iscollectible")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsCollectible(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("type_get_iscollectible", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_metadatatoken")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_MetadataToken(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("type_get_metadatatoken", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_emptytypes")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_EmptyTypes() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Type[]
        """
        result = InteropUtils.invoke("type_get_emptytypes")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("type_get_missing")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_Missing() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Object
        """
        result = InteropUtils.invoke("type_get_missing")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
