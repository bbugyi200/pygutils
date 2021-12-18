"""Deprecated 'gutils' package."""

import sys
from warnings import warn

import bugyi
from bugyi import *


class GutilsDepreciationWarning(Warning):
    """Deprecated package exception."""


warn(
    "The 'gutils' package has been deprecated. Use the 'bugyi' package"
    " instead.",
    category=GutilsDepreciationWarning,
    stacklevel=2,
)

sys.modules["gutils"] = bugyi
