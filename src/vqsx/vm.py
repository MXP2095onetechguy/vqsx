"""
Virtual machine for executing VQsX binaries.
"""

from .constants import Instructions, int_to_inst, is_noop, is_halt
from .constants import StatusFlags, STATUS_ZERO, STATUS_HALTED, STATUS_NEXT, STATUS_FAULT
from .constants import Colors, index_to_name
from .constants import VQSXI_MAGIC, VQSXI_DIM_FORMAT, VQSXI_CDEPTH_FORMAT, VQSXI_BYTECODELEN_FORMAT
from .constants import INSTRUCTION_RAWBINARYOP1_PACK, INSTRUCTION_RAWBINARYOP8_PACK, INSTRUCTION_RAWUNARY1_PACK, INSTRUCTION_RAWUNARY8_PACK, INSTRUCTION_RAWUNARYF_PACK
from .constants import INSTRUCTION_PACK, INSTRUCTION_BINARYOP1_PACK, INSTRUCTION_BINARYOP8_PACK, INSTRUCTION_UNARY1_PACK, INSTRUCTION_UNARY8_PACK, INSTRUCTION_UNARYF_PACK

from .types import InvalidVQsXiMagicException, VQsXiBadFieldException, VQsXiBytecodeUnderflowException

from .observers import VQsXObserver, VQsXaObserver, VQsXStubObserver, ObserverEvents

import typing, types, enum
import io, struct
import functools

# Hidden
_tb_halt = False # traceback on halt
_info_fetcherror = False # fetcherror

class _nsFetchError(typing.NamedTuple):
    ipc : int
    bytecode : bytes
    len : int


from abc import ABC, abstractmethod

__all__ = ["RGBColor", "ColorMap", 
           "map_color", 
           "NullOpBehavior",
           "ByteCodeStream",
           "VQsXObserver", "VQsXaObserver", "VQsXStubObserver",
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

class VQsXExecutor(object):
    """
    The VQsX virtual machine.

    This virtual machine is a high level virtual machine. It does not emulate the machine precisely, just the operations.
    Even yet, some behaviors aren't perfectly emulated because of the way the VM is designed.
    """

    def __init__(self, nullmode : NullOpBehavior = NullOpBehavior.FAULT):
        """
        Initialization of the VM.
        """
        super().__init__()

        # Observers for observing events like calls from the VM.
        self.__observers : set[VQsXObserver] = set()

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


    @functools.singledispatchmethod
    def load(self, addr : int, bytecode : ByteCodeStream | None = None):
        """
        Load the bytecode into the VM and prepare it for execution.
        If you want to reset the bytecode, pass in None

        addr is the address to start from. Its the GOEXEC location.
        """

        # No bytecode, empty bytecode
        if bytecode is None: bytecode = bytes()

        # slice bytecode
        # This emulates the GOEXEC register
        slicedbit = bytes(bytecode[slice(addr, None)])

        # Initialize the bytecode
        self.bytecode = slicedbit

    @load.register
    def __load_stream(self, bytecode : ByteCodeStream | None = None):
        """
        Load the bytecode into the VM and prepare it for execution.
        If you want to reset the bytecode, pass in None
        """

        self.load(0, bytecode)


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

        if _tb_halt:
            import traceback
            traceback.print_stack()

        self.__notify_observers(ObserverEvents.HALT, faulty)

    def __ishalted(self) -> bool:
        """
        Utility function to check the halting state.
        """
        return (self.status & STATUS_HALTED)


    def __fetch(self) -> int | _nsFetchError:
        """
        Fetch bytes and move on.
        
        Meant for instructions
        """
        # print(self.bytecode, self.ipc, len(self.bytecode))
        try:
            mc = self.bytecode[self.ipc]
            self.ipc = self.ipc + 1
            return mc
        except IndexError:
            ns : _nsFetchError = _nsFetchError(self.ipc, self.bytecode, len(self.bytecode))
            return ns
    
    def __fetch_binaryop8(self) -> tuple[int, int]:
        """
        Fetch Binary 64-bit operands.
        """

        ops = bytes()
        nextipc = self.ipc+8
        ops = ops + self.bytecode[self.ipc:nextipc]
        self.ipc = nextipc
        nextipc = self.ipc+8
        ops = ops + self.bytecode[self.ipc:nextipc]
        self.ipc = nextipc
        # print(hex(self.bytecode[self.ipc]))

        op1, op2 = struct.unpack(INSTRUCTION_RAWBINARYOP8_PACK, ops)
        return (op1, op2)

    def __fetch_binaryop1(self) -> tuple[int, int]:
        """
        Fetch Binary 8-bit operands.
        """
    
    
    def spin(self):
        """
        Puts the VM into execution ready state.

        This does not start the execution, just sets some flags for readiness.
        """
        self.status = STATUS_ZERO



    def register(self, observer : VQsXObserver):
        """
        Registers an observer with the VQsX VM.
        """
        self.__observers.add(observer)

    def deregister(self, observer : VQsXObserver) -> bool:
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

        for observer in self.__observers: # Notify all observers
            # We separate all the observer methods so its simpler on the observer's side.
            # Even if its kinda WET, we do this so we can call the appropriate observer methods.

            # Special events
            if event == ObserverEvents.ONSTEP:
                observer.onstep(*args, **kwargs) # Instruction fetched (pre/post)
            elif event == ObserverEvents.FETCHINST:
                observer.fetchinst(*args, **kwargs) # Instruction fetch predecoded
            elif event == ObserverEvents.FETCHDECODEDINST: # Instruction fetch postdecoded
                observer.fetchdecodedinst(*args, **kwargs)
            elif event == ObserverEvents.HALT:
                observer.halt(*args, **kwargs) # VM Halted

            # Instructions!
            if event == ObserverEvents.POSITION:
                observer.position(*args, **kwargs) # hey, position! Get your x & y!
            elif event == ObserverEvents.CENTER:
                observer.center(*args, **kwargs) # hey, center!
            elif event == ObserverEvents.ORIGIN:
                observer.origin(*args, **kwargs) # hey origin!



    def __step_instructions(self, inst : Instructions):
        if inst == Instructions.POSITION:
            pos : tuple[int, int] = self.__fetch_binaryop8()
            self.__notify_observers(ObserverEvents.POSITION, pos[0], pos[1])
        elif inst == Instructions.CENTER:
            self.__notify_observers(ObserverEvents.CENTER)
        elif inst == Instructions.ORIGIN:
            self.__notify_observers(ObserverEvents.ORIGIN)
        else:
            return True
        
        return False

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
        if isinstance(inst, _nsFetchError):
            if _info_fetcherror:
                print(f"ipc={inst.ipc} size={inst.len}", inst.bytecode)

            self.__halt(True)
            return

        # Handle invalid instructions while at the same time converting it to an Instruction enum
        self.__notify_observers(ObserverEvents.FETCHINST, inst)
        inst = int_to_inst(inst)
        if inst is None: # Invalid/Illegal? Halt
            self.__halt(True)
            return
        self.__notify_observers(ObserverEvents.FETCHDECODEDINST, inst)
        
        # Handle the instructions in the order of implementation
        if is_noop(inst, self.__null_isnoop): # Is noop?
            pass
        elif is_halt(inst, self.__null_ishalt): # Is halt?
            self.__halt(False)
        else: # For other/invalid/illegal instructions
            shouldhaltfaulty = self.__step_instructions(inst)
            if shouldhaltfaulty:
                self.__halt(True) # Halt faulty     

        # Halt if there is no more
        if self.ipc >= len(self.bytecode):
            self.__halt(False)

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