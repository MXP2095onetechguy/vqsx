"""
Library for disassembling VQsX binaries back to their assembly.
"""

from .constants import Instructions, is_noop

__all__ = ["Disassembler"]

class Disassembler(object):
    """
    This disassembler class converts a VQsX binary into its semantically corresponding VQsX assembly.
    This disassembler does not convert into a one-to-one match as elements such as labels are lost during assembly.
    """
    pass