import subprocess as sp

from bugyi import subprocess as bsp
from bugyi.core import scriptname
from bugyi.errors import BResult, Err, Ok


def get_pass(key: str) -> BResult[str]:
    out_err_r = bsp.safe_popen(["pass", "show", key])
    if isinstance(out_err_r, Err):
        return out_err_r

    password, _err = out_err_r.ok()
    return Ok(password)


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


def notify(
    *args: str, title: str = None, urgency: str = None, up: int = 0
) -> None:
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
        title = scriptname(up=up + 1)

    cmd_list = ["notify-send"]
    cmd_list.extend([title])

    if urgency is not None:
        cmd_list.extend(["-u", urgency])

    cmd_list.extend(args)

    sp.check_call(cmd_list)
