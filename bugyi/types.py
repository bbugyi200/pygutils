from collections import defaultdict
from pathlib import Path
from typing import Any, Type, TypeVar, Union


E = TypeVar("E", bound=Exception)
T = TypeVar("T")

PathLike = Union[str, Path]

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
        class _FinalMock:
            def __getitem__(self, key: Type[T]) -> Type[T]:
                return key

        class _ProtocolMock(type):
            def __getitem__(cls, _key: Any) -> "_ProtocolMock":
                return cls

        Final = _FinalMock()  # type: ignore
        Literal = defaultdict(lambda: str)  # type: ignore
        Protocol = _ProtocolMock("Protocol", (object,), {})  # type: ignore
