"""Global Utilities

This package imports core.py into its global namespace. See help(gutils.core)
for documentation on globally defined functions.
"""

from gutils import colorize, debug, io, logging, xdg
from gutils.core import *
from gutils.subprocess import create_pidfile
