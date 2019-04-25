"""Internal Shared Utilities for gutils Package"""

import inspect
import os  # noqa: F401
from pathlib import Path
from typing import *  # noqa: F401
from types import *  # noqa: F401

# ----- Type Aliases -----
StackType = List[inspect.FrameInfo]
# ------------------------


def scriptname(stack: StackType) -> str:
    """ Returns the Filename of the Calling Module

    Args:
        stack: object returned by 'inspect.stack'

    Returns:
        Filename with .py extension stripped off.
    """
    return Path(stack[1].filename).stem
