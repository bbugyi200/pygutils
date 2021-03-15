"""Global Utilities"""

# For accessing modules as attributes of 'gutils' (e.g. 'gutils.logging').
from gutils import colorize, debug, io, logging, xdg

# For accessing core functions/classes via `from gutils import <NAME>`.
# (DEPRECIATED: Use 'from gutils.core import <NAME>' instead.)
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
# (DEPRECIATED: Use 'from gutils import subprocess as bsp' instead.)
from gutils.subprocess import create_pidfile, StillAliveException
