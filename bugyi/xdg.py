"""XDG Utilities"""

import inspect
import os
from pathlib import Path

import bugyi.shared as shared


_home = os.environ.get('HOME')
_xdg_vals = {
    "config": ("XDG_CONFIG_HOME", f"{_home}/.config"),
    "data": ("XDG_DATA_HOME", f"{_home}/.local/share"),
    "runtime": ("XDG_RUNTIME_DIR", "/tmp"),
    "cache": ("XDG_CACHE_HOME", f"{_home}/.cache"),
}


def init(userdir: str, stack: shared.StackType = None) -> Path:
    """ Get XDG User Directory.

    Args:
        userdir (str): one of the four defined XDG user directories
            ('config', 'data', 'runtime', or 'cache').
        stack (optional): stack object (see inspect module)

    Returns:
        Full user directory path, as specified by the XDG standard.
    """
    if stack is None:
        stack = inspect.stack()

    scriptname = shared.scriptname(stack)

    full_xdg_dir = Path("{}/{}".format(get(userdir), scriptname))
    full_xdg_dir.mkdir(parents=True, exist_ok=True)

    return full_xdg_dir


def get(userdir: str) -> Path:
    userdir = userdir.lower()
    userdir_opts = {"config", "data", "runtime", "cache"}
    if userdir not in userdir_opts:
        raise ValueError(
            "Argument @userdir MUST be one of the following "
            "options: {}".format(userdir_opts)
        )

    envvar, dirfmt = _xdg_vals[userdir]
    xdg_dir = _get(envvar, dirfmt)
    return xdg_dir


def _get(envvar: str, default_dir: str) -> Path:
    if envvar in os.environ:
        xdg_dir = os.environ[envvar]
    else:
        xdg_dir = default_dir

    return Path(xdg_dir)
