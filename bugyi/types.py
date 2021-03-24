import inspect
from pathlib import Path
from typing import List, Union


# The below 'typing' module types are imported from this module by other
# modules/scripts.
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

        class _ProtocolMock:
            def __init__(self, *_args: Any, **_kwargs: Any) -> None:
                return None

            def __getitem__(self, _key: Any) -> "_ProtocolMock":
                return self

        Literal = defaultdict(lambda: str)  # type: ignore
        Protocol = _ProtocolMock()  # type: ignore


PathLike = Union[str, Path]
StackType = List[inspect.FrameInfo]
