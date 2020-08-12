from typing import Callable, Generic, Type, TypeVar, Union


_T = TypeVar("_T")
_E = TypeVar("_E", bound=Exception)


class Ok(Generic[_T]):
    def __init__(self, value: _T) -> None:
        self._value = value

    def ok(self) -> _T:
        return self._value


class Err(Generic[_E]):
    def __init__(self, e: _E) -> None:
        self._e = e

    def err(self) -> _E:
        return self._e


# The 'Result' return type is used to implement an error-handling model heavily
# influenced by that used by the Rust programming language
# (see https://doc.rust-lang.org/book/ch09-00-error-handling.html).
Result = Union[Ok[_T], Err[_E]]


def InitErrHelper(Error: Type[_E]) -> Callable[[str], Err[_E]]:
    """
    Factory function which can be used to initialize a helper function for
    returning Err types.
    """
    def ErrHelper(emsg: str) -> Err[_E]:
        e = Error(emsg)
        return Err(e)

    return ErrHelper
