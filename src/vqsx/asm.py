"""
Library for constructing VQsX binaries.
"""

from .constants import Instructions, SetOriginValues, Colors
from .constants import INSTRUCTION_PACK, INSTRUCTION_BINARYOP1_PACK, INSTRUCTION_BINARYOP8_PACK, INSTRUCTION_UNARY1_PACK, INSTRUCTION_UNARY8_PACK, INSTRUCTION_UNARYF_PACK
from . import types as vqsxtypes
import io, contextlib, struct, functools
from typing import Self, Iterator, Generator
import shlex

__all__ = ["Assembler", "Builder"]

class Assembler(contextlib.AbstractContextManager, object):
    """
    This assembler class is used to assemble VQsX assembly into VQsX binaries.

    This assembler is not stateless. It has states that is maintained.
    """
    def __init__(self):
        self.__builder = Builder() # Create an internal builder, which actually generates the binary. The assembler is just an interpreter.

        self.reset()


    def __init_active_label(self):
        """
        Initialize the current active label if not set.
        """
        if self.__labelstate not in self.__labels:
            self.__labels[self.__labelstate] = "" # Initialize the currently active label

    def reset(self):
        """
        Reset the assembler.
        """
        self.__builder.reset()

        self.__labelstate : str | None = None # String variable for keeping the current active label. None is the default, AKA no labels.
        self.__labels : dict[str | None, str] = {} # Dictionary for labels and their sources
        self.__init_active_label()



    def __enter__(self) -> Self:
        self.__builder.__enter__()
        pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Cleans up the internal bits, including the builder.
        """
        self.reset()
        return self.__builder.__exit__(exc_type, exc_val, exc_tb)
    

    def __cleanse(self, iterator : Iterator[str]) -> Generator[str, None, None]:
        """
        An internal method for cleansing assembly source lines of top-level comments.
        """

        for line in iterator:
            if line.startswith("#"): # Cleanse top-level comments
                continue
            else:
                yield line

    def __push_label(self, line : str):
        """
        Push string to label for processing.
        """
        self.__labels[self.__labelstate] = self.__labels[self.__labelstate] + line + "\n"

    @functools.singledispatchmethod
    def assemble(self, assembly : str):
        """
        Assembles the provided assembly source.
        This begins the interpreter, which calls the internal builder to build the binary.
        """

        l = iter(assembly.splitlines()) # Create an iterator over the lines.
        cleansed = self.__cleanse(l) # Cleanse the lines of comments and create a generator.

        for count, line in enumerate(cleansed): # Loop over the cleansed lines
            line : str = line # Current line
            count : int = count # Current line number

            if line.startswith(":"):
                tline = shlex.split(line)
                if len(tline) < 1: # Verify that there is a label
                    # TODO: Replace this with a real exception
                    raise vqsxtypes.VQsXAssemblerException("Bad thing.")

                # Fetch and verify the label
                label : str = tline[0]
                if label == ":": # Verify that the label is not just ':'
                    raise vqsxtypes.VQsXInvalidLabelException("Label missing terminating ':'!", label, count)
                if not label.endswith(":"): # Verify that the label does not ends with :
                    raise vqsxtypes.VQsXInvalidLabelException("Label missing terminating ':'!", label, count)


                # Process the label
                labelslice : slice = slice(1, len(label)-1, 1)
                label : str = label[labelslice]
                if label == "":
                    raise vqsxtypes.VQsXInvalidLabelException("Label is empty!", labelslice, count)

                # Set the active label
                # Initialize if the label is new
                self.__labelstate = label
                self.__init_active_label()
                continue

            if line.startswith("."):
                tline = shlex.split(line)
                # print(tline)
                continue

            self.__push_label(line)




    @assemble.register
    def __assemble_stream(self, file : io.IOBase):
        """
        Singledispatch for files
        """

        self.assemble(file.read())

    def dump(self) -> bytes:
        """
        Obtain the assembled binary.
        This is just a proxy to the builder, which does the actual job of building the binary.
        """
        return self.__builder.dump()

class Builder(contextlib.AbstractContextManager, object):
    """
    This class is used to directly assemble VQsX binaries programatically.
    This class directly assembles VQsX binaries without any VQsX assembly being involved.
    Each method call creates a new instruction and appends it.

    This class cannot undo mistakes due to the nature of the building/assembly method.
    """
    def __init__(self):
        self.bstream = io.BytesIO()


    def reset(self):
        self.bstream.close()
        self.bstream = io.BytesIO()

    
    def __enter__(self) -> Self:
        pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Cleans up and closes the internal stream.
        """
        self.bstream.close()
        return False
    

    def dump(self) -> bytes:
        """
        Dumps the built/assembled VQsX binary.
        """
        return self.bstream.getvalue()
    

    def __write_single(self, inst : Instructions):
        """
        DRY up the code: Operandless instructions.
        """

        en_inst = struct.pack(INSTRUCTION_PACK, inst) # Pack and encode the instruction
        self.bstream.write(en_inst)

    def __write_binary1(self, inst : Instructions, arg1, arg2):
        """
        DRY up the code: Binary 8-bit operand instructions.
        """

        en_inst = struct.pack(INSTRUCTION_BINARYOP1_PACK, inst, arg1, arg2) # Pack and encode the instruction
        self.bstream.write(en_inst)

    def __write_binary8(self, inst : Instructions, arg1, arg2):
        """
        DRY up the code: Binary 64-bit operand instructions.
        """

        en_inst = struct.pack(INSTRUCTION_BINARYOP8_PACK, inst, arg1, arg2) # Pack and encode the instruction
        self.bstream.write(en_inst)

    def __write_unary1(self, inst : Instructions, arg):
        """
        DRY up the code: Unary 8-bit operand instructions.
        """

        en_inst = struct.pack(INSTRUCTION_UNARY1_PACK, inst, arg) # Pack and encode the instruction
        self.bstream.write(en_inst)

    def __write_unary8(self, inst : Instructions, arg):
        """
        DRY up the code: Unary 64-bit operand instructions.
        """

        en_inst = struct.pack(INSTRUCTION_UNARY8_PACK, inst, arg) # Pack and encode the instruction
        self.bstream.write(en_inst)

    def __write_unaryf(self, inst : Instructions, arg : float):
        """
        DRY up the code: Unary 64-bit IEEE 754 operand instructions.
        """

        en_inst = struct.pack(INSTRUCTION_UNARYF_PACK, inst, arg) # Pack and encode the instruction
        self.bstream.write(en_inst)
    

    def null(self) -> Self:
        """
        Appends a NULL into the binary.

        How the NULL behaves is dependent on the VQsX engine's behavior.
        """

        self.__write_single(Instructions.NULL) # Write a NULL instruction

        return self
    
    def position(self, x : int, y : int) -> Self:
        """
        Appends a POSITION into the binary.
        """

        self.__write_binary8(Instructions.POSITION, x, y) # Write a POSITION instruction
        
        return self
    
    def center(self) -> Self:
        """
        Appends a CENTER into the binary.
        """

        self.__write_single(Instructions.CENTER) # Too tired to write, no more this comment from now on 'till or except for NOP.

        return self
    
    def origin(self) -> Self:
        """
        Appends an ORIGIN into the binary.
        """

        self.__write_single(Instructions.ORIGIN)

        return self

    def setorigin(self, origin : SetOriginValues) -> Self:
        """
        Appends a SETORIGIN instruction.
        """

        self.__write_unary1(Instructions.SETORIGIN, origin)

        return self

    def brightness(self, brightness : int) -> Self:
        """
        Appends a BRIGHTNESS instruction.
        """

        self.__write_unary1(Instructions.BRIGHTNESS, brightness)

        return self

    def scale(self, scale : int) -> Self:
        """
        Appends a SCALE instruction.
        """

        self.__write_unary1(Instructions.SCALE, scale)

        return self
    
    def color(self, color : Colors) -> Self:
        """
        Appends a COLOR instruction.
        """

        self.__write_unary1(Instructions.COLOR, color)

        return self
    
    def draw(self, x : int, y : int) -> Self:
        """
        Appends a DRAW instruction.
        """

        self.__write_binary8(Instructions.DRAW, x, y)

        return self
    
    def forward(self, dist : int) -> Self:
        """
        Appends a FORWARD instruction.
        """

        self.__write_unary8(Instructions.FORWARD, dist)

        return self

    def backward(self, dist : int) -> Self:
        """
        Appends a BACKWARD instruction.
        """

        self.__write_unary8(Instructions.BACKWARDS, dist)

        return self

    def drawforward(self, dist : int) -> Self:
        """
        Appends a DRAWFORWARD instruction.
        """

        self.__write_unary8(Instructions.DRAWFORWARD, dist)

        return self

    def drawbackwards(self, dist : int) -> Self:
        """
        Appends a DRAWBACKWARDS instruction.
        """

        self.__write_unary8(Instructions.DRAWBACKWARDS, dist)

        return self
    
    def rotatedeg(self, deg : float) -> Self:
        """
        Appends a ROTATEDEG instruction.
        """

        self.__write_unaryf(Instructions.ROTATEDEG, deg)

        return self
    
    def rotaterad(self, deg : float) -> Self:
        """
        Appends a ROTATERAD instruction.
        """

        self.__write_unaryf(Instructions.ROTATERAD, deg)

        return self

    def rotaterdeg(self, deg : float) -> Self:
        """
        Appends a ROTATERDEG instruction.
        """

        self.__write_unaryf(Instructions.ROTATERDEG, deg)

        return self
    
    def rotaterrad(self, deg : float) -> Self:
        """
        Appends a ROTATERRAD instruction.
        """

        self.__write_unaryf(Instructions.ROTATERRAD, deg)

        return self
    
    def rotateorigin(self) -> Self:
        """
        Appends a ROTATEORIGIN instruction.
        """

        self.__write_single(Instructions.ROTATEORIGIN)

        return self
    
    def rotatesetorigin(self, origin : int) -> Self:
        """
        Appends a ROTATESETORIGIN instruction.

        TODO: give origin a proper type
        """

        self.__write_unary1(Instructions.ROTATESETORIGIN, origin)

        return self
    
    def statepush(self) -> Self:
        """
        Appends an STPUSH instruction.
        """

        self.__write_single(Instructions.STPUSH)

        return self
    
    def statepop(self) -> Self:
        """
        Appends an STPOP instruction.
        """

        self.__write_single(Instructions.STPOP)

        return self
    
    def penpush(self) -> Self:
        """
        Appends a PSPUSH instruction.
        """

        self.__write_single(Instructions.PSPUSH)

        return self
    
    def penpop(self) -> Self:
        """
        Appends a PSTPOP instruction.
        """

        self.__write_single(Instructions.PSPOP)

        return self
    
    def initialize(self) -> Self:
        """
        Appends an INITIALIZE instruction.
        """

        self.__write_single(Instructions.INITIALIZE)

        return self

    
    def nop(self) -> Self:
        """
        Appends an explicit NOP into the binary.
        """

        self.__write_single(Instructions.NOOP) # Write a NOP instruction

        return self

