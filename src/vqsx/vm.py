from .constants import Colors, index_to_name
from .constants import VQSXI_MAGIC, VQSXI_DIM_FORMAT, VQSXI_CDEPTH_FORMAT, VQSXI_BYTECODELEN_FORMAT

from .types import InvalidVQsXiMagicException, VQsXiBadFieldException, VQsXiBytecodeUnderflowException

import typing, types
import io, struct

__all__ = ["RGBColor", "ColorMap", 
           "map_color", 
           "ByteCodeStream",
           "VQsXExecutor", "ImageEngine"
           ]

class RGBColor(typing.NamedTuple):
    """
    Class for representing colors
    """
    red : int
    blue : int
    green : int

ColorMap : types.MappingProxyType = types.MappingProxyType({
    Colors.BRED: RGBColor(0xFF, 0x55, 0x55),
    Colors.BGREEN: RGBColor(0x55, 0xFF, 0x55),
    Colors.BBLUE: RGBColor(0x55, 0x55, 0xFF),
    Colors.BYELLOW: RGBColor(0xFF, 0xFF, 0x55),
    Colors.BMAGENTA: RGBColor(0xFF, 0x55, 0xFF),
    Colors.BCYAN: RGBColor(0x55, 0xFF, 0xFF),
    Colors.BORANGE: RGBColor(0xFF, 0xAA, 0x55),
    Colors.BPINK: RGBColor(0xFF, 0x69, 0xB4),
    Colors.BLIME: RGBColor(0xAA, 0xFF, 0x55)
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


ByteCodeStream = bytes | bytearray

class VQsXExecutor(object):
    """
    The VQsX virtual machine.
    """

    def __init__(self):
        """
        Initialization of the VM.
        """
        super().__init__()

        # Initialize the bytecode to an empty bytecode
        self.bytecode : bytes = bytes()


    def load(self, bytecode : ByteCodeStream | None = None):
        """
        Load the bytecode into the VM and prepare it for execution.
        If you want to reset the bytecode, pass in None
        """

        # No bytecode, empty bytecode
        if bytecode is None: bytecode = bytes()

        # Initialize the bytecode
        self.bytecode = bytes(bytecode)

    def reset(self):
        """
        Reset the VM into its initial state.
        """

    def setup(self):
        """
        Setup the VM with initial values.
        """


    def step(self):
        """
        Single-step the VM.
        This only executes 1 instruction.
        """
        pass

    def run(self):
        """
        Resets and Runs the VM continuosly until the VM is finished executing.
        This is running step multiple times until the VM halts.
        """

        # Reset the VM
        self.reset()

        # Run the VM
        while True:
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
        bdim = stream.read(4) # Read the bytes that represent the dimension (width, height)
        if len(bdim) < 4: raise VQsXiBadFieldException("Width field is invalid! Not a VQsXi stream!")
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