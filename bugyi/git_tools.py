import sys
from typing import Iterable, List, NamedTuple

from . import subprocess as bsp
from .errors import BResult, Err, Ok


def top_level_dir(cwd: str = None) -> BResult[str]:
    """
    Returns:
        The full path of top-level directory which contains the .git directory.
    """
    out_err_r = bsp.safe_popen(
        ["git", "rev-parse", "--show-toplevel"], cwd=cwd
    )
    if isinstance(out_err_r, Err):
        return out_err_r
    else:
        out, _err = out_err_r.ok()
        return Ok(out)


class GitRemote(NamedTuple):
    name: str
    url: str


def remotes() -> BResult[List[GitRemote]]:
    """Python wrapper around the `git remote -v` command."""
    out_err_r = bsp.safe_popen(["git", "remote", "-v"])
    if isinstance(out_err_r, Err):
        return out_err_r

    out, _err = out_err_r.ok()

    all_remotes = []
    for line in out.split("\n"):
        line_split = line.split()
        if len(line_split) < 2:
            continue

        remote = GitRemote(str(line_split[0]), str(line_split[1]))
        if remote not in all_remotes:
            all_remotes.append(remote)

    return Ok(all_remotes)


def local_branch_exists(branch: str) -> BResult[bool]:
    return _branch_exists(["git", "branch", "--list", branch])


def remote_branch_exists(remote, branch):
    # type: (str, str) -> BResult[bool]
    return _branch_exists(["git", "ls-remote", "--heads", remote, branch])


def _branch_exists(cmd_parts: Iterable[str]) -> BResult[bool]:
    out_err_r = bsp.safe_popen(list(cmd_parts))
    if isinstance(out_err_r, Err):
        return out_err_r
    else:
        out, _err = out_err_r.ok()
        return Ok(bool(out))


def checkout(branch: str, template_branch: str = None) -> BResult[None]:
    cmd_list = ["git", "checkout"]
    if template_branch is None:
        cmd_list.append(branch)
    else:
        cmd_list.extend(["-b", branch, template_branch])

    r = bsp.safe_popen(cmd_list, stdout=sys.stdout)
    if isinstance(r, Err):
        return r

    return Ok(None)


def pull() -> BResult[None]:
    return _git_cmd("pull")


def fetch(remote: str = None) -> BResult[None]:
    if remote is None:
        opts = ["--all"]
    else:
        opts = [remote]

    return _git_cmd("fetch", *opts)


def add_remote(name: str, url: str) -> BResult[None]:
    return _git_cmd("remote", "add", name, url)


def _git_cmd(cmd: str, *opts: str) -> BResult[None]:
    cmd_list = ["git", cmd]
    cmd_list.extend(opts)
    r = bsp.safe_popen(cmd_list, stdout=sys.stdout)
    if isinstance(r, Err):
        return r

    return Ok(None)


def current_branch() -> BResult[str]:
    ref_r = bsp.safe_popen(["git", "symbolic-ref", "--quiet", "HEAD"])
    if isinstance(ref_r, Err):
        return ref_r

    ref, _ = ref_r.ok()
    return Ok(ref.split("/")[-1])
