import argparse
import atexit
import errno
import inspect
import os
from os.path import abspath, isfile, realpath
import random
import signal as sig
import string
import subprocess as sp
import sys
from textwrap import wrap
from typing import Any, Callable, Iterator, Sequence, TypeVar

from loguru import logger as log

import gutils
import gutils.shared as shared


try:
    from typing import Protocol
except ImportError:
    Protocol = object  # type: ignore


_T = TypeVar("_T")


def ArgumentParser(
    *args: Any, description: Any = None, **kwargs: Any
) -> argparse.ArgumentParser:
    """Wrapper for argparse.ArgumentParser."""
    if description is None:
        try:
            frame = inspect.stack()[1].frame
            description = frame.f_globals["__doc__"]
        except KeyError:
            pass

    parser = argparse.ArgumentParser(  # type: ignore
        *args, description=description, **kwargs
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debugging mode."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output."
    )

    return parser


def catch(func: Callable) -> Callable:
    """Wrapper for loguru.logger.catch"""
    catcher = log.bind(quiet=True)
    return catcher.catch(
        message="{record[exception].type.__name__}", reraise=True
    )(func)


def create_dir(directory: str) -> None:
    """Create directory if it does not already exist.

    Args:
        directory: full directory path.
    """
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def mkfifo(FIFO_PATH: str) -> None:
    """Creates named pipe if it does not already exist.

    Args:
        FIFO_PATH (str): the full file path where the named pipe will be
        created.
    """
    try:
        os.mkfifo(FIFO_PATH)
    except OSError:
        pass


def notify(*args: str, title: str = None, urgency: str = None) -> None:
    """
    Sends desktop notification with calling script's name as the notification
    title.

    Args:
        *args: Arguments to be passed to the notify-send command.
        title (opt): Notification title.
        urgency (opt): Notification urgency.
    """
    try:
        assert args, "No notification message specified."
        assert urgency in (
            None,
            "low",
            "normal",
            "critical",
        ), "Invalid Urgency: {}".format(urgency)
    except AssertionError as e:
        raise ValueError(str(e)) from e

    if title is None:
        title = shared.scriptname(inspect.stack())

    cmd_list = ["notify-send"]
    cmd_list.extend([title])

    if urgency is not None:
        cmd_list.extend(["-u", urgency])

    cmd_list.extend(args)

    sp.check_call(cmd_list)


def secret() -> str:
    """Get Secret String for Use with secret.sh Script"""
    secret_key = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(16)
    )
    fp = "/tmp/{}.secret".format(shared.scriptname(inspect.stack()))

    @atexit.register
    def remove_secret_file() -> None:  # pylint: disable=unused-variable
        """Exit Handler that Removes Secret File"""
        try:
            os.remove(fp)
        except OSError:
            pass

    with open(fp, "w") as f:
        f.write(secret_key)

    return secret_key


def shell(*cmds: str) -> str:
    """Run Shell Command(s)"""
    out = sp.check_output("; ".join(cmds), shell=True)
    return out.decode().strip()


def signal(*signums: int) -> Callable:
    """A decorator for registering signal handlers."""

    def _signal(handler: Callable) -> Callable:
        for signum in signums:
            sig.signal(signum, handler)

        return handler

    return _signal


def xkey(key: str) -> None:
    """Wrapper for `xdotool key`"""
    sp.check_call(["xdotool", "key", key])


def xtype(keys: str, *, delay: int = None) -> None:
    """Wrapper for `xdotool type`

    Args:
        keys (str): Keys to type.
        delay (optional): Typing delay.
    """
    if delay is None:
        delay = 150

    keys = keys.strip("\n")

    sp.check_call(["xdotool", "type", "--delay", str(delay), keys])


def cname(obj):
    # type: (object) -> str
    """Helper function for getting an object's class name as a string."""
    return obj.__class__.__name__


def ewrap(multiline_msg, width=80, indent=0):
    # type: (str, int, int) -> Iterator[str]
    """A better version of textwrap.wrap()."""
    for msg in multiline_msg.split("\n"):
        if not msg:
            yield ""
            continue

        msg = (" " * indent) + msg

        i = 0
        while i < len(msg) and msg[i] == " ":
            i += 1

        spaces = " " * i
        for m in wrap(
            msg, width, subsequent_indent=spaces, drop_whitespace=True
        ):
            yield m


def efill(multiline_msg, width=80, indent=0):
    # type: (str, int, int) -> str
    """A better version of textwrap.fill()."""
    return "\n".join(ewrap(multiline_msg, width, indent))


class Inspector:
    """
    Helper class for python introspection (e.g. What line number is this?)
    """

    def __init__(self, up=0):
        # type: (int) -> None
        stack = inspect.stack()[up + 1]

        self.module_name = _path_to_module(stack[1])
        self.file_name = stack[1]
        self.line_number = stack[2]
        self.function_name = stack[3]
        self.lines = "".join(stack[4] or [])


def _path_to_module(path):
    # type: (str) -> str
    P = path

    # HACK: Improves the (still broken) output in some weird cases where
    # python gets confused about paths.
    real_abs_P = realpath(abspath(P))
    if isfile(real_abs_P):
        P = real_abs_P

    if P.endswith((".py", ".px")):
        P = P[:-3]

    sorted_pypaths = sorted(sys.path, key=lambda x: -len(x))
    for pypath in sorted_pypaths:
        pypath = realpath(pypath)
        P = P.replace(pypath + "/", "")

    P = P.replace("/", ".")
    return P


class MainType(Protocol):
    def __call__(self, argv: Sequence[str] = None) -> int:
        pass


def main_factory(
    parse_cli_args: Callable[[Sequence[str]], _T],
    run: Callable[[_T], int],
) -> MainType:
    """
    Returns a generic main() function to be used as a script's entry point.
    """

    def main(argv: Sequence[str] = None) -> int:
        if argv is None:
            argv = sys.argv

        args = parse_cli_args(argv)

        if hasattr(args, "debug"):
            debug: bool = getattr(args, "debug")
        else:
            debug = False

        if hasattr(args, "verbose"):
            verbose: bool = getattr(args, "verbose")
        else:
            verbose = False

        gutils.logging.configure(__file__, debug=debug, verbose=verbose)
        log.debug("args = {!r}", args)

        scriptname = shared.scriptname(inspect.stack())

        try:
            status = run(args)
        except KeyboardInterrupt:
            print(
                "Received SIGINT signal. Terminating {}...".format(scriptname)
            )
            return 0
        except Exception:
            log.exception(
                "An unrecoverable error has been raised. Terminating {}...",
                scriptname,
            )
            raise
        else:
            return status

    return main
