import enum
import io, os
import typing, types

"""
Constants common to different VQsX bits.
"""

__all__ = ["Colors",
           "name_to_index","index_to_name",
           "name_to_str","str_to_name",
           "RGBColor", "ColorMap",
           "map_color",

           "INSTRUCTION_PACK", 
           "INSTRUCTION_RAWBINARYOP1_PACK", "INSTRUCTION_RAWBINARYOP8_PACK", "INSTRUCTION_RAWUNARY1_PACK", "INSTRUCTION_RAWUNARY8_PACK", "INSTRUCTION_RAWUNARYF_PACK",
           "INSTRUCTION_BINARYOP1_PACK", "INSTRUCTION_BINARYOP8_PACK", "INSTRUCTION_UNARY1_PACK", "INSTRUCTION_UNARY8_PACK", "INSTRUCTION_UNARYF_PACK",
           "Instructions",
           "MnemonicEntry", "MnemonicMapping",
           "inst_to_int", "int_to_inst", "inst_to_name",
           "is_noop", "is_halt",

           "SetOriginValues",
           "int_to_sov", "sov_to_int", "sov_to_str", "str_to_sov",

           "StatusFlags",
           "STATUS_ZERO", "STATUS_HALTED", "STATUS_NEXT", "STATUS_FAULT",
           "status_stringify",

           "VQSXI_MAGIC",
           "VQSXI_DIM_FORMAT", "VQSXI_CDEPTH_FORMAT"
           ]

# Special architecture constants
ENDIANESS = "<" # '<' for little-endian. '>' for big-endian.

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

class RGBColor(typing.NamedTuple):
    """
    Class for representing colors
    """
    red : int
    green : int
    blue : int

ColorMap : types.MappingProxyType = types.MappingProxyType({
    Colors.BRED: RGBColor(0xFF, 0x55, 0x55),
    Colors.BGREEN: RGBColor(0x55, 0xFF, 0x55),
    Colors.BBLUE: RGBColor(0x55, 0x55, 0xFF),
    Colors.BYELLOW: RGBColor(0xFF, 0xFF, 0x55),
    Colors.BMAGENTA: RGBColor(0xFF, 0x55, 0xFF),
    Colors.BCYAN: RGBColor(0x55, 0xFF, 0xFF),
    Colors.BORANGE: RGBColor(0xFF, 0xAA, 0x55),
    Colors.BPINK: RGBColor(0xFF, 0x69, 0xB4),
    Colors.BLIME: RGBColor(0xAA, 0xFF, 0x55),

    Colors.BSKYBLUE: RGBColor(0x87, 0xCE, 0xFA),
    Colors.BPURPLE: RGBColor(0xAA, 0x55, 0xFF),
    Colors.BTEAL: RGBColor(0xAA, 0x55, 0xFF),

    Colors.AZURE: RGBColor(0xF0, 0xFF, 0xFF),

    Colors.BWHITE: RGBColor(0xFF, 0xFF, 0xFF)
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


# VQsX Bytecode Utilities
INSTRUCTION_PACK = f"{ENDIANESS}B" # Struct fmt argument for packing operandless opcodes

INSTRUCTION_RAWBINARYOP1_PACK = f"bb" # Struct fmt argument for packing raw binary 8-bit operands.
INSTRUCTION_RAWBINARYOP8_PACK = f"qq" # Struct fmt argument for packing raw binary 64-bit operands.
INSTRUCTION_RAWUNARY1_PACK = f"b" # Struct fmt argument for packing a raw unary 8-bit operand.
INSTRUCTION_RAWUNARY8_PACK = f"q" # Struct fmt argument for packing a raw unary 64-bit operand.
INSTRUCTION_RAWUNARYF_PACK = f"d" # Struct fmt argument for packing a raw unary 64-bit IEEE 754 operand.

INSTRUCTION_BINARYOP1_PACK = f"{ENDIANESS}B{INSTRUCTION_RAWBINARYOP1_PACK}" # Struct fmt argument for packing binary opcodes with 8-bit operands.
INSTRUCTION_BINARYOP8_PACK = f"{ENDIANESS}B{INSTRUCTION_RAWBINARYOP8_PACK}" # Struct fmt argument for packing binary opcodes with 64-bit operands.
INSTRUCTION_UNARY1_PACK = f"{ENDIANESS}B{INSTRUCTION_RAWUNARY1_PACK}" # Struct fmt argument for packing unary opcodes with an 8-bit operand.
INSTRUCTION_UNARY8_PACK = f"{ENDIANESS}B{INSTRUCTION_RAWUNARY8_PACK}" # Struct fmt argument for packing unary opcodes with a 64-bit operand.
INSTRUCTION_UNARYF_PACK = f"{ENDIANESS}B{INSTRUCTION_RAWUNARYF_PACK}" # Struct fmt argument for packing unary opcodes with a 64-bit IEEE 754 operand.

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
    Instructions.COLOR: MnemonicEntry(Instructions.COLOR, "color", "clr"),
    # FILL
    Instructions.NOOP: MnemonicEntry(Instructions.NOOP, "no-operation", "nop")
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

def sov_to_int(ori : SetOriginValues) -> int:
    """
    Converts a SETORIGIN value to an integer.
    """
    return ori.value

def int_to_sov(num : int) -> SetOriginValues:
    """
    Converts an integer to a SETORIGIN value.
    """
    if num > (SetOriginValues.TOPLEFT - 1):
        return SetOriginValues(num)
    return None

def sov_to_str(ori : SetOriginValues) -> str:
    """
    Converts a SETORIGIN value to its string representation.
    """

    return ori.name

def str_to_sov(name : str) -> SetOriginValues:
    """
    Converts a string into a SETORIGIN value.
    """

    if name in SetOriginValues.__members__:
        return SetOriginValues[name]
    return None

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

# good utilities for status
def status_stringify(stat : StatusFlags) -> str:
    jio = io.StringIO("") # Create builder boi

    if stat == STATUS_ZERO: # Deal with zero aka clear aka running with no waiting
        jio.write("ZERO")
        return jio.getvalue()
    
    # utility internals
    def lenio(stream : io.IOBase) -> int:
        pretold = stream.tell() # Get the stream position for reset purposes.
        stream.seek(0, os.SEEK_END) # Seek to end for size.
        told = stream.tell() # Get the stream position. The stream has tell, hence its told. In this state, its the size of the stream.
        stream.seek(pretold, os.SEEK_SET) # Reset now
        return told
    
    def jiopipe(stream : io.IOBase):
        if lenio(stream) > 0:
            stream.write("|")
    
    # Time to deal with messages
    if stat & STATUS_HALTED:
        jiopipe(jio)
        jio.write("HALT")
    if stat & STATUS_NEXT:
        jiopipe(jio)
        jio.write("NEXT")
    if stat & STATUS_FAULT:
        jiopipe(jio)
        jio.write("FAULT")
    return jio.getvalue()


# Constants useful for VQsXi support
VQSXI_MAGIC = list(b"VQsXi")
VQSXI_DIM_FORMAT = f"{ENDIANESS}QQ" # struct fmt argument for VQsXi dimensions
VQSXI_CDEPTH_FORMAT = f"{ENDIANESS}?" # struct fmt argument for VQsXi color depth
VQSXI_BYTECODELEN_FORMAT = f"{ENDIANESS}Q" # struct fmt argument for VQsXi bytecode length
