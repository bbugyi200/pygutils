"""Helper functions for command-line argument parsing."""

import argparse
import inspect
from typing import Any


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
        "-d", "--debug", action="store_true", help="Enable debugging mode."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output."
    )

    return parser
