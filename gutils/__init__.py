"""Global Utilities"""

# For accessing modules as attributes of 'gutils' (e.g. 'gutils.logging').
#
# DEPRECIATED: Use `from gutils import <MODULE>` or `from gutils.<MODULE>
# import <NAME>` instead.
from gutils import colors, debug, io, logging, xdg

# For accessing core functions/classes via `from gutils import <NAME>`.
#
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

# For accessing the create_pidfile() function via `from gutils import
# create_pidfile`.
#
# DEPRECIATED: Use 'from gutils import subprocess as bsp' instead.
from gutils.subprocess import create_pidfile, StillAliveException


# For accessing the colors modules via `from gutils import colorize`.
#
# DEPRECIATED: Use `from gutils import colors` instead.
colorize = colors
