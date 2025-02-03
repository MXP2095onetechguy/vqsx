import enum
import typing, types

"""
Constants common to different VQsX bits.
"""

__all__ = ["Colors",
           "name_to_index","index_to_name",
           "name_to_str","str_to_name",

           "INSTRUCTION_PACK", "INSTRUCTION_BINARYOP1_PACK", "INSTRUCTION_BINARYOP8_PACK", "INSTRUCTION_UNARY1_PACK", "INSTRUCTION_UNARY8_PACK", "INSTRUCTION_UNARYF_PACK",
           "Instructions",
           "MnemonicEntry", "MnemonicMapping",
           "inst_to_int", "int_to_inst", "inst_to_name",
           "is_noop", "is_halt",

           "SetOriginValues"

           "StatusFlags",
           "STATUS_ZERO", "STATUS_HALTED", "STATUS_NEXT", "STATUS_FAULT",

           "VQSXI_MAGIC",
           "VQSXI_DIM_FORMAT", "VQSXI_CDEPTH_FORMAT"
           ]

# Color constants
@enum.unique
@enum.verify(enum.CONTINUOUS)
class Colors(enum.IntEnum, enum.ReprEnum):
    """
    Constants for defining VQsX color indexes and their names.

    Colors names that are prefixed with B means they are bright colors.
    """
    BRED = 0
    BGREEN = 1
    BBLUE = 2
    BYELLOW = 3
    BMAGENTA = 4
    BCYAN = 5
    BORANGE = 6
    BPINK = 7
    BLIME = 8


    BSKYBLUE = 9
    BPURPLE = 10
    BTEAL = 11

    AZURE = 12

    BWHITE = 13
    BBEIGE = 14
    LAVENDER = 15
    FUCHSIA = 16
    OLIVE = 17
    BROWN = 18
    LIGHTBROWN = 19
    TAN = 20
    GOLD = 21

COLOR_COUNT = len(Colors)

# Color utilities
def name_to_index(name : Colors) -> int:
    """
    Converts a named color into a color index.
    """
    return name.value

def index_to_name(index : int) -> Colors | None:
    """
    Converts a color index into a named color.

    All invalid indexes would result in None being returned.
    """

    if index > 0 and index < COLOR_COUNT:
        return Colors(index)
    return None

def name_to_str(name : Colors) -> str:
    """
    Converts a named color into a string.
    """ 
    return name.name

def str_to_name(string : str) -> Colors | None:
    """
    Converts a string into a named color.

    All invalid strings would result in None being returned.
    """

    if string in Colors.__members__:
        return Colors[string]
    return None


# VQsX Bytecode Utilities
INSTRUCTION_PACK = "<B" # Struct fmt argument for packing operandless opcodes
INSTRUCTION_BINARYOP1_PACK = "<BBB" # Struct fmt argument for packing binary opcodes with 8-bit operands.
INSTRUCTION_BINARYOP8_PACK = "<BQQ" # Struct fmt argument for packing binary opcodes with 64-bit operands.
INSTRUCTION_UNARY1_PACK = "<BB" # Struct fmt argument for packing unary opcodes with an 8-bit operand.
INSTRUCTION_UNARY8_PACK = "<BQ" # Struct fmt argument for packing unary opcodes with a 64-bit operand.
INSTRUCTION_UNARYF_PACK = "<Bd" # Struct fmt argument for packing unary opcodes with a 64-bit IEEE 754 operand.

@enum.unique
@enum.verify(enum.CONTINUOUS)
class Instructions(enum.IntEnum, enum.ReprEnum):
    """
    Enum for instructions and their opcodes
    """
    NULL = 0x00 # Null
    POSITION = 0x01 # Position
    CENTER = 0x02 # Center
    ORIGIN = 0x03 # Origin
    SETORIGIN = 0x04 # Set Origin
    BRIGHTNESS = 0x05 # Set Brightness
    SCALE = 0x06 # Set Scale
    COLOR = 0x07 # Set Color
    DRAW = 0x08 # Draw
    FORWARD = 0x09 # Move Forward
    BACKWARDS = 0x0A # Move Backwards
    DRAWFORWARD = 0x0B # Draw Forward
    DRAWBACKWARDS = 0x0C # Draw Backwards
    ROTATEDEG = 0x0D # Rotate Clockwise Degrees
    ROTATERAD =  0x0E # Rotate Clockwise Radians
    ROTATERDEG = 0x0F # Rotate Counterclockwise Degrees
    ROTATERRAD = 0x10 # Rotate Counterclockwise Radians
    ROTATEORIGIN = 0x11 # Rotate Origin
    ROTATESETORIGIN = 0x12 # Rotate Set Origin
    STPUSH = 0x13 # Push Pen State To Stack
    STPOP = 0x14 # Pop Pen Stack From Stack
    PSPUSH = 0x15 # Push Pen Position To Stack
    PSPOP = 0x16 # Pop Pen Position From Stack
    INITIALIZE = 0x17 # Reset Pen State
    JUMP = 0x18 # Jump
    CALL = 0x19 # Call
    JUMPIPC = 0x1A # Jump IPC Offset
    CALLIPC = 0x1B # Call IPC Offset
    JUMPMST = 0x1C # Jump Memory Start Offset
    CALLMST = 0x1D # Call Memory Start Offset
    RETURN = 0x1E # Return From Call
    HALT = 0x1F # Halt
    WAITNEXT = 0x20 # Wait For NEXT
    NOOP = 0x21 # No-Operation (Explicit/Default)

