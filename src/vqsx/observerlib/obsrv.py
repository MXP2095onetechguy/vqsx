"""
Testrunner VQsXObserver
"""

from .. import VQsXaObserver, VQsXExecutor, status_stringify, Instructions, inst_to_name

__all__ = [
        "obsrv"
    ]

class obsrv(VQsXaObserver):
    """
    The testrunner observer.

    This observer is used by the testrunner script and is made for debugging purposes.
    This observer is not meant for general use.
    """
    def __init__(self, vm : VQsXExecutor, silent : bool):
        self.vm : VQsXExecutor = vm
        self.silent = silent
    
    def onstep(self, post : bool):
        if self.silent:
            return
        print("ONSTEP", "poststep" if post else "prestep", status_stringify(self.vm.status))

    def fetchinst(self, inst : int):
        if self.silent:
            return
        print("FETCHINST", inst, hex(inst))

    def fetchdecodedinst(self, inst : Instructions):
        if self.silent:
            return
        nam = inst_to_name(inst)
        if nam is not None: nam = f"[{nam.name}]"
        print("FETCHDECODEDINST", nam)

    def halt(self, faulty : bool):
        print("HALT", "faulty" if faulty else "hlt")


    def position(self, x : int, y : int):
        print("POSITION", f"[{x}, {y}]")

    def center(self):
        print("CENTER")

    def origin(self):
        print("ORIGIN")