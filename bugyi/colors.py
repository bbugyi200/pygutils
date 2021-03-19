"""Return Colorized Strings using ASCII Color Escape Codes"""

from typing import Callable


def _color_factory(N: int) -> Callable[[str], str]:
    def colorizer(msg: str) -> str:
        return "%s%s%s" % ("\033[{}m".format(N), msg, "\033[0m")

    return colorizer


black = _color_factory(30)
red = _color_factory(31)
green = _color_factory(32)
yellow = _color_factory(33)
blue = _color_factory(34)
magenta = _color_factory(35)
cyan = _color_factory(36)
white = _color_factory(37)
