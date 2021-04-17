import atexit
import errno
import os
import random
import signal as sig
import string
import subprocess as sp
import sys
from textwrap import wrap
from typing import Callable, Iterator, Sequence, TypeVar

from loguru import logger as log

from .types import Protocol


_T = TypeVar("_T")


def catch(func: Callable) -> Callable:
    """Wrapper for loguru.logger.catch

    DEPRECIATED: Use the main_factory() function instead.
    """
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


def secret() -> str:
    """Get Secret String for Use with secret.sh Script"""
    from bugyi.meta import scriptname

    secret_key = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(16)
    )
    fp = "/tmp/{}.secret".format(scriptname(up=1))

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
    """Run Shell Command(s)

    DEPRECIATED: Use the bugyi.subprocess module's functions instead.
    """
    out = sp.check_output("; ".join(cmds), shell=True)
    return out.decode().strip()


def signal(*signums: int) -> Callable:
    """A decorator for registering signal handlers."""

    def _signal(handler: Callable) -> Callable:
        for signum in signums:
            sig.signal(signum, handler)

        return handler

    return _signal


def ewrap(
    multiline_msg: str, width: int = 80, indent: int = 0
) -> Iterator[str]:
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


def efill(multiline_msg: str, width: int = 80, indent: int = 0) -> str:
    """A better version of textwrap.fill()."""
    return "\n".join(ewrap(multiline_msg, width, indent))


class _MainType(Protocol):
    def __call__(self, argv: Sequence[str] = None) -> int:
        pass


def main_factory(
    parse_cli_args: Callable[[Sequence[str]], _T], run: Callable[[_T], int]
) -> _MainType:
    """
    Returns a generic main() function to be used as a script's entry point.
    """
    from bugyi.logging import configure as configure_logging
    from bugyi.meta import scriptname

    def main(argv: Sequence[str] = None) -> int:
        if argv is None:
            argv = sys.argv

        args = parse_cli_args(argv)

        debug: bool = getattr(args, "debug", False)
        verbose: int = getattr(args, "verbose", 0)
        name = scriptname(up=1)

        configure_logging(name, debug=debug, verbose=verbose)

        log.trace("Trace mode has been enabled.")
        log.debug("args = {!r}", args)

        try:
            status = run(args)
        except KeyboardInterrupt:
            print("Received SIGINT signal. Terminating {}...".format(name))
            return 0
        except Exception:
            log.exception(
                "An unrecoverable error has been raised. Terminating {}...",
                name,
            )
            return 1
        else:
            return status

    return main
