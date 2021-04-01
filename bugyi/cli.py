"""Helper functions for command-line argument parsing."""

import argparse
from dataclasses import dataclass
import inspect
from typing import Any


@dataclass
class Arguments:
    debug: bool
    verbose: int


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
        "-d",
        "--debug",
        action="store_true",
        help="Enable debugging mode. DEPRECIATED: Use --verbose instead.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        help=(
            "How verbose should the output be? This option can be specified"
            " multiple times."
        ),
    )

    return parser
