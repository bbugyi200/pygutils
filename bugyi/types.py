from collections import defaultdict
from pathlib import Path
from typing import Any, Union


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

        class _ProtocolMock(type):
            def __getitem__(cls, _key: Any) -> "_ProtocolMock":
                return cls

        Literal = defaultdict(lambda: str)  # type: ignore
        Protocol = _ProtocolMock("Protocol", (object,), {})  # type: ignore


PathLike = Union[str, Path]
