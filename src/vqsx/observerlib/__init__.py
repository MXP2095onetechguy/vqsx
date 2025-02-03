"""
This package is for the default VQsX observer implementations.

All these classes implement the VQsXObserver API in different ways.
"""

from .turtlehandler import TurtleObserver
from .obsrv import obsrv

__all__ = [
    "TurtleObserver",
    "obsrv"
]