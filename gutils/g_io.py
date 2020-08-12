import sys
import termios
import tty
from typing import Any


def getch(prompt: str = None) -> str:
    """Reads a single character from stdin.

    Args:
        prompt (optional): prompt that is presented to user.

    Returns:
        The single character that was read.
    """
    if prompt:
        sys.stdout.write(prompt)

    sys.stdout.flush()

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def emsg(msg: str) -> None:
    """ERROR Message"""
    print("[ERROR] {}".format(msg))


def imsg(msg: str) -> None:
    """INFO Message"""
    print(">>> {}".format(msg))


def eprint(*args: Any, **kwargs: Any) -> None:
    """Helper function for printing to STDERR."""
    print(*args, file=sys.stderr, **kwargs)
