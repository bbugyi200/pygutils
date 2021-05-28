import os
from pathlib import Path

import pytest

import bugyi
from bugyi.xdg import XDG_Type


_xdg_params = [
    ("config", "/home/bryan/.config"),
    ("data", "/home/bryan/.local/share"),
    ("runtime", "/run/user/1000"),
    ("cache", "/home/bryan/.cache"),
]
xdg_params = [(x, Path(y)) for x, y in _xdg_params]


@pytest.mark.parametrize("key,expected_part", xdg_params)
def test_xdg_init(key: XDG_Type, expected_part: Path) -> None:
    expected = expected_part / "test_xdg"
    assert expected == bugyi.xdg.init_full_dir(key)
    os.rmdir(expected)


@pytest.mark.parametrize("key,expected", xdg_params)
def test_xdg_get(key: XDG_Type, expected: Path) -> None:
    assert expected == bugyi.xdg.get_base_dir(key)


def test_init_failure() -> None:
    with pytest.raises(AssertionError):
        bugyi.xdg.init("bad_key")  # type: ignore
