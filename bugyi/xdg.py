"""XDG Utilities"""

from functools import partial
import os
from pathlib import Path
from typing import Any, Callable, Dict, Tuple

from .meta import deprecated, scriptname
from .types import Literal


XDG_Type = Literal["cache", "config", "data", "runtime"]

_home = os.environ.get("HOME")
# Mapping of XDG directory types to 2-tuples of the form (envvar, default_dir).
_xdg_type_map: Dict[XDG_Type, Tuple[str, str]] = {
    "cache": ("XDG_CACHE_HOME", f"{_home}/.cache"),
    "config": ("XDG_CONFIG_HOME", f"{_home}/.config"),
    "data": ("XDG_DATA_HOME", f"{_home}/.local/share"),
    "runtime": ("XDG_RUNTIME_DIR", "/tmp"),
}


def init_full_dir(xdg_type: XDG_Type, *, up: int = 0) -> Path:
    """
    Returns:
        Full XDG user directory (including scriptname).

    Side Effects:
        Ensures the full XDG user directory exists before returning it.
    """
    full_xdg_dir = get_full_dir(xdg_type, up=up + 1)
    full_xdg_dir.mkdir(parents=True, exist_ok=True)
    return full_xdg_dir


def get_full_dir(xdg_type: XDG_Type, *, up: int = 0) -> Path:
    """
    Returns:
        Full XDG user directory (including scriptname).
    """
    base_xdg_dir = get_base_dir(xdg_type)
    full_xdg_dir = base_xdg_dir / scriptname(up=up + 1)
    return full_xdg_dir


def get_base_dir(xdg_type: XDG_Type) -> Path:
    """
    Returns:
        The base/general XDG user directory.
    """
    assert (
        xdg_type in _xdg_type_map
    ), "Provided @xdg_type parameter is not valid: {!r} not in {}".format(
        xdg_type, list(_xdg_type_map.keys())
    )

    envvar, default_dir = _xdg_type_map[xdg_type]
    xdg_dir = Path(os.environ.get(envvar, default_dir))
    return xdg_dir


def _deprecated_func(old_name: str, func: Callable, **kwargs: Any) -> Callable:
    return deprecated(
        partial(func, **kwargs),
        f"The '{old_name}' function is deprecated. Use the '{func.__name__}'"
        " function instead.",
    )


init = _deprecated_func("init", init_full_dir, up=1)
get = _deprecated_func("get", get_base_dir)
