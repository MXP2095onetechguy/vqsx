#!/usr/bin/env python3
import vqsx

ie = vqsx.ImageEngine()
try:
    ie.load(b"VQsXi\x16\x00\x16\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x21\x21")
    print(ie.width, ie.height, ie.colordepth)
    print(ie.bytecode)
except vqsx.VQsXiBytecodeUnderflowException as bue:
    print(f"e:{bue.expected} a:{bue.actual}")