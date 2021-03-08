import subprocess as sp
from typing import Any, Iterable, List, Tuple

from gutils.errors import BErr, BResult, BugyiError, Err, Ok


def safe_popen(cmd_parts, **kwargs):
    # type: (Iterable[str], Any) -> BResult[Tuple[str, str]]
    """Wrapper for subprocess.Popen(...).

    Returns:
        Ok((out, err)) if the command is successful.
            OR
        Err(BugyiError) otherwise.
    """
    cmd_list = list(cmd_parts)

    if "stdout" not in kwargs:
        kwargs["stdout"] = sp.PIPE

    if "stderr" not in kwargs:
        kwargs["stderr"] = sp.PIPE

    ps = sp.Popen(cmd_list, **kwargs)

    proc = DoneProcess(ps, cmd_list)
    if ps.returncode != 0:
        return proc.to_error(up=1)

    return Ok((proc.out, proc.err))


def unsafe_popen(cmd_parts, **kwargs):
    # type: (Iterable[str], Any) -> Tuple[str, str]
    """Wrapper for subprocess.Popen(...)

    You can use unsafe_popen() instead of safe_popen() when you don't care
    whether or not the command succeeds.

    Returns: (out, err)
    """
    cmd_list = list(cmd_parts)

    if "stdout" not in kwargs:
        kwargs["stdout"] = sp.PIPE

    if "stderr" not in kwargs:
        kwargs["stderr"] = sp.PIPE

    ps = sp.Popen(cmd_list, **kwargs)
    proc = DoneProcess(ps, cmd_list)

    return (proc.out, proc.err)


class DoneProcess:
    def __init__(self, ps, cmd_list):
        # type: (sp.Popen, List[str]) -> None
        self.ps = ps
        self.cmd_list = cmd_list

        stdout, stderr = ps.communicate()
        self.out = "" if stdout is None else str(stdout.decode().strip())
        self.err = "" if stderr is None else str(stderr.decode().strip())

    def to_error(self, up=0):
        # type: (int) -> Err[BugyiError]
        maybe_out = ""
        if self.out:
            maybe_out = "\n\n----- STDOUT\n{}".format(self.out)

        maybe_err = ""
        if self.err:
            maybe_err = "\n\n----- STDERR\n{}".format(self.err)

        return BErr(
            "Command Failed: %r%s%s",
            self.cmd_list,
            maybe_out,
            maybe_err,
            up=up + 1,
        )
