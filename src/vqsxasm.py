#!/usr/bin/env python3
"""
The VQsX Assembler CLI.

This assembler uses the VQsX assembler API.
"""

import vqsx
import argparse, sys

asm = vqsx.Assembler()
parser = argparse.ArgumentParser("vqsxasm",
                                 description="The VQsX Assembler.")

parser.add_argument("-o", "--output", 
                    dest="output",
                    help="Where to output the generated assembled binary.",
                    type=str,
                    default="a.vBin")

parser.add_argument("input",
                    help="Input VQsX Assembler assembly source.",
                    type=str)

args = parser.parse_args(sys.argv[1:])

with open(args.input, "r") as f:
    asm.assemble(f)