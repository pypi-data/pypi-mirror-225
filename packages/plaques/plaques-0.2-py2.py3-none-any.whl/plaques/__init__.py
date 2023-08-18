"""A minimalistic TUI (Text User Interface) library for Linux."""

__version__ = "0.2"

from .base import Color, Pivot, CharCell, Plaque
from .elements import Text, Frame, Window
globals().update(Color.__members__)
globals().update(Pivot.__members__)
globals().update(Frame.__members__)