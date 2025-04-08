#!/usr/bin/env python3

import argparse, turtle
import tkinter as tk, tkinter.messagebox as tkmb, tkinter.filedialog as tkfd
from vqsx import Packed
from PIL import Image, EpsImagePlugin


def main(args):
    # EpsImagePlugin.gs_binary = False

    parser = argparse.ArgumentParser()
    parser.add_argument("-b,--bytecode",
                        dest="bytecode",
                        help="Where is the bytecode file to read from?",
                        nargs="?",
                        type=str)
    parser.add_argument("-d,--debugged",
                        action="store_true",
                        dest="debugged",
                        help="Run in debugged mode?")
    parser.add_argument("-k,--black-canvas",
                        action="store_true",
                        dest="blacked",
                        help="Black the canvas or keep it white?")
    parser.add_argument("-j,--static-canvas",
                        action="store_true",
                        dest="staticscrollcanvas",
                        help="Should the canvas be scrollable or static?")
    
    arged = parser.parse_args(args) # Parse
    bitcode : bytes | None = arged.bytecode # Get the bytecode path
    debugged : bool = arged.debugged # Get debugged mode status
    blacked : bool = arged.blacked # Black the canvas?
    cstaticscroll : bool = not arged.staticscrollcanvas # True if canvas should be static

    # Setup window
    winroot = tk.Tk("VQsX Turtle Renderer")
    packed = Packed(winroot, 
                    scrolledcanvas=cstaticscroll,
                    debugged=debugged)
    packed.pack()

    # Add a menubar
    def construct_menu(rt : tk.Misc, cvs : tk.Canvas) -> tk.Menu:
        menubar = tk.Menu(rt)

        NOPNAN = lambda *_, **__ : None # NOPNAN for NOP
        def save2disk():
            import io
            pef : io.IOBase = tkfd.asksaveasfile(mode="wb")
            with pef:
                epsstream = io.BytesIO(
                        bytes(
                            cvs.postscript(colormode='color'), 
                            "ascii"
                        )
                    )
                
                im = Image.open(epsstream)
                im.save(pef, format="PNG")


        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu) # Add cascade

        filemenu.add_command(label="Load", command=NOPNAN) # Load bytecode
        filemenu.add_command(label="Save", command=save2disk) # Save the canvas
        filemenu.add_separator() # Separate files and quit
        filemenu.add_command(label="Quit", command=rt.quit)


        return menubar
    menumx = construct_menu(winroot, packed.get_canvas())
    winroot.config(menu=menumx)

    # Get jucy bits
    vm = packed.get_vm()
    cvs = packed.get_canvas()

    # Black canvas?
    if blacked:
        # Hack: get width and height
        width, height = (cvs.winfo_reqwidth(), cvs.winfo_reqheight())
        cvs.create_rectangle(-1*(width/2), -1*(height/2), width/2, height/2, fill="black")

    if bitcode:
        try:
            with open(bitcode, "rb") as f:
                packed.load(f)
        except Exception as e:
            tkmb.showwarning("Failed to read Bytecode File", f"There was a problem resding the bytecode file and the turtle renderer will not do anything. \n{e}")
    else:
        tkmb.showwarning("No Bytecode File", "You have not provided a bytecode file to run. The turtle renderer will not do anything.")

    winroot.mainloop()

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
