"""Global Utilities

This package imports core.py into its global namespace. See help(gutils.core)
for documentation on globally defined functions.
"""

import gutils.colorize as colorize
from gutils.core import *
import gutils.debug as debug
import gutils.io as io
import gutils.logging as logging
from gutils.subprocess import create_pidfile
import gutils.xdg as xdg
