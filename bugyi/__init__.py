"""Global Utilities"""

# For accessing modules as attributes of 'bugyi' (e.g. 'bugyi.logging').
#
# DEPRECIATED: Use `from bugyi import <MODULE>` or `from bugyi.<MODULE>
# import <NAME>` instead.
from bugyi import colors, debug, io, logging, xdg

# For accessing core functions/classes via `from bugyi import <NAME>`.
#
# DEPRECIATED: Use 'from bugyi.core import <NAME>' instead.
from bugyi.core import (
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

# For accessing the create_pidfile() function via `from bugyi import
# create_pidfile`.
#
# DEPRECIATED: Use 'from bugyi import subprocess as bsp' instead.
from bugyi.subprocess import create_pidfile, StillAliveException


# For accessing the colors modules via `from bugyi import colorize`.
#
# DEPRECIATED: Use `from bugyi import colors` instead.
colorize = colors