class MnemonicEntry(typing.NamedTuple):
    """
    Class for representing the mapping between opcodes, instructions and their mnemonics.
    """
    inst : Instructions
    name : str
    mnemonic : str

INSTRUCTION_COUNT = len(Instructions)

MnemonicMapping : types.MappingProxyType = types.MappingProxyType({
    Instructions.NULL: MnemonicEntry(Instructions.NULL, "null", "nul"),
    Instructions.POSITION: MnemonicEntry(Instructions.POSITION, "position", "pos"),
    Instructions.CENTER: MnemonicEntry(Instructions.CENTER, "center", "cntr"),
    Instructions.ORIGIN: MnemonicEntry(Instructions.ORIGIN, "origin", "ori"),
    Instructions.SETORIGIN: MnemonicEntry(Instructions.SETORIGIN, "setorigin", "sori"),
    Instructions.BRIGHTNESS: MnemonicEntry(Instructions.BRIGHTNESS, "brightness", "bri"),
    Instructions.SCALE: MnemonicEntry(Instructions.SCALE, "scale", "scl"),
    Instructions.COLOR: MnemonicEntry(Instructions.COLOR, "color", "clr")
})

def inst_to_int(inst : Instructions) -> int:
    """
    Function to convert instructions into integers.
    """
    return inst.value

def int_to_inst(opcode : int) -> Instructions | None:
    """
    Function to convert opcode integers into instructions.

    All invalid opcodes would result in None being returned. Invalid opcodes include illegal instructions and vice-versa.
    """

    if opcode > (Instructions.NULL - 1) and opcode < INSTRUCTION_COUNT:
        return Instructions(opcode)
    return None

def inst_to_name(inst : Instructions) -> MnemonicEntry | None:
    """
    Function to convert instructions into their string representation.

    Return value is the MnemonicEntry class for the instruction. This class holds info such as their string name and their mnemonic.
    None is returned if inst is invalid
    """

    if inst not in MnemonicMapping:
        return None

    return MnemonicMapping[inst]

def is_noop(inst : Instructions, isnull_noop : bool) -> bool:
    """
    Function to check if instruction is a no-op

    This function returns True if the instruction is a no-op.

    The isnull_noop argument is a boolean that indicates to the function whether the VM interprets the NULL opcode as a no-op or not. 
    """

    if inst == Instructions.NOOP:
        return True
    
    if isnull_noop and inst == Instructions.NULL:
        return True
    
    return False

def is_halt(inst : Instructions, isnull_halt : bool) -> bool:
    """
    Function to check if instruction is a halt instruction

    This function returns True if the instruction is a no-op.

    The isnull_halt argument is a boolean that indicates to the function whether the VM interprets the NULL opcode as a halt instruction or not. 
    """

    if inst == Instructions.HALT:
        return True
    
    if isnull_halt and inst == Instructions.NULL:
        return True
    
    return False

# Constants useful as complementaries to Opcodes
@enum.unique
class SetOriginValues(enum.IntEnum, enum.ReprEnum):
    """
    Values for the SETORIGIN instruction.
    """

    TOPLEFT = 0
    CENTER = 1
    BOTTOMLEFT = 2

# Constants useful for the status register
# Its used with bitfields and bitmasks
@enum.unique
@enum.verify(enum.CONTINUOUS)
@enum.verify(enum.NAMED_FLAGS)
class StatusFlags(enum.IntFlag, enum.ReprEnum):
    """
    Flags providing values
    """
    ZERO = 0
    HALTED = 1 << 0
    NEXT = 1 << 1
    FAULT = 1 << 2
# Aliases for backwards compatibility
STATUS_ZERO = StatusFlags.ZERO
STATUS_HALTED = StatusFlags.HALTED
STATUS_NEXT = StatusFlags.NEXT
STATUS_FAULT = StatusFlags.FAULT


# Constants useful for VQsXi support
VQSXI_MAGIC = list(b"VQsXi")
VQSXI_DIM_FORMAT = "<QQ" # struct fmt argument for VQsXi dimensions
VQSXI_CDEPTH_FORMAT = "<?" # struct fmt argument for VQsXi color depth
VQSXI_BYTECODELEN_FORMAT = "<Q" # struct fmt argument for VQsXi bytecode length
