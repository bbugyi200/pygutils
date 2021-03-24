import inspect
from pathlib import Path
from typing import List, Union


# These types are imported from this module by other modules/scripts.
#
# Used to maintain Python<=3.7 compatibility.
try:
    from typing import Literal, Protocol  # pylint: disable=unused-import
except ImportError:
    try:
        from typing_extensions import Literal, Protocol  # type: ignore
    except ImportError:
        from collections import defaultdict
        from typing import Any

        class _ProtocolType:
            def __init__(self, *_args: Any, **_kwargs: Any) -> None:
                return None

            def __getitem__(self, key: Any) -> "_ProtocolType":
                return self

        Literal = defaultdict(lambda: str)  # type: ignore
        Protocol = _ProtocolType()  # type: ignore


PathLike = Union[str, Path]
StackType = List[inspect.FrameInfo]
