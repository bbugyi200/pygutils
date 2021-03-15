"""Internal Shared Utilities for bugyi Package"""

import inspect
from pathlib import Path
from typing import List


StackType = List[inspect.FrameInfo]


def scriptname(stack: StackType) -> str:
    """ Returns the Filename of the Calling Module

    Args:
        stack: object returned by 'inspect.stack'

    Returns:
        Filename with .py extension stripped off.
    """
    return Path(stack[1].filename).stem
