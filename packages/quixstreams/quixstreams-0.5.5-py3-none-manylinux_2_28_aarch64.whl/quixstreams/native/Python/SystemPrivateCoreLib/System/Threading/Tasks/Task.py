# ***********************GENERATED CODE WARNING************************
# This file is code generated, any modification you do will be lost the
# next time this file is regenerated.
# *********************************************************************

import ctypes
import weakref
from typing import Optional
from ctypes import c_void_p
from typing import Callable
from .....InteropHelpers.InteropUtils import InteropUtils


class Task(object):
    
    _weakrefs = {}
    
    def __new__(cls, net_pointer: c_void_p):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type Task
        
        Returns
        ----------
        
        Task:
            Instance wrapping the .net type Task
        """
        if type(net_pointer) is not c_void_p:
            net_pointer = net_pointer.get_interop_ptr__()
        
        instance = Task._weakrefs.get(net_pointer.value)
        if instance is None:
            instance = super(Task, cls).__new__(cls)
            Task._weakrefs[net_pointer.value] = instance
        
        return instance
    
    def __init__(self, net_pointer: c_void_p, finalize: bool = True):
        """
        Parameters
        ----------
        
        net_pointer: c_void_p
            GC Handle Pointer to .Net type Task
        
        Returns
        ----------
        
        Task:
            Instance wrapping the .net type Task
        """
        if '_Task_pointer' in dir(self):
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
        del Task._weakrefs[self._pointer.value]
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
    _interop_func = InteropUtils.get_function("task_constructor")
    _interop_func.restype = c_void_p
    @staticmethod
    def Constructor(action: Callable[[], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        action: Callable[[], None]
            Underlying .Net type is Action
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        action_func_wrapper_addr = None
        if action is not None:
            action_converter = lambda : action()

            action_converter_func_wrapper = ctypes.CFUNCTYPE(None)(action_converter)
            action_func_wrapper_addr = ctypes.cast(action_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering action_converter_func_wrapper in task_constructor, addr {}".format(action_func_wrapper_addr))
                action_func_wrapper_addr_val = action_func_wrapper_addr.value
                # TODO Task._weakrefs.append(weakref.ref(action_converter_func_wrapper, lambda x: print("De-referenced action_converter_func_wrapper in task_constructor, addr {}".format(action_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("task_constructor", action_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, action_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_constructor2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Constructor2(action: Callable[[], None], cancellationToken: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        action: Callable[[], None]
            Underlying .Net type is Action
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        action_func_wrapper_addr = None
        if action is not None:
            action_converter = lambda : action()

            action_converter_func_wrapper = ctypes.CFUNCTYPE(None)(action_converter)
            action_func_wrapper_addr = ctypes.cast(action_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering action_converter_func_wrapper in task_constructor2, addr {}".format(action_func_wrapper_addr))
                action_func_wrapper_addr_val = action_func_wrapper_addr.value
                # TODO Task._weakrefs.append(weakref.ref(action_converter_func_wrapper, lambda x: print("De-referenced action_converter_func_wrapper in task_constructor2, addr {}".format(action_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("task_constructor2", action_func_wrapper_addr, cancellationToken)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, action_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_constructor5")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Constructor5(action: Callable[[c_void_p], None], state: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        action: Callable[[c_void_p], None]
            Underlying .Net type is Action<Object>
        
        state: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        action_func_wrapper_addr = None
        if action is not None:
            action_converter = lambda p0: action(c_void_p(p0))

            action_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p)(action_converter)
            action_func_wrapper_addr = ctypes.cast(action_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering action_converter_func_wrapper in task_constructor5, addr {}".format(action_func_wrapper_addr))
                action_func_wrapper_addr_val = action_func_wrapper_addr.value
                # TODO Task._weakrefs.append(weakref.ref(action_converter_func_wrapper, lambda x: print("De-referenced action_converter_func_wrapper in task_constructor5, addr {}".format(action_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("task_constructor5", action_func_wrapper_addr, state)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, action_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_constructor6")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    @staticmethod
    def Constructor6(action: Callable[[c_void_p], None], state: c_void_p, cancellationToken: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        action: Callable[[c_void_p], None]
            Underlying .Net type is Action<Object>
        
        state: c_void_p
            GC Handle Pointer to .Net type Object
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        action_func_wrapper_addr = None
        if action is not None:
            action_converter = lambda p0: action(c_void_p(p0))

            action_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p)(action_converter)
            action_func_wrapper_addr = ctypes.cast(action_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering action_converter_func_wrapper in task_constructor6, addr {}".format(action_func_wrapper_addr))
                action_func_wrapper_addr_val = action_func_wrapper_addr.value
                # TODO Task._weakrefs.append(weakref.ref(action_converter_func_wrapper, lambda x: print("De-referenced action_converter_func_wrapper in task_constructor6, addr {}".format(action_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("task_constructor6", action_func_wrapper_addr, state, cancellationToken)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, action_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_start")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def Start(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("task_start", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_runsynchronously")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def RunSynchronously(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("task_runsynchronously", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_get_id")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    def get_Id(self) -> int:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("task_get_id", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_get_currentid")
    _interop_func.restype = InteropUtils.create_nullable(ctypes.c_int)
    @staticmethod
    def get_CurrentId() -> Optional[int]:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        Optional[int]:
            Underlying .Net type is int?
        """
        result = InteropUtils.invoke("task_get_currentid")
        result_optional = None if not result.HasValue else result.Value
        return result_optional
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_get_iscanceled")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsCanceled(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("task_get_iscanceled", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_get_iscompleted")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsCompleted(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("task_get_iscompleted", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_get_iscompletedsuccessfully")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsCompletedSuccessfully(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("task_get_iscompletedsuccessfully", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_get_asyncstate")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    def get_AsyncState(self) -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Object
        """
        result = InteropUtils.invoke("task_get_asyncstate", self._pointer)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_get_completedtask")
    _interop_func.restype = c_void_p
    @staticmethod
    def get_CompletedTask() -> c_void_p:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        result = InteropUtils.invoke("task_get_completedtask")
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_get_isfaulted")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p]
    def get_IsFaulted(self) -> bool:
        """
        Parameters
        ----------
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("task_get_isfaulted", self._pointer)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_dispose")
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
        InteropUtils.invoke("task_dispose", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_wait")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    def Wait(self) -> None:
        """
        Parameters
        ----------
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("task_wait", self._pointer)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_wait2")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Wait2(self, timeout: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        timeout: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("task_wait2", self._pointer, timeout)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_wait3")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def Wait3(self, timeout: c_void_p, cancellationToken: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        timeout: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("task_wait3", self._pointer, timeout, cancellationToken)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_wait4")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    def Wait4(self, cancellationToken: c_void_p) -> None:
        """
        Parameters
        ----------
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("task_wait4", self._pointer, cancellationToken)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_wait5")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, ctypes.c_int]
    def Wait5(self, millisecondsTimeout: int) -> bool:
        """
        Parameters
        ----------
        
        millisecondsTimeout: int
            Underlying .Net type is int
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("task_wait5", self._pointer, millisecondsTimeout)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_wait6")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, ctypes.c_int, c_void_p]
    def Wait6(self, millisecondsTimeout: int, cancellationToken: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        millisecondsTimeout: int
            Underlying .Net type is int
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("task_wait6", self._pointer, millisecondsTimeout, cancellationToken)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_waitasync")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def WaitAsync(self, cancellationToken: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        result = InteropUtils.invoke("task_waitasync", self._pointer, cancellationToken)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_waitasync2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def WaitAsync2(self, timeout: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        timeout: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        result = InteropUtils.invoke("task_waitasync2", self._pointer, timeout)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_waitasync3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def WaitAsync3(self, timeout: c_void_p, cancellationToken: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        timeout: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        result = InteropUtils.invoke("task_waitasync3", self._pointer, timeout, cancellationToken)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_continuewith")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    def ContinueWith(self, continuationAction: Callable[[c_void_p], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        continuationAction: Callable[[c_void_p], None]
            Underlying .Net type is Action<Task>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        continuationAction_func_wrapper_addr = None
        if continuationAction is not None:
            continuationAction_converter = lambda p0: continuationAction(c_void_p(p0))

            continuationAction_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p)(continuationAction_converter)
            continuationAction_func_wrapper_addr = ctypes.cast(continuationAction_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering continuationAction_converter_func_wrapper in task_continuewith, addr {}".format(continuationAction_func_wrapper_addr))
                continuationAction_func_wrapper_addr_val = continuationAction_func_wrapper_addr.value
                # TODO Task._weakrefs.append(weakref.ref(continuationAction_converter_func_wrapper, lambda x: print("De-referenced continuationAction_converter_func_wrapper in task_continuewith, addr {}".format(continuationAction_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("task_continuewith", self._pointer, continuationAction_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, continuationAction_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_continuewith2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def ContinueWith2(self, continuationAction: Callable[[c_void_p], None], cancellationToken: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        continuationAction: Callable[[c_void_p], None]
            Underlying .Net type is Action<Task>
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        continuationAction_func_wrapper_addr = None
        if continuationAction is not None:
            continuationAction_converter = lambda p0: continuationAction(c_void_p(p0))

            continuationAction_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p)(continuationAction_converter)
            continuationAction_func_wrapper_addr = ctypes.cast(continuationAction_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering continuationAction_converter_func_wrapper in task_continuewith2, addr {}".format(continuationAction_func_wrapper_addr))
                continuationAction_func_wrapper_addr_val = continuationAction_func_wrapper_addr.value
                # TODO Task._weakrefs.append(weakref.ref(continuationAction_converter_func_wrapper, lambda x: print("De-referenced continuationAction_converter_func_wrapper in task_continuewith2, addr {}".format(continuationAction_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("task_continuewith2", self._pointer, continuationAction_func_wrapper_addr, cancellationToken)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, continuationAction_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_continuewith6")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p]
    def ContinueWith6(self, continuationAction: Callable[[c_void_p, c_void_p], None], state: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        continuationAction: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is Action<Task, Object>
        
        state: c_void_p
            GC Handle Pointer to .Net type Object
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        continuationAction_func_wrapper_addr = None
        if continuationAction is not None:
            continuationAction_converter = lambda p0, p1: continuationAction(c_void_p(p0), c_void_p(p1))

            continuationAction_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p, c_void_p)(continuationAction_converter)
            continuationAction_func_wrapper_addr = ctypes.cast(continuationAction_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering continuationAction_converter_func_wrapper in task_continuewith6, addr {}".format(continuationAction_func_wrapper_addr))
                continuationAction_func_wrapper_addr_val = continuationAction_func_wrapper_addr.value
                # TODO Task._weakrefs.append(weakref.ref(continuationAction_converter_func_wrapper, lambda x: print("De-referenced continuationAction_converter_func_wrapper in task_continuewith6, addr {}".format(continuationAction_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("task_continuewith6", self._pointer, continuationAction_func_wrapper_addr, state)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, continuationAction_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_continuewith7")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
    def ContinueWith7(self, continuationAction: Callable[[c_void_p, c_void_p], None], state: c_void_p, cancellationToken: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        continuationAction: Callable[[c_void_p, c_void_p], None]
            Underlying .Net type is Action<Task, Object>
        
        state: c_void_p
            GC Handle Pointer to .Net type Object
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        continuationAction_func_wrapper_addr = None
        if continuationAction is not None:
            continuationAction_converter = lambda p0, p1: continuationAction(c_void_p(p0), c_void_p(p1))

            continuationAction_converter_func_wrapper = ctypes.CFUNCTYPE(None, c_void_p, c_void_p)(continuationAction_converter)
            continuationAction_func_wrapper_addr = ctypes.cast(continuationAction_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering continuationAction_converter_func_wrapper in task_continuewith7, addr {}".format(continuationAction_func_wrapper_addr))
                continuationAction_func_wrapper_addr_val = continuationAction_func_wrapper_addr.value
                # TODO Task._weakrefs.append(weakref.ref(continuationAction_converter_func_wrapper, lambda x: print("De-referenced continuationAction_converter_func_wrapper in task_continuewith7, addr {}".format(continuationAction_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("task_continuewith7", self._pointer, continuationAction_func_wrapper_addr, state, cancellationToken)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, continuationAction_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_waitall")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def WaitAll(tasks: c_void_p) -> None:
        """
        Parameters
        ----------
        
        tasks: c_void_p
            GC Handle Pointer to .Net type Task[]
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("task_waitall", tasks)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_waitall2")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def WaitAll2(tasks: c_void_p, timeout: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        tasks: c_void_p
            GC Handle Pointer to .Net type Task[]
        
        timeout: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("task_waitall2", tasks, timeout)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_waitall3")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, ctypes.c_int]
    @staticmethod
    def WaitAll3(tasks: c_void_p, millisecondsTimeout: int) -> bool:
        """
        Parameters
        ----------
        
        tasks: c_void_p
            GC Handle Pointer to .Net type Task[]
        
        millisecondsTimeout: int
            Underlying .Net type is int
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("task_waitall3", tasks, millisecondsTimeout)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_waitall4")
    _interop_func.restype = None
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def WaitAll4(tasks: c_void_p, cancellationToken: c_void_p) -> None:
        """
        Parameters
        ----------
        
        tasks: c_void_p
            GC Handle Pointer to .Net type Task[]
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        None:
            Underlying .Net type is void
        """
        InteropUtils.invoke("task_waitall4", tasks, cancellationToken)
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_waitall5")
    _interop_func.restype = ctypes.c_ubyte
    _interop_func.argtypes = [c_void_p, ctypes.c_int, c_void_p]
    @staticmethod
    def WaitAll5(tasks: c_void_p, millisecondsTimeout: int, cancellationToken: c_void_p) -> bool:
        """
        Parameters
        ----------
        
        tasks: c_void_p
            GC Handle Pointer to .Net type Task[]
        
        millisecondsTimeout: int
            Underlying .Net type is int
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        bool:
            Underlying .Net type is Boolean
        """
        result = InteropUtils.invoke("task_waitall5", tasks, millisecondsTimeout, cancellationToken)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_waitany")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def WaitAny(tasks: c_void_p) -> int:
        """
        Parameters
        ----------
        
        tasks: c_void_p
            GC Handle Pointer to .Net type Task[]
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("task_waitany", tasks)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_waitany2")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def WaitAny2(tasks: c_void_p, timeout: c_void_p) -> int:
        """
        Parameters
        ----------
        
        tasks: c_void_p
            GC Handle Pointer to .Net type Task[]
        
        timeout: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("task_waitany2", tasks, timeout)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_waitany3")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def WaitAny3(tasks: c_void_p, cancellationToken: c_void_p) -> int:
        """
        Parameters
        ----------
        
        tasks: c_void_p
            GC Handle Pointer to .Net type Task[]
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("task_waitany3", tasks, cancellationToken)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_waitany4")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p, ctypes.c_int]
    @staticmethod
    def WaitAny4(tasks: c_void_p, millisecondsTimeout: int) -> int:
        """
        Parameters
        ----------
        
        tasks: c_void_p
            GC Handle Pointer to .Net type Task[]
        
        millisecondsTimeout: int
            Underlying .Net type is int
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("task_waitany4", tasks, millisecondsTimeout)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_waitany5")
    _interop_func.restype = ctypes.c_int
    _interop_func.argtypes = [c_void_p, ctypes.c_int, c_void_p]
    @staticmethod
    def WaitAny5(tasks: c_void_p, millisecondsTimeout: int, cancellationToken: c_void_p) -> int:
        """
        Parameters
        ----------
        
        tasks: c_void_p
            GC Handle Pointer to .Net type Task[]
        
        millisecondsTimeout: int
            Underlying .Net type is int
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        int:
            Underlying .Net type is int
        """
        result = InteropUtils.invoke("task_waitany5", tasks, millisecondsTimeout, cancellationToken)
        return result
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_fromexception")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def FromException(exception: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        exception: c_void_p
            GC Handle Pointer to .Net type Exception
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        result = InteropUtils.invoke("task_fromexception", exception)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_fromcanceled")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def FromCanceled(cancellationToken: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        result = InteropUtils.invoke("task_fromcanceled", cancellationToken)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_run")
    _interop_func.restype = c_void_p
    @staticmethod
    def Run(action: Callable[[], None]) -> c_void_p:
        """
        Parameters
        ----------
        
        action: Callable[[], None]
            Underlying .Net type is Action
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        action_func_wrapper_addr = None
        if action is not None:
            action_converter = lambda : action()

            action_converter_func_wrapper = ctypes.CFUNCTYPE(None)(action_converter)
            action_func_wrapper_addr = ctypes.cast(action_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering action_converter_func_wrapper in task_run, addr {}".format(action_func_wrapper_addr))
                action_func_wrapper_addr_val = action_func_wrapper_addr.value
                # TODO Task._weakrefs.append(weakref.ref(action_converter_func_wrapper, lambda x: print("De-referenced action_converter_func_wrapper in task_run, addr {}".format(action_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("task_run", action_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, action_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_run2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Run2(action: Callable[[], None], cancellationToken: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        action: Callable[[], None]
            Underlying .Net type is Action
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        action_func_wrapper_addr = None
        if action is not None:
            action_converter = lambda : action()

            action_converter_func_wrapper = ctypes.CFUNCTYPE(None)(action_converter)
            action_func_wrapper_addr = ctypes.cast(action_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering action_converter_func_wrapper in task_run2, addr {}".format(action_func_wrapper_addr))
                action_func_wrapper_addr_val = action_func_wrapper_addr.value
                # TODO Task._weakrefs.append(weakref.ref(action_converter_func_wrapper, lambda x: print("De-referenced action_converter_func_wrapper in task_run2, addr {}".format(action_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("task_run2", action_func_wrapper_addr, cancellationToken)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, action_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_run5")
    _interop_func.restype = c_void_p
    @staticmethod
    def Run5(function: Callable[[], c_void_p]) -> c_void_p:
        """
        Parameters
        ----------
        
        function: Callable[[], c_void_p]
            Underlying .Net type is Func<Task>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        function_func_wrapper_addr = None
        if function is not None:
            function_converter = lambda : function()

            function_converter_func_wrapper = ctypes.CFUNCTYPE(c_void_p)(function_converter)
            function_func_wrapper_addr = ctypes.cast(function_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering function_converter_func_wrapper in task_run5, addr {}".format(function_func_wrapper_addr))
                function_func_wrapper_addr_val = function_func_wrapper_addr.value
                # TODO Task._weakrefs.append(weakref.ref(function_converter_func_wrapper, lambda x: print("De-referenced function_converter_func_wrapper in task_run5, addr {}".format(function_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("task_run5", function_func_wrapper_addr)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, function_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_run6")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Run6(function: Callable[[], c_void_p], cancellationToken: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        function: Callable[[], c_void_p]
            Underlying .Net type is Func<Task>
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        function_func_wrapper_addr = None
        if function is not None:
            function_converter = lambda : function()

            function_converter_func_wrapper = ctypes.CFUNCTYPE(c_void_p)(function_converter)
            function_func_wrapper_addr = ctypes.cast(function_converter_func_wrapper, c_void_p)
            if InteropUtils.DebugEnabled:
                print("Registering function_converter_func_wrapper in task_run6, addr {}".format(function_func_wrapper_addr))
                function_func_wrapper_addr_val = function_func_wrapper_addr.value
                # TODO Task._weakrefs.append(weakref.ref(function_converter_func_wrapper, lambda x: print("De-referenced function_converter_func_wrapper in task_run6, addr {}".format(function_func_wrapper_addr_val))))
        
        result = InteropUtils.invoke("task_run6", function_func_wrapper_addr, cancellationToken)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr, function_func_wrapper_addr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_delay")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def Delay(delay: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        delay: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        result = InteropUtils.invoke("task_delay", delay)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_delay2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def Delay2(delay: c_void_p, cancellationToken: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        delay: c_void_p
            GC Handle Pointer to .Net type TimeSpan
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        result = InteropUtils.invoke("task_delay2", delay, cancellationToken)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_delay3")
    _interop_func.restype = c_void_p
    @staticmethod
    def Delay3(millisecondsDelay: int) -> c_void_p:
        """
        Parameters
        ----------
        
        millisecondsDelay: int
            Underlying .Net type is int
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        result = InteropUtils.invoke("task_delay3", millisecondsDelay)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_delay4")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [ctypes.c_int, c_void_p]
    @staticmethod
    def Delay4(millisecondsDelay: int, cancellationToken: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        millisecondsDelay: int
            Underlying .Net type is int
        
        cancellationToken: c_void_p
            GC Handle Pointer to .Net type CancellationToken
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        result = InteropUtils.invoke("task_delay4", millisecondsDelay, cancellationToken)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_whenall")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def WhenAll(tasks: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        tasks: c_void_p
            GC Handle Pointer to .Net type IEnumerable<Task>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        result = InteropUtils.invoke("task_whenall", tasks)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_whenall2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def WhenAll2(tasks: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        tasks: c_void_p
            GC Handle Pointer to .Net type Task[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task
        """
        result = InteropUtils.invoke("task_whenall2", tasks)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_whenany")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def WhenAny(tasks: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        tasks: c_void_p
            GC Handle Pointer to .Net type Task[]
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<Task>
        """
        result = InteropUtils.invoke("task_whenany", tasks)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_whenany2")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p, c_void_p]
    @staticmethod
    def WhenAny2(task1: c_void_p, task2: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        task1: c_void_p
            GC Handle Pointer to .Net type Task
        
        task2: c_void_p
            GC Handle Pointer to .Net type Task
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<Task>
        """
        result = InteropUtils.invoke("task_whenany2", task1, task2)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
    
    # ctypes function return type//parameter fix
    _interop_func = InteropUtils.get_function("task_whenany3")
    _interop_func.restype = c_void_p
    _interop_func.argtypes = [c_void_p]
    @staticmethod
    def WhenAny3(tasks: c_void_p) -> c_void_p:
        """
        Parameters
        ----------
        
        tasks: c_void_p
            GC Handle Pointer to .Net type IEnumerable<Task>
        
        Returns
        -------
        
        c_void_p:
            GC Handle Pointer to .Net type Task<Task>
        """
        result = InteropUtils.invoke("task_whenany3", tasks)
        result_ptr = ctypes.c_void_p(result) if result is not None else None
        return result_ptr
