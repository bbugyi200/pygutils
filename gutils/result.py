from typing import Any, Generic, NoReturn, Type, TypeVar, Union

from typing_extensions import Protocol


_T = TypeVar("_T")
_E = TypeVar("_E", bound=Exception)


class Ok(Generic[_T]):
    def __init__(self, value: _T) -> None:
        self._value = value

    def ok(self) -> _T:
        return self._value

    def unwrap(self) -> _T:
        return self.ok()


class Err(Generic[_E]):
    def __init__(self, e: _E) -> None:
        self._e = e

    def err(self) -> _E:
        return self._e

    def unwrap(self) -> NoReturn:
        raise self.err()


# The 'Result' return type is used to implement an error-handling model heavily
# influenced by that used by the Rust programming language
# (see https://doc.rust-lang.org/book/ch09-00-error-handling.html).
Result = Union[Ok[_T], Err[_E]]


class _ErrHelper(Protocol[_E]):
    def __call__(self, *args: Any) -> Err[_E]:
        pass


def init_err_helper(Error: Type[_E]) -> _ErrHelper[_E]:
    """
    Factory function which can be used to initialize a helper function for
    returning Err types.
    """

    def err_helper(*args: Any) -> Err[_E]:
        e = Error(*args)
        return Err(e)

    return err_helper
