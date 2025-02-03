"""
The VQsX Forth Interpreter.
"""

from .. import Builder

from contextlib import AbstractAsyncContextManager
from typing import Self

class VQsXForthInterpreter(AbstractAsyncContextManager, object):
    """
    The VQsX Forth Interpreter.

    An implementation of Forth.
    Its more like a compiler, but sure we'll call it an interpreter.
    It does not use the assembler directly, but uses the builder.
    The interpreter translates the world literally to opcodes; the interpreter does not support jumps and calls directly.

    Basically the interpreter compiles VQsX Forth. This version of Forth targets VQsX and hence the available words are designed for VQsX.
    VQsX Forth is not turing complete due to the turing-incomplete nature of VQsX.
    """
    
    def __init__(self):
        self.__builder = Builder() # Create a new builder

        self.words : dict = {} # Words dictionary for words in Forth.

        self.reset()


    def reset(self):
        """
        Resets the internal state and builder.
        """

        # Reset the internal state
        self.words = {}

        self.cleanse()

    def cleanse(self):
        """
        Reset the builder.
        """

        # Reset the builder
        self.__builder.reset()


    def __enter__(self) -> Self:
        self.__builder.__enter__()
        pass

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Cleans up the internal bits.
        """
        self.reset()
        return self.__builder.__exit__(exc_type, exc_val, exc_tb)


    def dump(self) -> bytes:
        """
        Obtain the compiled binary.
        This is just a proxy to the builder, which does the actual job of building the binary.
        """
        return self.__builder.dump()
