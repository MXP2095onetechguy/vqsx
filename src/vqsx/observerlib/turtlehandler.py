"""
Turtle implementation of a VQsXObserver.
"""

import turtle as t
from .. import VQsXObserver, VQsXExecutor as VExec

__all__ = ["TurtleObserver"]

class TurtleObserver(VQsXObserver):
    def __init__(self, vexec : VExec, screen : t.TurtleScreen, turtle : t.Turtle):
        self.screen = screen
        self.turtle = turtle
        self.vexec = vexec

    def position(self, x, y):
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.pendown()

    def center(self):
        """
        stub

        TODO: add some magic math to do centering independent of origin
        """
        pass

    def origin(self):
        """
        stub

        TODO: add some origin math
        """