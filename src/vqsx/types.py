"""
Types needed to support the VQsX libraries.
All these bits are common.

This module mostly houses exception types, but can be expanded later on.
"""

__all__ = ["VQsXException",
           
           "VQsXExecutorException", "VQsXImageEngineException",

           "IllegalInstructionException",
           
           "VQsXAssemblerException",
           "VQsXInvalidLabelException"]

# Base Exception
class VQsXException(Exception):
    """
    Exception that is the superclass of all VQsX related exceptions.
    Exception that is also the most generic VQsX exceptions when there are very generic problems.
    """
    pass


class VQsXExecutorException(VQsXException):
    """
    Exception that is used for problems related to the VM.
    """
    pass

class VQsXImageEngineException(VQsXExecutorException):
    """
    Exception that is used for problems related to the VQsXi Image Engine.
    """


class InvalidVQsXiMagicException(VQsXImageEngineException):
    """
    Exception for when the magic number is invalid.

    Obtain the magic number in question via the magic attribute.
    """

    def __init__(self, message, magic : bytes):
        """
        Constructor.

        message - message of the exception.
        magic - the invalid magic number in question.
        """
        super().__init__(message)

        self.magic = magic

class VQsXiBadFieldException(VQsXImageEngineException):
    """
    Exception raised when a field other than the magic number is invalid.
    """
    pass

class VQsXiBytecodeUnderflowException(VQsXImageEngineException):
    """
    Exception raised when the bytecode is unexpectedly shorter than the counted bytecode length from the bytecode length field of the header.

    This error means there is too little bytecode. Bytecode size is less than expected exception.

    The underflow is in the sense that there's too little. Its a poorly chosen name, but whatever.
    """
    def __init__(self, message, expected : int, actual : int):
        """
        Constructor.

        message - message of the exception.
        expected - expected number of bytes for the bytecode.
        actual - how much bytecode was actually there.
        """
        super().__init__(message)

        self.expected = expected
        self.actual = actual


class VQsXAssemblerException(VQsXException):
    """
    Superclass exception for all VQsX Assembler related errors.
    """
    pass


class VQsXInvalidLabelException(VQsXAssemblerException):
    """
    Exception for when an invalid label is encountered by the assembler.
    """
    def __init__(self, message, offender : str, line : int):
        super().__init__(message)

        self.offender = offender
        self.line = line
