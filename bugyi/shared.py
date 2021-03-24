"""Internal Shared Utilities for bugyi Package"""

from pathlib import Path

from bugyi.types import StackType


def scriptname(stack: StackType) -> str:
    """ Returns the Filename of the Calling Module

    Args:
        stack: object returned by 'inspect.stack'

    Returns:
        Filename with .py extension stripped off.
    """
    return Path(stack[1].filename).stem
