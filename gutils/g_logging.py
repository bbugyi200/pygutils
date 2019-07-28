"""Automates Logging Initialization"""

import contextlib
import inspect
import logging
import types
from typing import *  # noqa: F401
from types import *  # noqa: F401


def getEasyLogger(name: str) -> logging.Logger:
    """Initializes Log Handlers

    Args:
        name: name of the logger to create and return.
    """
    log = logging.getLogger(name)
    _add_vdebug_level()

    log.setLevel(logging.VDEBUG)  # type: ignore

    formatter = _getFormatter(frame=inspect.stack()[1].frame)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    sh.setLevel(logging.INFO)

    log_file = f"/var/tmp/{name}.log"
    fh = logging.FileHandler(log_file)
    fh.setFormatter(
        _getFormatter(frame=inspect.stack()[1].frame, verbose=True)
    )
    fh.setLevel(logging.DEBUG)

    log.addHandler(fh)
    log.addHandler(sh)

    return log


def _add_vdebug_level() -> None:
    """Adds custom logging level for verbose debug logs."""
    VDEBUG_LEVEL_NUM = 5
    logging.addLevelName(VDEBUG_LEVEL_NUM, "VDEBUG")

    def vdebug(self: Type, message: str, *args: Any, **kwargs: Any) -> None:
        if self.isEnabledFor(VDEBUG_LEVEL_NUM):
            self._log(VDEBUG_LEVEL_NUM, message, args, **kwargs)

    logging.Logger.vdebug = vdebug  # type: ignore
    logging.VDEBUG = VDEBUG_LEVEL_NUM  # type: ignore


def _getFormatter(
    *, frame: FrameType = None, verbose: bool = False
) -> logging.Formatter:
    """Get log formatter.

    Args:
        frame (optional): frame obect (see inspect module).
        verbose: True if a more verbose log format is desired.

    Returns:
        logging.Formatter object.
    """
    if frame is None:
        frame = inspect.stack()[1].frame

    base_formatting = _get_log_fmt(frame)

    if verbose:
        formatter = logging.Formatter(
            "(%(asctime)s) {}".format(base_formatting),
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:
        formatter = logging.Formatter(base_formatting)

    return formatter


@contextlib.contextmanager
def context(
    log: logging.Logger,
    *,
    debug: bool = False,
    verbose: bool = False,
) -> Generator:
    """Exception handling context manager.

    Logs any exceptions that are thrown. Allows the reuse of common exception
    handling logic.
    """
    if debug:
        # must slice stack ([1:]) to cut off contextlib module
        _enableDebugMode(log, verbose=verbose)

    try:
        yield
    except Exception as e:
        log.exception(f'{type(e).__name__}: {str(e)}')
        raise


def _enableDebugMode(log: logging.Logger, *, verbose: bool) -> None:
    """Enables debug mode.

    Adds a FileHandler. Sets the logging level of this handler and any
    existing StreamHandlers to DEBUG.
    """

    level = logging.VDEBUG if verbose else logging.DEBUG  # type: ignore

    for handler in log.handlers:
        if not isinstance(handler, logging.StreamHandler):
            handler.setLevel(level)

    # return early if a FileHandler already exists
    for handler in log.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.setLevel(level)
            return

    log.debug("Debugging mode enabled.")


def _get_log_fmt(frame: FrameType) -> str:
    """Get Logging Format String

    Returns a log formatting string, which can be used as the first argument to
    the logging.Formatter constructor.

    Args:
        frame: frame object (see inspect module).
    """
    fmt = (
        "[%(levelname)s] <%(process)s{}> "
        "(%(filename)s:%(funcName)s:%(lineno)d) %(message)s"
    )

    basic_formatting = fmt.format("")
    thread_formatting = fmt.format(":%(threadName)s")

    if _has_threading(frame):
        return thread_formatting
    else:
        return basic_formatting


def _has_threading(frame: FrameType) -> bool:
    """
    Determines whether or not the given frame has the 'threading' module in
    scope.
    """
    try:
        return isinstance(frame.f_globals["threading"], types.ModuleType)
    except KeyError:
        return False
