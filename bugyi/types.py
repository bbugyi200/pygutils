import inspect
from pathlib import Path
from typing import List, Union


# These types are imported from this module by other modules/scripts.
#
# Used to maintain Python<=3.7 compatibility.
try:
    from typing import Literal, Protocol  # pylint: disable=unused-import
except ImportError:
    from typing_extensions import Literal, Protocol  # type: ignore


PathLike = Union[str, Path]
StackType = List[inspect.FrameInfo]
