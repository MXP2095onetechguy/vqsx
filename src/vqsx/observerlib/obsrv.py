"""
Testrunner VQsXObserver
"""

from .. import VQsXaObserver, VQsXExecutor
from .. import Instructions, SetOriginValues, Colors, RGBColor
from .. import status_stringify, inst_to_name, sov_to_str, name_to_index, name_to_str

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

    def setorigin(self, ori : SetOriginValues):
        print("SETORIGIN", sov_to_str(ori))

    def brightness(self, lvl : int):
        print("BRIGHTNESS", lvl)

    def scale(self, scale : int):
        print("SCALE", scale)

    def color(self, color : Colors, actualcolor : RGBColor):
        print("COLOR", name_to_index(color), name_to_str(color), actualcolor)

    def draw(self, x : int, y : int):
        print("DRAW", x, y)
    
    def forward(self, dist : int):
        print("FORWARD", dist)

    def backward(self, dist : int):
        print("BACKWARD", dist)

    def drawforward(self, dist):
        print("DRAWFORWARD", dist)

    def drawbackward(self, dist):
        print("DRAWBACKWARD", dist)

    def rotatedeg(self, angle):
        print("ROTATEDEG", angle)

    def rotaterad(self, angle):
        print("ROTATERAD", angle)

    def rotaterdeg(self, angle):
        print("ROTATERDEG", angle)
    
    def rotaterrad(self, angle):
        print("ROTATERRAD", angle)

    def rotateorigin(self):
        print("ROTATEORIGIN")

    def rotatesetorigin(self, origin):
        print("ROTATESETORIGIN", origin)