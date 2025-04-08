"""
Virtual machine for executing VQsX binaries.
"""

from .constants import Instructions, int_to_inst, is_noop, is_halt
from .constants import StatusFlags, STATUS_ZERO, STATUS_HALTED, STATUS_NEXT, STATUS_FAULT
from .constants import Colors, index_to_name
from .constants import RGBColor, map_color
from .constants import SetOriginValues, sov_to_int, int_to_sov
from .constants import VQSXI_MAGIC, VQSXI_DIM_FORMAT, VQSXI_CDEPTH_FORMAT, VQSXI_BYTECODELEN_FORMAT
from .constants import INSTRUCTION_RAWBINARYOP1_PACK, INSTRUCTION_RAWBINARYOP8_PACK, INSTRUCTION_RAWUNARY1_PACK, INSTRUCTION_RAWUNARY8_PACK, INSTRUCTION_RAWUNARYF_PACK
from .constants import INSTRUCTION_PACK, INSTRUCTION_BINARYOP1_PACK, INSTRUCTION_BINARYOP8_PACK, INSTRUCTION_UNARY1_PACK, INSTRUCTION_UNARY8_PACK, INSTRUCTION_UNARYF_PACK

from .types import InvalidVQsXiMagicException, VQsXiBadFieldException, VQsXiBytecodeUnderflowException

from .observers import VQsXObserver, VQsXaObserver, VQsXStubObserver, ObserverEvents

import typing, types, enum
import io, struct
import functools
import collections.abc as cabc

# Hidden
_tb_halt = False # traceback on halt
_info_fetcherror = False # fetcherror

class _nsFetchError(typing.NamedTuple):
    ipc : int
    bytecode : bytes
    len : int


from abc import ABC, abstractmethod

