import enum

"""
Constants common to different VQsX bits.
"""

__all__ = ["Colors",
           "name_to_index","index_to_name",
           "name_to_str","str_to_name",

           "INSTRUCTION_PACK",
           "Instructions",
           "is_noop",

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
INSTRUCTION_PACK = "<B" # Struct fmt argument for packing opcodes

@enum.unique
@enum.verify(enum.CONTINUOUS)
class Instructions(enum.IntEnum, enum.ReprEnum):
    """
    Enum for instructions and their opcodes
    """
    NNOOP = 0x00 # No-Operation (Null)
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

def is_noop(inst : Instructions) -> bool:
    """
    Function to check if Instruction is a NOP independent of the instruction.
    """
    explicit_nop = ((inst is Instructions.NNOOP) or (inst == Instructions.NNOOP)) # This NOP is the 0x21 NOP (Explicit NOP)
    null_nop = ((inst is Instructions.NOOP) or (inst == Instructions.NOOP)) # This NOP is the 0x00 NOP (Null NOP)
    return explicit_nop or null_nop # Is either Null or Explicit NOP. Both are the same semantically as they are just NOPs, just that the Null NOP is meant for convenience especially with zeroed out memory.


# Constants useful for VQsXi support
VQSXI_MAGIC = list(b"VQsXi")
VQSXI_DIM_FORMAT = "<HH" # struct fmt argument for VQsXi dimensions
VQSXI_CDEPTH_FORMAT = "<?" # struct fmt argument for VQsXi color depth
VQSXI_BYTECODELEN_FORMAT = "<Q" # struct fmt argument for VQsXi bytecode length
