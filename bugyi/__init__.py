# For accessing modules as attributes of 'bugyi' (e.g. 'bugyi.logging').
#
# DEPRECIATED: Use `from bugyi import <MODULE>` or `from bugyi.<MODULE>
# import <NAME>` instead.
from bugyi import colors, debug, io, logging, xdg

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
    secret,
    shell,
    signal,
)

# DEPRECIATED: Import directly from the 'bugyi.tools' module instead.
from bugyi.tools import notify, xkey, xtype

# DEPRECIATED: Use 'from bugyi import subprocess as bsp' instead.
from bugyi.subprocess import create_pidfile, StillAliveException


# DEPRECIATED: Use `from bugyi import colors` instead.
colorize = colors
