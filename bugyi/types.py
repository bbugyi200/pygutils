from pathlib import Path
from typing import Union


# These types are imported from this module by other modules/scripts.
try:
    from typing import Literal, Protocol  # pylint: disable=unused-import
except ImportError:
    from typing_extensions import Literal, Protocol  # type: ignore


PathLike = Union[str, Path]
