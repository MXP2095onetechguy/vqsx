"""
This library is for implementing the stub and default observers.

Custom observers should inherit the observers from here.
"""

import enum
from abc import ABC, abstractmethod
from . import Instructions

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

    # Prefix 100 for anti-collision between special events
    # Each of the events here are instruction related observer events
    POSITION = 100
    CENTER = 101
    ORIGIN = 102


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

VQsXaObserver : type[VQsXObserver] = VQsXObserver # Alias

class VQsXStubObserver(VQsXaObserver):
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


    def position(self, x, y):
        "stub"

    def center(self):
        "stub"
