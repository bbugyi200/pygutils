from collections import defaultdict
from pathlib import Path
from typing import Any, Type, TypeVar, Union


_T = TypeVar("_T")


# The below 'typing' module types are imported from this module by other
# modules/scripts.
#
# Used to maintain Python<=3.7 compatibility.
try:
    from typing import (  # pylint: disable=unused-import
        Final,
        Literal,
        Protocol,
    )
except ImportError:
    try:
        from typing_extension import Final, Literal, Protocol  # type: ignore
    except ImportError:

        class _FinalMock(type):
            def __getitem__(cls, key: Type[_T]) -> Type[_T]:
                return key

        class _ProtocolMock(type):
            def __getitem__(cls, _key: Any) -> "_ProtocolMock":
                return cls

        Final = _FinalMock("Final", (object,), {})  # type: ignore
        Literal = defaultdict(lambda: str)  # type: ignore
        Protocol = _ProtocolMock("Protocol", (object,), {})  # type: ignore


PathLike = Union[str, Path]
