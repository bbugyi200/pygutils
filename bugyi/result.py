from functools import wraps
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    NoReturn,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

from .io import efill
from .meta import cname


_T = TypeVar("_T")
_E = TypeVar("_E", bound=Exception)


class Ok(Generic[_T]):
    def __init__(self, value: _T) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"{cname(self)}({self.ok()!r})"

    def __bool__(self) -> NoReturn:
        _raise_bool_error(self)

    @staticmethod
    def err() -> None:
        return None

    def ok(self) -> _T:
        return self._value

    def unwrap(self) -> _T:
        return self.ok()


class Err(Generic[_E]):
    def __init__(self, e: _E) -> None:
        self._e = e

    def __repr__(self) -> str:
        return f"{cname(self)}(\n{efill(str(self.err()), indent=2)}\n)"

    def __bool__(self) -> NoReturn:
        _raise_bool_error(self)

    def err(self) -> _E:
        return self._e

    def unwrap(self) -> NoReturn:
        raise self.err()


# The 'Result' return type is used to implement an error-handling model heavily
# influenced by that used by the Rust programming language
# (see https://doc.rust-lang.org/book/ch09-00-error-handling.html).
Result = Union[Ok[_T], Err[_E]]


def return_lazy_result(
    func: Callable[..., Result[_T, _E]]
) -> Callable[..., "_LazyResult[_T, _E]"]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> _LazyResult[_T, _E]:
        return _LazyResult(func, *args, **kwargs)

    return wrapper


class _LazyResult(Generic[_T, _E]):
    def __init__(
        self, func: Callable[..., Result[_T, _E]], *args: Any, **kwargs: Any
    ) -> None:
        self._func = func
        self._args: Tuple[Any, ...] = args
        self._kwargs: Dict[str, Any] = kwargs

        self._result: Optional[Result[_T, _E]] = None

    def __bool__(self) -> NoReturn:
        _raise_bool_error(self)

    def result(self) -> Result[_T, _E]:
        if self._result is None:
            self._result = self._func(*self._args, **self._kwargs)
        return self._result

    def err(self) -> Optional[_E]:
        return self.result().err()

    def unwrap(self) -> _T:
        return self.result().unwrap()


def _raise_bool_error(self: Any) -> NoReturn:
    raise NotImplementedError(
        f"{cname(self)} object ({self!r}) cannot be evaluated as a boolean."
        " This is probably a bug in your code. Make sure you are either"
        " explicitly checking for Err results or using the `Result.unwrap()`"
        " method."
    )
