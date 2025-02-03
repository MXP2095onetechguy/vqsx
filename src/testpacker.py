#!/usr/bin/env python3

import vqsx
import argparse, sys

def megapack(b : vqsx.Builder):
    b.statepush() # Push the current pen state (AKA initial pen state)
    b.setorigin(SOV.TOPLEFT).nop().setorigin(SOV.CENTER) # setorigin, nop and setorigin
    b.origin().nop() # origin
    b.position(TESTX1, TESTY1).nop() # position and nop
    b.brightness(10) # Max brightness
    b.scale(1) # Initial scale
    b.color(CLRs.AZURE) # Azure it!
    b.null().nop() # separate
    b.draw(DRAWCONST1, DRAWCONST1) # Draw an azure line
    b.drawforward(5) # Move and draw forwards 5 units
    b.forward(10) # Move forwards 5 units
    b.nop() # Separate
    b.rotatedeg(30.567).drawforward(17) # Rotate by 30.567 degrees and move and draw forwards 17 units
    b.statepop() # pop the state
    b.rotaterrad(2) # Rotate counterclockwise 2 rads
    b.backward(10) # Move backwards 10 units
    b.color(CLRs.BMAGENTA)
    b.draw(TESTX2, TESTY2) # Draw by moving 0xFF 0xFE
    b.initialize() # Reinitialize state assembly
    b.color(CLRs.AZURE) # Azurity

def tinypack(b : vqsx.Builder):
    b.nop()
    b.position(0xFEFFAABBCAFED00D, 0xFACEABCDEF161718)
    b.center()

CLRs = vqsx.Colors
SOV = vqsx.SetOriginValues # Aliasing
b : vqsx.Builder = vqsx.Builder() # Generate a builder

# Constants
TESTX1 = 0xFFFE
TESTY1 = 0xFEFF
DRAWCONST1 = 0x15151515FFFEFCFC
TESTX2 = 0xFF
TESTY2 = 0xFE

# Argparse for output
parser = argparse.ArgumentParser(prog="testpacker",
                                 description="Program for testing the builder")

parser.add_argument("-s", "--silent",
                    dest="silent",
                    action="store_true",
                    help="Silent output?")
parser.add_argument("-t", "--tiny",
                    dest="tiny",
                    action="store_true",
                    help="Tiny packed output?")

parser.add_argument("output",
                    nargs="?",
                    help="Output location of the test binary.",
                    type=str)

# parse and fetch
args = parser.parse_args(sys.argv[1:])
silent = args.silent
tiny = args.tiny
outfile = args.output

# Test building
if tiny:
    tinypack(b)
else:
    megapack(b)


dumpy = b.dump() # Dump
if not silent: 
    print(dumpy)
    print(list(dumpy))

if outfile:
    with open(outfile, "wb") as f:
        f.write(dumpy)