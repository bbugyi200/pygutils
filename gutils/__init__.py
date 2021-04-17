"""Depreciated 'gutils' package."""

import sys
from warnings import warn

import bugyi
from bugyi import *


class GutilsDepreciationWarning(Warning):
    """Depreciated package exception."""


warn(
    "The 'gutils' package has been depreciated. Use the 'bugyi' package"
    " instead.",
    category=GutilsDepreciationWarning,
    stacklevel=2,
)

sys.modules["gutils"] = bugyi
