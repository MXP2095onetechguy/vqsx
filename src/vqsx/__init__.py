"""
Library and software package to help manipulate and work with VQsX.
"""

# Constant values and utilities
from .constants import Colors
from .constants import name_to_index, index_to_name, name_to_str, str_to_name
from .constants import Instructions
from .constants import inst_to_int, int_to_inst, inst_to_name
from .constants import SetOriginValues
from .constants import StatusFlags
from .constants import STATUS_ZERO, STATUS_HALTED, STATUS_NEXT, STATUS_FAULT
from .constants import VQSXI_MAGIC

from .types import VQsXException
from .types import VQsXExecutorException, VQsXImageEngineException
from .types import InvalidVQsXiMagicException, VQsXiBadFieldException, VQsXiBytecodeUnderflowException
from .types import VQsXAssemblerException
from .types import VQsXInvalidLabelException

from .vm import RGBColor, ColorMap, map_color
from .vm import NullOpBehavior
from .vm import VQsXaObserver, VQsXObserver
from .vm import VQsXExecutor, ImageEngine

from .asm import Assembler, Builder
from .disasm import Disassembler

from .vqsx4 import VQsXForthInterpreter

__all__ = ["Colors",
           "name_to_index", "index_to_name", "name_to_str", "str_to_name",
           "Instructions", 
           "SetOriginValues",
           "StatusFlags",
           "STATUS_ZERO", "STATUS_HALTED", "STATUS_NEXT", "STATUS_FAULT",
           "inst_to_int", "int_to_inst", "inst_to_name",
           "VQSXI_MAGIC",

           "VQsXException",
           "VQsXExecutorException", "VQsXImageEngineException",
           "InvalidVQsXiMagicException", "VQsXiBadFieldException", "VQsXiByteCodeUnderflowException",

           "RGBColor", "ColorMap", "map_color", 
           "NullOpBehavior",
           "VQsXaObserver", "VQsXObserver",
           "VQsXExecutor", "ImageEngine",

           "Assembler", "Builder",
           "Disassembler",

           "VQsXForthInterpreter"
           ]