__all__ = [
           "NullOpBehavior",
           "ByteCodeStream",
           "VQsXObserver", "VQsXaObserver", "VQsXStubObserver",
           "VQsXExecutor", "ImageEngine"
           ]


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


    def __advance(self, count : int) -> tuple[int, int]:
        """
        DRY attempt for advance.

        Return
            Index 0 - Old ipc
            Index 1 - Next ipc
        """
        oldipc = self.ipc
        nextipc = oldipc+count
        self.ipc = nextipc
        return (oldipc, nextipc)


    def __fetch(self) -> int | _nsFetchError:
        """
        Fetch bytes and move on.
        
        Meant for instructions
        """
        # print(self.bytecode, self.ipc, len(self.bytecode))
        try:
            mc = self.bytecode[self.ipc]
            self.ipc = self.__advance(1)[1]
            return mc
        except IndexError:
            ns : _nsFetchError = _nsFetchError(self.ipc, self.bytecode, len(self.bytecode))
            return ns
    
    def __fetch_binaryop8(self) -> tuple[int, int]:
        """
        Fetch Binary 64-bit operands.
        """

        ops = bytes()
        oldipc, nextipc = self.__advance(8)
        ops = ops + self.bytecode[oldipc:nextipc]
        oldipc, nextipc = self.__advance(8)
        ops = ops + self.bytecode[oldipc:nextipc]
        # print(hex(self.bytecode[self.ipc]))

        op1, op2 = struct.unpack(INSTRUCTION_RAWBINARYOP8_PACK, ops)
        return (op1, op2)

    def __fetch_binaryop1(self) -> tuple[int, int]:
        """
        Fetch Binary 8-bit operands.
        """
        ops = bytes()
        oldipc, nextipc = self.__advance(1)
        ops = ops + self.bytecode[oldipc:nextipc]
        oldipc, nextipc = self.__advance(1)
        ops = ops + self.bytecode[oldipc:nextipc]
        # print(hex(self.bytecode[self.ipc]))

        op1, op2 = struct.unpack(INSTRUCTION_RAWBINARYOP1_PACK, ops)
        return (op1, op2)
    
    def __fetch_unary1(self) -> int:
        """
        Fetch a Unary 8-bit operand
        """

        sop = bytes()
        oldipc, nextipc = self.__advance(1)
        sop = bytes(self.bytecode[oldipc:nextipc])

        op, *_ = struct.unpack(INSTRUCTION_RAWUNARY1_PACK, sop)

        return op
    
    def __fetch_unary8(self) -> int:
        """
        Fetch a Unary 64-bit operand
        """

        sop = bytes()
        oldipc, nextipc = self.__advance(8)
        sop = bytes(self.bytecode[oldipc:nextipc])

        op, *_ = struct.unpack(INSTRUCTION_RAWUNARY8_PACK, sop)

        return op
    
    def __fetch_unaryf(self) -> float:
        """
        Fetch an 64-bit IEEE 754 operand
        """

        sop = bytes()
        oldipc, nextipc = self.__advance(8)
        sop = bytes(self.bytecode[oldipc:nextipc])

        op, *_ = struct.unpack(INSTRUCTION_RAWUNARYF_PACK, sop)

        return op
    
    
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

            # Event MatchDB
            # Used for writing DRY and maintainable code
            MATCHDB : dict[ObserverEvents, types.FunctionType] = {
                # Special events
                ObserverEvents.ONSTEP: observer.onstep,
                ObserverEvents.FETCHINST: observer.fetchinst,
                ObserverEvents.FETCHDECODEDINST: observer.fetchdecodedinst,
                ObserverEvents.HALT: observer.halt,

                # Instructions!
                ObserverEvents.POSITION: observer.position, # hey, position! Get your x & y!
                ObserverEvents.CENTER: observer.center, # hey, center!
                ObserverEvents.ORIGIN: observer.origin, # hey origin!
                ObserverEvents.SETORIGIN: observer.setorigin, # hey, setorigin! Get your setorigin values!
                ObserverEvents.BRIGHTNESS: observer.brightness, # hey, brightness! Get your brightness values!
                ObserverEvents.SCALE: observer.scale, # hey, scale! Get your scale factor values!
                ObserverEvents.COLOR: observer.color, # hey, color! Get your color values here!
                ObserverEvents.DRAW: observer.draw, # hey, draw! Get your x & y!
                ObserverEvents.FORWARD: observer.forward, # hey, forward! Move forward!
                ObserverEvents.BACKWARD: observer.backward, # hey, backwards! Move backwards!
                ObserverEvents.DRAWFORWARD: observer.drawforward, # hey, drawforward! Move and draw forward!
                ObserverEvents.DRAWBACKWARD: observer.drawbackward, # hey, drawbackward! Move and draw backward!
                ObserverEvents.ROTATEDEG: observer.rotatedeg, # TODO: Do more of the hey!
                ObserverEvents.ROTATERAD: observer.rotaterad,
                ObserverEvents.ROTATERDEG: observer.rotaterdeg,
                ObserverEvents.ROTATERRAD: observer.rotaterrad,
                ObserverEvents.ROTATEORIGIN: observer.rotateorigin,
                ObserverEvents.ROTATESETORIGIN: observer.rotatesetorigin,
            }

            # Maintainability
            handler = MATCHDB[event]
            handler(*args, **kwargs)



    def __step_instructions(self, inst : Instructions):

        if inst == Instructions.POSITION:
            pos : tuple[int, int] = self.__fetch_binaryop8()
            self.__notify_observers(ObserverEvents.POSITION, pos[0], pos[1])
        elif inst == Instructions.CENTER:
            self.__notify_observers(ObserverEvents.CENTER)
        elif inst == Instructions.ORIGIN:
            self.__notify_observers(ObserverEvents.ORIGIN)
        elif inst == Instructions.SETORIGIN:
            ori : int = self.__fetch_unary1()
            ori : SetOriginValues = int_to_sov(ori)
            self.__notify_observers(ObserverEvents.SETORIGIN, ori)
        elif inst == Instructions.BRIGHTNESS:
            bri : int = self.__fetch_unary1()
            self.__notify_observers(ObserverEvents.BRIGHTNESS, bri)
        elif inst == Instructions.SCALE:
            scalef : int = self.__fetch_unary1()
            self.__notify_observers(ObserverEvents.SCALE, scalef)
        elif inst == Instructions.COLOR:
            coloridx : int = self.__fetch_unary1()
            color : Colors = index_to_name(coloridx)
            actualcolor : RGBColor = map_color(coloridx)
            self.__notify_observers(ObserverEvents.COLOR, color, actualcolor)
        elif inst == Instructions.DRAW:
            pos : tuple[int, int] = self.__fetch_binaryop8()
            self.__notify_observers(ObserverEvents.DRAW, pos[0], pos[1])
        elif inst == Instructions.FORWARD:
            dist : int = self.__fetch_unary8()
            self.__notify_observers(ObserverEvents.FORWARD, dist)
        elif inst == Instructions.BACKWARDS:
            dist : int = self.__fetch_unary8()
            self.__notify_observers(ObserverEvents.BACKWARD, dist)
        elif inst == Instructions.DRAWFORWARD:
            dist : int = self.__fetch_unary8()
            self.__notify_observers(ObserverEvents.DRAWFORWARD, dist)
        elif inst == Instructions.BACKWARDS:
            dist : int = self.__fetch_unary8()
            self.__notify_observers(ObserverEvents.DRAWBACKWARD, dist)
        elif inst == Instructions.ROTATEDEG:
            angle : float = self.__fetch_unaryf()
            self.__notify_observers(ObserverEvents.ROTATEDEG, angle)
        elif inst == Instructions.ROTATERAD:
            angle : float = self.__fetch_unaryf()
            self.__notify_observers(ObserverEvents.ROTATERAD, angle)
        elif inst == Instructions.ROTATERDEG:
            angle : float = self.__fetch_unaryf()
            self.__notify_observers(ObserverEvents.ROTATERDEG, angle)
        elif inst == Instructions.ROTATERRAD:
            angle : float = self.__fetch_unaryf()
            self.__notify_observers(ObserverEvents.ROTATERAD, angle)
        elif inst == Instructions.ROTATEORIGIN:
            self.__notify_observers(ObserverEvents.ROTATEORIGIN)
        elif inst == Instructions.ROTATESETORIGIN:
            ori : int = self.__fetch_unary1()
            self.__notify_observers(ObserverEvents.ROTATESETORIGIN)
        else:
            return True # Unknown?
        
        return False # Nah

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