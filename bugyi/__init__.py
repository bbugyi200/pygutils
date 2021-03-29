# For accessing modules as attributes of 'bugyi' (e.g. 'bugyi.logging').
#
# DEPRECIATED: Use `from bugyi import <MODULE>` or `from bugyi.<MODULE>
# import <NAME>` instead.
from bugyi import core, debug, io, logging, xdg

# For accessing core functions/classes via `from bugyi import <NAME>`.
#
# DEPRECIATED: Use 'from bugyi.core import <NAME>' instead.
from bugyi.core import (
    catch,
    create_dir,
    efill,
    ewrap,
    mkfifo,
    secret,
    shell,
    signal,
)

# For accessing ArgumentParser via `from bugyi import ArgumentParser`.
#
# DEPRECIATED: Use `from bugyi.cli import ArgumentParser` instead.
from bugyi.cli import ArgumentParser

# For accessing subprocess functions/classes via `from bugyi import <NAME>`.
#
# DEPRECIATED: Use 'from bugyi import subprocess as bsp' instead.
from bugyi.subprocess import create_pidfile, StillAliveException

# For accessing tools.py functions via `from bugyi import <TOOL>`.
#
# DEPRECIATED: Import directly from the 'bugyi.tools' module instead.
from bugyi.tools import notify, xkey, xtype

# For accessing the colors modules via `from bugyi import colorize`.
#
# DEPRECIATED: Use `from bugyi.io import colors` instead.
from bugyi.io import colors as colorize
