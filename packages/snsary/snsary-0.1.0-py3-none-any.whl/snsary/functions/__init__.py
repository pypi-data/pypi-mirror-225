"""
A function accepts a single :mod:`Reading <snsary.models.reading>` as an argument and can return zero or more :mod:`Readings <snsary.models.reading>`. This module contains classes whose instances are callable and act as functions.
"""

from .filter import Filter
from .function import Function
from .rename import Rename
from .window import Window
from .window_average import WindowAverage
from .window_summary import WindowSummary

__all__ = [
    "Filter",
    "Window",
    "WindowAverage",
    "Function",
    "WindowSummary",
    "Rename",
]
