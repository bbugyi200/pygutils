"""XDG Utilities"""

import inspect
import os
from pathlib import Path

import bugyi.shared as shared
from bugyi.types import StackType


_home = os.environ.get("HOME")
# Mapping of XDG directory types to 2-tuples of the form (envvar, default_dir).
_xdg_type_map = {
    "config": ("XDG_CONFIG_HOME", f"{_home}/.config"),
    "data": ("XDG_DATA_HOME", f"{_home}/.local/share"),
    "runtime": ("XDG_RUNTIME_DIR", "/tmp"),
    "cache": ("XDG_CACHE_HOME", f"{_home}/.cache"),
}


def init_full_dir(xdg_type: str, stack: StackType = None) -> Path:
    """
    Returns:
        Full XDG user directory (including scriptname).

    Side Effects:
        Ensures the full XDG user directory exists before returning it.
    """
    if stack is None:
        stack = inspect.stack()

    full_xdg_dir = get_full_dir(xdg_type, stack)
    full_xdg_dir.mkdir(parents=True, exist_ok=True)
    return full_xdg_dir


def get_full_dir(xdg_type: str, stack: StackType = None) -> Path:
    """
    Returns:
        Full XDG user directory (including scriptname).
    """
    if stack is None:
        stack = inspect.stack()

    scriptname = shared.scriptname(stack)
    base_xdg_dir = get_base_dir(xdg_type)
    full_xdg_dir = base_xdg_dir / scriptname
    return full_xdg_dir


def get_base_dir(xdg_type: str) -> Path:
    """
    Returns:
        The base/general XDG user directory.
    """
    xdg_type = xdg_type.lower()
    xdg_type_choices = {"config", "data", "runtime", "cache"}
    if xdg_type not in xdg_type_choices:
        raise ValueError(
            "Argument @xdg_type MUST be one of the following "
            "options: {}".format(xdg_type_choices)
        )

    envvar, default_dir = _xdg_type_map[xdg_type]
    xdg_dir = _get_base_dir(envvar, default_dir)
    return xdg_dir


def _get_base_dir(envvar: str, default_dir: str) -> Path:
    if envvar in os.environ:
        xdg_dir = os.environ[envvar]
    else:
        xdg_dir = default_dir

    return Path(xdg_dir)


# DEPRECIATED: Use newer, more descriptive function names instead.
init = init_full_dir
get = get_base_dir
