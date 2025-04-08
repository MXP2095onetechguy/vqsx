"""
This library is for implementing the stub and default observers.

Custom observers should inherit the observers from here.
"""

import enum
from abc import ABC, abstractmethod
from . import Instructions, SetOriginValues, Colors, RGBColor

__all__ = [
            "ObserverEvents",
            "VQsXObserver", "VQsXaObserver",
            "VQsXStubObserver"
        ]

@enum.unique
class ObserverEvents(enum.IntEnum):
    """
    Implementation detail enum for observers
    """

    # Special events
    ONSTEP = 0
    FETCHINST = 1
    FETCHDECODEDINST = 2
    HALT = 3
    RESET = 4

    # Prefix 100 for anti-collision between special events
    # Each of the events here are instruction related observer events
    POSITION = 100
    CENTER = 101
    ORIGIN = 102
    SETORIGIN = 103
    BRIGHTNESS = 104
    SCALE = 105
    COLOR = 106
    DRAW = 107
    FORWARD = 108
    BACKWARD = 109
    DRAWFORWARD = 110
    DRAWBACKWARD = 111
    ROTATEDEG = 112
    ROTATERAD = 113
    ROTATERDEG = 114
    ROTATERRAD = 115
    ROTATEORIGIN = 116
    ROTATESETORIGIN = 117


class VQsXObserver(ABC, object):
    """
    The VQsX Abstract Observer.

    This class is an observer class intended to be inherited.
    Let the methods of this class document what to expect from each instruction call for instruction events.
    """

    @abstractmethod
    def onstep(self, post : bool):
        """
        Run whenever the VM fetches and executes an instruction.

        post - Boolean argument. False when this onstep is called before the fetch and execution. True when called after fetch and execution.

        This function is not called when an invalid instruction is encountered.
        """

    @abstractmethod
    def fetchinst(self, inst : int):
        """
        Run whenever the VM has fetched but hasn't decoded it.

        inst - The undecoded instruction.
        """

    @abstractmethod
    def fetchdecodedinst(self, inst : Instructions):
        """
        Run whenever the VM has decoded the instruction.

        inst - Instruction argument.
        """

    @abstractmethod
    def halt(self, faulty : bool):
        """
        Run whenever the VM has halted (fault or not).

        faulty - Whether the halting is faulty in nature.

        This method is also the fault observer. Just check the faulty argument.
        """

    @abstractmethod
    def reset(self):
        """
        Run whenever the VM has been reset.
        """


    @abstractmethod
    def position(self, x : int, y : int):
        """
        Run whenever the VM encountered a POSITION instruction.

        x - x position to move to
        y - y position to move to
        """

    @abstractmethod
    def center(self):
        """
        Run whenever the VM encountered a CENTER instruction.
        """

    @abstractmethod
    def origin(self):
        """
        Run whenever the VM encountered an ORIGIN instruction.
        """

    @abstractmethod
    def setorigin(self, ori : SetOriginValues):
        """
        Run whenever the VM encountered a SETORIGIN instruction.
        """

    @abstractmethod
    def brightness(self, lvl : int):
        """
        Run whenever the VM encountered a BRIGHTNESS instruction.
        """

    @abstractmethod
    def scale(self, scale : SetOriginValues):
        """
        Run whenever the VM encountered a SCALE instruction.
        """

    @abstractmethod
    def color(self, color : Colors, actualcolor : RGBColor):
        """
        Run whenever the VM encountered a COLOR instruction.
        """

    @abstractmethod
    def draw(self, x : int, y : int):
        """
        Run whenever the VM encountered a DRAW instruction.

        x and y is the location to move to relative to the current (former) position of the pen.
        """

    @abstractmethod
    def forward(self, dist : int):
        """
        Run whenever the VM encountered a FORWARD instruction.
        """

    @abstractmethod
    def backward(self, dist : int):
        """
        Run whenever the VM encountered a BACKWARD instruction.
        """

    @abstractmethod
    def drawforward(self, dist : int):
        """
        Run whenever the VM encountered a DRAWFORWARD instruction.
        """

    @abstractmethod
    def drawbackward(self, dist : int):
        """
        Run whenever the VM encountered a DRAWBACKWARD instruction.
        """

    @abstractmethod
    def rotatedeg(self, angle : float):
        """
        Run whenever the VM encountered a ROTATEDEG instruction.
        """

    @abstractmethod
    def rotaterad(self, angle : float):
        """
        Run whenever the VM encountered a ROTATERAD instruction.
        """

    @abstractmethod
    def rotaterdeg(self, angle : float):
        """
        Run whenever the VM encountered a ROTATERDEG instruction.
        """

    @abstractmethod
    def rotaterrad(self, angle : float):
        """
        Run whenever the VM encountered a ROTATERAD instruction.
        """

    @abstractmethod
    def rotateorigin(self):
        """
        Run whenever the VM encountered a ROTATEORIGIN instruction.
        """

    @abstractmethod
    def rotatesetorigin(self, origin):
        """
        Run whenever the VM encountered a ROTATESETORIGIN instruction.
        """



VQsXaObserver : type[VQsXObserver] = VQsXObserver # Alias

class VQsXStubObserver(VQsXObserver):
    """
    The VQsX Stub Observer.

    This class is a concrete-stub implementation of the VQsX Abstract Observer.
    Implement the method stubs as needed. This class is intended to be used as an easy-to-inherit class.
    """

    def onstep(self, post : bool):
        "stub"

    def fetchinst(self, inst : int):
        "stub"

    def fetchdecodedinst(self, inst : Instructions):
        "stub"

    def halt(self, faulty : bool):
        "stub"

    def reset(self):
        "stub"


    def position(self, x, y):
        "stub"

    def center(self):
        "stub"

    def origin(self):
        "stub"

    def setorigin(self, ori : SetOriginValues):
        "stub"

    def brightness(self, lvl : int):
        "stub"

    def scale(self, scale : int):
        "stub"

    def color(self, color : Colors, actualcolor : RGBColor):
        "stub"

    def draw(self, x : int, y : int):
        "stub"

    def forward(self, dist : int):
        "stub"

    def backward(self, dist):
        "stub"

    def drawforward(self, dist):
        "stub"

    def drawbackward(self, dist):
        "stub"

    def rotatedeg(self, angle):
        "stub"

    def rotaterad(self, angle):
        "stub"

    def rotaterdeg(self, angle):
        "stub"
    
    def rotaterrad(self, angle):
        "stub"

    def rotateorigin(self):
        "stub"

    def rotatesetorigin(self, origin):
        "stub"

_test = VQsXStubObserver()
