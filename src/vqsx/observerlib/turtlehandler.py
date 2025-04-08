"""
Turtle implementation of a VQsXObserver.
"""

import turtle as t
from turtle import Vec2D as V, Vec2D
from .. import VQsXStubObserver, VQsXExecutor as VExec, ByteCodeStream as BStream
from .. import Colors, RGBColor
import tkinter as tk
import functools, io

__all__ = ["TurtleObserver", "Packed"]

class TurtleObserver(VQsXStubObserver):
    """
    TODO: make this fully stubless.
    """
    def __init__(self, vexec : VExec, screen : t.TurtleScreen, turtle : t.RawTurtle, debugged : bool):
        """
        TurtleObserver Constructor

        vexec - The VQSXExecutor to bind to
        screen - The TurtleScreen to bind to
        turtle - The RawTurtle to bind to
        debugged - Whether to show turtle during runtime
        """

        self.screen = screen
        self.turtle = turtle
        self.vexec = vexec
        self.debugged = debugged

    
    def onstep(self, post):
        """
        If running in debugged mode, show the turtle when running.
        """
        if self.debugged:
            self.turtle.showturtle()
        else:
            self.turtle.hideturtle()

    def halt(self, faulty):
        """
        If halted, hide the turtle.
        """
        if self.debugged:
            self.turtle.hideturtle()

    def reset(self):
        """
        Reset the turtle on reset.
        """
        self.turtle.reset()


    def position(self, x, y):
        """
        Turtle move relatively.
        """
        self.turtle.penup()
        self.turtle.goto(self.turtle.pos() + V(x, y))

    def center(self):
        """
        Move the turtle to center with home.
        """
        self.turtle.penup()
        self.turtle.home()

    
    def color(self, color : Colors, actualcolor : RGBColor):
        r = actualcolor.red / 255.0
        g = actualcolor.green / 255.0
        b = actualcolor.blue / 255.0
        lgx = (r, g, b)
        # print(color, "->", actualcolor, "->", lgx)
        self.turtle.color(lgx)

    
    def forward(self, dist):
        """
        Move the turtle forward.
        """
        self.turtle.penup()
        self.turtle.forward(dist)
    
    def backward(self, dist):
        """
        Move the turtle backward.
        """
        self.turtle.penup()
        self.turtle.backward(dist)
    
    def drawforward(self, dist):
        """
        Move and draw the turtle backward.
        """
        self.turtle.pendown()
        self.turtle.forward(dist)
        self.turtle.penup()
    
    def drawbackward(self, dist):
        """
        Move and draw the turtle backward.
        """
        self.turtle.pendown()
        self.turtle.backward(dist)
        self.turtle.penup()

    def rotatedeg(self, angle):
        """
        Rotate the turtle by degrees
        """
        self.turtle.setheading(
            self.turtle.heading() + angle
        )

    def rotaterdeg(self, angle):
        """
        Rotate the turtle by degrees in opposite
        """
        self.rotatedeg(angle * -1)

    

class Packed(tk.Frame):
    """
    A Tkinter Frame that houses a canvas that is usable for a VQsX VM to paint on.
    """

    def __init__(self, master : tk.Misc, 
                 showcontrols : bool = True, scrolledcanvas : bool = True,
                 speed : int | str = "fastest",  debugged : bool = False, 
                 *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Query scrolled canvas for size
        _scrolll = t.ScrolledCanvas(self)
        width, height = (_scrolll.winfo_reqwidth(), _scrolll.winfo_reqheight())
        _scrolll.destroy()
        _scrolll = None

        # Create the controls
        self.__canvas = t.ScrolledCanvas(self) if scrolledcanvas else tk.Canvas(self, width=width, height=height)
        self.__cframe = self.__package_controls()

        # Create the turtle bits
        self.__screen = t.TurtleScreen(self.__canvas)
        self.__turtle = t.RawTurtle(self.__screen)

        # Create the VM and Observer
        self.__VM = VExec()
        self.__TO = TurtleObserver(self.__VM, self.__screen, self.__turtle, debugged)
        self.__VM.register(self.__TO)

        # Pack it
        self.__canvas.pack()
        if showcontrols: self.__cframe.pack()

        # Setup turtle
        self.__speed = speed
        self.__turtle.speed(self.__speed)

    def __package_controls(self) -> tk.Misc:
        cframe = tk.Frame(self) # Pack frame

        # Create buttons
        runb = tk.Button(cframe, text="Run", command=self.__crun)
        stepb = tk.Button(cframe, text="Step", command=self.__step)
        resetb = tk.Button(cframe, text="Reset", command=self.__creset)

        # Grid buttons
        runb.grid(row=0, column=0, sticky="nsew")
        # stepb.grid(row=0, column=1, sticky="nsew")
        resetb.grid(row=0, column=2, sticky="nsew")

        return cframe

    
    def __crun(self):
        self.run()

    def __step(self):
        self.step()

    def __creset(self):
        self.reset()

    
    def get_vm(self) -> VExec:
        return self.__VM
    
    def get_canvas(self) -> tk.Canvas:
        return self.__canvas

    
    @functools.singledispatchmethod
    def load(self, addr : int, bytecode : BStream | None = None):
        self.__VM.load(addr, bytecode)

    @load.register
    def __load_stream(self, bytecode : BStream | None = None):
        self.__VM.load(0, bytecode)

    @load.register
    def __load_file(self, stream : io.IOBase):
        self.load(stream.read())


    def reset(self):
        self.__turtle.reset() # Reset turtle

        # Set some bits back
        self.__turtle.speed(self.__speed)

        self.__VM.reset()

    def setup(self):
        self.__VM.setup()

    def step(self):
        self.__VM.step()

    def run(self):
        self.__VM.run()
