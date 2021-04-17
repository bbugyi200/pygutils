# For accessing modules as attributes of 'bugyi' (e.g. 'bugyi.logging').
#
# DEPRECIATED: Use `from bugyi import <MODULE>` or `from bugyi.<MODULE> import
# <NAME>` instead.
from bugyi import debug, io, logging, xdg

from bugyi.cli import ArgumentParser
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
from bugyi.subprocess import (
    StillAliveException as _StillAliveException,
    create_pidfile,
)
from bugyi.tools import notify, xkey, xtype

from bugyi.meta import depreciated


ArgumentParser = depreciated(
    ArgumentParser,
    "Importing 'ArgumentParser' directly from the 'bugyi' package is"
    " depreciated. Use 'from bugyi import cli' instead.",
)

_CORE_WARNING = (
    "Accessing / Importing the '{0}' function directly from the 'bugyi'"
    " package is depreciated. Use 'from bugyi.core import {0}' instead.".format
)
catch = depreciated(catch, _CORE_WARNING("catch"))
create_dir = depreciated(create_dir, _CORE_WARNING("create_dir"))
efill = depreciated(efill, _CORE_WARNING("efill"))
ewrap = depreciated(ewrap, _CORE_WARNING("ewrap"))
mkfifo = depreciated(mkfifo, _CORE_WARNING("mkfifo"))
secret = depreciated(secret, _CORE_WARNING("secret"))
shell = depreciated(shell, _CORE_WARNING("shell"))
signal = depreciated(signal, _CORE_WARNING("signal"))

_SUBPROCESS_WARNING = (
    "Importing '{}' directly from the 'bugyi' package is depreciated. Use"
    " 'from bugyi import subprocess as bsp' instead.".format
)
StillAliveException = depreciated(
    _StillAliveException, _SUBPROCESS_WARNING("StillAliveException")
)
create_pidfile = depreciated(
    create_pidfile, _SUBPROCESS_WARNING("create_pidfile")
)

_TOOLS_WARNING = (
    "Importing '{0}' directly from the 'bugyi' package is depreciated. Use"
    " 'from bugyi.tools import {0}' instead.".format
)
notify = depreciated(notify, _TOOLS_WARNING("notify"))
xkey = depreciated(xkey, _TOOLS_WARNING("xkey"))
xtype = depreciated(xtype, _TOOLS_WARNING("xtype"))
