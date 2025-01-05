"""
Library and software package to help manipulate and work with VQsX.
"""

# Constant values and utilities
from .constants import Colors
from .constants import name_to_index, index_to_name, name_to_str, str_to_name
from .constants import Instructions, is_noop
from .constants import VQSXI_MAGIC

from .types import VQsXException
from .types import VQsXExecutorException, VQsXImageEngineException
from .types import InvalidVQsXiMagicException, VQsXiBadFieldException, VQsXiBytecodeUnderflowException

from .vm import RGBColor, ColorMap, map_color
from .vm import VQsXExecutor, ImageEngine

from .asm import Assembler, Builder
from .disasm import Disassembler

__all__ = ["Colors",
           "name_to_index", "index_to_name", "name_to_str", "str_to_name",
           "Instructions", "is_noop",

           "VQsXException",
           "VQsXExecutorException", "VQsXImageEngineException",
           "InvalidVQsXiMagicException", "VQsXiBadFieldException", "VQsXiByteCodeUnderflowException",

           "RGBColor", "ColorMap", "map_color", 
           "VQsXExecutor", "ImageEngine",

           "Assembler", "Builder",
           "Disassembler"
           ]