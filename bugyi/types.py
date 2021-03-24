from pathlib import Path
from typing import Union


# 'Protocol' is imported from this module by other modules/scripts.
try:
    from typing import Protocol  # pylint: disable=unused-import
except ImportError:
    try:
        from typing_extensions import Protocol  # type: ignore
    except ImportError:
        Protocol = object  # type: ignore


PathLike = Union[str, Path]
