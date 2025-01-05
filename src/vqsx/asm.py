from .constants import Instructions, is_noop, INSTRUCTION_PACK
import io, contextlib, struct
from typing import Self

__all__ = ["Assembler", "Builder"]

class Assembler(contextlib.AbstractContextManager, object):
    """
    This assembler class is used to assemble VQsX assembly into VQsX binaries.
    """
    def __init__(self):
        self.__builder = Builder() # Create an internal builder, which actually generates the binary. The assembler is just an interpreter.


    def __enter__(self) -> Self:
        self.__builder.__enter__()
        pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Cleans up the internal bits, including the builder.
        """
        return self.__builder.__exit__(exc_type, exc_val, exc_tb)
    
    
    def assemble(self, assembly : str):
        """
        Assembles the provided assembly source.
        This begins the interpreter, which calls the internal builder to build the binary.
        """
        pass

    def dump(self) -> bytes:
        """
        Obtained the assembled binary.
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
    

    def nop(self, nullnop : bool = False) -> Self:
        """
        Appends a NOP into the binary.

        You can choose to either use the Explicit NOP or the Null NOP with the nullnop argument.
        """

        nop = Instructions.NNOOP if nullnop else Instructions.NOOP
        nop = struct.pack(INSTRUCTION_PACK, nop)
        self.bstream.write(nop)

        return self