"""Global Utilities

This package imports core.py into its global namespace. See help(gutils.core)
for documentation on globally defined functions.
"""

# For accessing modules as attributes of 'gutils' (e.g. 'gutils.logging').
from gutils import colorize, debug, io, logging, xdg
# DEPRECIATED: Use 'from gutils.core import <NAME>' instead.
from gutils.core import (
    ArgumentParser,
    catch,
    cname,
    create_dir,
    efill,
    ewrap,
    Inspector,
    mkfifo,
    notify,
    secret,
    shell,
    signal,
    xkey,
    xtype,
)
# DEPRECIATED: Use 'from gutils import subprocess as bsp' instead.
from gutils.subprocess import create_pidfile
