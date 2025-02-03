"""
Virtual machine for executing VQsX binaries.
"""

from .constants import Instructions, int_to_inst, is_noop, is_halt
from .constants import StatusFlags, STATUS_ZERO, STATUS_HALTED, STATUS_NEXT, STATUS_FAULT
from .constants import Colors, index_to_name
from .constants import VQSXI_MAGIC, VQSXI_DIM_FORMAT, VQSXI_CDEPTH_FORMAT, VQSXI_BYTECODELEN_FORMAT

from .types import InvalidVQsXiMagicException, VQsXiBadFieldException, VQsXiBytecodeUnderflowException

import typing, types, enum
import io, struct

from abc import ABC, abstractmethod

__all__ = ["RGBColor", "ColorMap", 
           "map_color", 
           "NullOpBehavior",
           "ByteCodeStream",
           "VQsXaObserver", "VQsXObserver",
           "VQsXExecutor", "ImageEngine"
           ]

class RGBColor(typing.NamedTuple):
    """
    Class for representing colors
    """
    red : int
    blue : int
    green : int

ColorMap : types.MappingProxyType = types.MappingProxyType({
    Colors.BRED: RGBColor(0xFF, 0x55, 0x55),
    Colors.BGREEN: RGBColor(0x55, 0xFF, 0x55),
    Colors.BBLUE: RGBColor(0x55, 0x55, 0xFF),
    Colors.BYELLOW: RGBColor(0xFF, 0xFF, 0x55),
    Colors.BMAGENTA: RGBColor(0xFF, 0x55, 0xFF),
    Colors.BCYAN: RGBColor(0x55, 0xFF, 0xFF),
    Colors.BORANGE: RGBColor(0xFF, 0xAA, 0x55),
    Colors.BPINK: RGBColor(0xFF, 0x69, 0xB4),
    Colors.BLIME: RGBColor(0xAA, 0xFF, 0x55)
})

def map_color(color : int) -> RGBColor:
    """
    Map index to their colors.
    This function unlike index_to_name, would return the default color of BRED if an index is invalid.
    This default value is conformant to the specification of VQsX.
    """
    color : Colors | int | None = index_to_name(color)
    if color is None: color = Colors.BRED
    return ColorMap[color]


ByteCodeStream = bytes | bytearray

@enum.unique
@enum.verify(enum.CONTINUOUS)
class NullOpBehavior(enum.IntEnum):
    """
    Enum to set the behavior of the null opcode.
    """
    NOOP = 0
    HALT = 1
    FAULT = 2

@enum.unique
@enum.verify(enum.CONTINUOUS)
class ObserverEvents(enum.IntEnum):
    """
    Implementation detail enum for observers
    """
    ONSTEP = 0
    FETCHINST = 1
    HALT = 2


class VQsXaObserver(ABC, object):
    """
    The VQsX Abstract Observer.

    This class is an observer class intended to be inherited.
    """

    @abstractmethod
    def onstep(self, post : bool):
        """
        Run whenever the VM fetches and executes an instruction.

        post - Boolean argument. False when this onstep is called before the fetch and execution. True when called after fetch and execution.

        This function is not called when an invalid instruction is encountered.
        """

    @abstractmethod
    def fetchinst(self, inst : Instructions):
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

class VQsXObserver(VQsXaObserver):
    """
    The VQsX Observer.

    This class is a concrete-stub implementation of the VQsX Abstract Observer.
    Implement the method stubs as needed. This class is intended to be used as an easy-to-inherit class.
    """

    def onstep(self, post : bool):
        "stub"

    def fetchinst(self, inst : Instructions):
        "stub"

    def halt(self, faulty : bool):
        "stub"

class VQsXExecutor(object):
    """
    The VQsX virtual machine.

    This virtual machine is a high level virtual machine. It does not emulate the machine precisely, just the operations.
    """

    def __init__(self, nullmode : NullOpBehavior = NullOpBehavior.FAULT):
        """
        Initialization of the VM.
        """
        super().__init__()

        # Observers for observing events like calls from the VM.
        self.__observers : set[VQsXaObserver] = set()

        # Set the behavior of the null opcode
        # Currently faulty, this should be user settable
        self.nullmode : NullOpBehavior = nullmode
        self.__null_isnoop : bool = (self.nullmode == NullOpBehavior.NOOP)
        self.__null_ishalt : bool = (self.nullmode == NullOpBehavior.HALT)

        # Initialize the bytecode to an empty bytecode
        self.bytecode : bytes = bytes()

        # Initialize the VM state.
        self.mst : int = 0 # MST - Memory Start
        self.ipc : int = self.mst # IPC - Instruction Pointer/Program Counter

        self.status : StatusFlags = STATUS_ZERO | STATUS_HALTED # Status - Status register


    def register(self, observer : VQsXaObserver):
        """
        Registers an observer with the VQsX VM.
        """
        self.__observers.add(observer)

    def deregister(self, observer : VQsXaObserver) -> bool:
        """
        Unregisters an observer with the VQsX VM.

        A True return value means the observer has been removed succesfully.
        A False return value means the observer wasn't removed succesfully.
        """

        try:
            self.__observers.remove(observer)
            return True
        except KeyError:
            return False
        
    def __notify_observers(self, event : ObserverEvents, *args, **kwargs):
        """
        Notify observers.

        event is an observer event
        
        This function is an implementation detail. Don't rely on this.
        """

        for observer in self.__observers:
            if event == ObserverEvents.ONSTEP:
                observer.onstep(*args, **kwargs) # Instruction fetched (pre/post)
            elif event == ObserverEvents.FETCHINST:
                observer.fetchinst(*args, **kwargs) # Instruction decoded
            elif event == ObserverEvents.HALT:
                observer.halt(*args, **kwargs) # VM Halted


    def load(self, bytecode : ByteCodeStream | None = None):
        """
        Load the bytecode into the VM and prepare it for execution.
        If you want to reset the bytecode, pass in None
        """

        # No bytecode, empty bytecode
        if bytecode is None: bytecode = bytes()

        # Initialize the bytecode
        self.bytecode = bytes(bytecode)

    def reset(self):
        """
        Reset the VM into its initial state.
        """

        # Reset some instruction pointer/program counter
        self.mst = 0
        self.ipc = self.mst

        self.status = STATUS_ZERO | STATUS_HALTED

    def setup(self):
        """
        Setup the VM with initial values.
        """

    

    
    def __halt(self, faulty : bool):
        """
        Halt the vm.

        The faulty argument specifies whether to halt with fault or not. It basically specifies if the halt is faulty or not in nature.
        """
        self.status = self.status | STATUS_HALTED
        if faulty: self.status = self.status | STATUS_FAULT

        self.__notify_observers(ObserverEvents.HALT, faulty)

    def __ishalted(self) -> bool:
        """
        Utility function to check the halting state.
        """
        return (self.status & STATUS_HALTED)


    def __fetch(self) -> int:
        """
        Fetch bytes and move on.
        """
        mc = self.bytecode[self.ipc]
        self.ipc = self.ipc + 1
        return mc
    
    def spin(self):
        """
        Puts the VM into execution ready state.

        This does not start the execution, just sets some flags for readiness.
        """
        self.status = STATUS_ZERO



    def step(self):
        """
        Single-step the VM.
        This only executes 1 instruction.
        """

        # Handle halt state
        if self.__ishalted(): return

        # Notify observers
        self.__notify_observers(ObserverEvents.ONSTEP, False)

        inst = self.__fetch() # Fetch instructions

        # Handle invalid instructions while at the same time converting it to an Instruction enum
        inst = int_to_inst(inst)
        if inst is None: # Invalid/Illegal? Halt
            self.__halt(True)
            return
        self.__notify_observers(ObserverEvents.FETCHINST, inst)
        
        # Handle the instructions in the order of implementation
        if is_noop(inst, self.__null_isnoop): # Is noop?
            return
        elif is_halt(inst, self.__null_ishalt): # Is halt?
            self.__halt(False)
        else: # For invalid/illegal instructions
            self.__halt(True) # Halt faulty

        self.__notify_observers(ObserverEvents.ONSTEP, True)        


    def run(self):
        """
        Resets and Runs the VM continuosly until the VM is finished executing.
        This is running step multiple times until the VM halts.
        """

        # Reset the VM
        self.reset()

        # Prepare the VM
        self.spin()

        # Run the VM
        while (not (self.status & STATUS_HALTED)):
            self.step()


class ImageEngine(VQsXExecutor, object):
    """
    A variant of the VQsXExecutor VM that allows for VqsX to be used as a graphical image format.
    This virtual machine takes into account the color depth and image size.
    The format that is read is the VQsXi format.
    """

    def __init__(self):
        """
        Initializes the ImageEngine.
        """
        super().__init__()

        self.width = 0
        self.height = 0

        self.colordepth = 0


    def load(self, image : ByteCodeStream | None = None):
        """
        Load the VQsXi image buffer into the VM.
        """

        # Obtain a stream from the image buffer.
        stream = io.BytesIO(image)

        # Validate the magic number
        magic = stream.read(5) # Read the magic number, which is 5 bytes.
        if len(magic) < 5: raise InvalidVQsXiMagicException("Magic number too short! Not a valid VQsXi stream!", magic)
        for i, c in enumerate(magic): # i is index, c is character
            if c != VQSXI_MAGIC[i]:
                raise InvalidVQsXiMagicException("Invalid magic number detected! Not a VQsXi stream!", magic)
            
        # Read the width & height
        bdim = stream.read(16) # Read the bytes that represent the dimension (width, height)
        if len(bdim) < 16: raise VQsXiBadFieldException("Width field is invalid! Not a VQsXi stream!")
        self.width, self.height = struct.unpack(VQSXI_DIM_FORMAT, bdim) # Unpack the dimensions into width and height

        # Read the color depth
        bcdepth = stream.read(1)
        if len(bcdepth) < 1: raise VQsXiBadFieldException("Color Depth field is invalid! Not a VQsXi stream!")
        self.colordepth, = struct.unpack(VQSXI_CDEPTH_FORMAT, bcdepth)

        # Read the length of the bytecode section
        bpcodelength = stream.read(8) # pcode because bbcode sounds weird. p-code (pcode) and bytecode (bcode) is the same thing, so it doesn't matter!
        if len(bpcodelength) < 8: raise VQsXiBadFieldException("Bytecode length field is invalid! Not a VQsXi stream!")
        pcodelength, = struct.unpack(VQSXI_BYTECODELEN_FORMAT, bpcodelength)

        # Slice the image buffer via stream to obtain the bytecode according to the bytecode length
        pcode = stream.read(pcodelength)
        if len(pcode) < pcodelength: raise VQsXiBytecodeUnderflowException("Bytecode size was lower than expectation!", pcodelength, len(pcode))
        
        super().load(pcode)