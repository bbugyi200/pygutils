import traceback
from typing import (
    Any,
    Generic,
    Iterator,
    List,
    NoReturn,
    Optional,
    Type,
    TypeVar,
    Union,
)

from typing_extensions import Protocol

from gutils import Inspector, cname, efill, ewrap


_T = TypeVar("_T")
_E = TypeVar("_E", bound=Exception)


class Ok(Generic[_T]):
    def __init__(self, value: _T) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"{cname(self)}({self.ok()!r})"

    def ok(self) -> _T:
        return self._value

    def unwrap(self) -> _T:
        return self.ok()


class Err(Generic[_E]):
    def __init__(self, e: _E) -> None:
        self._e = e

    def __repr__(self) -> str:
        return f"{cname(self)}(\n{efill(str(self.err()), indent=2)}\n)"

    def err(self) -> _E:
        return self._e

    def unwrap(self) -> NoReturn:
        raise self.err()


# The 'Result' return type is used to implement an error-handling model heavily
# influenced by that used by the Rust programming language
# (see https://doc.rust-lang.org/book/ch09-00-error-handling.html).
Result = Union[Ok[_T], Err[_E]]


class _ErrHelper(Protocol[_E]):
    def __call__(self, *args: Any, **kwargs: Any) -> Err[_E]:
        pass


def init_err_helper(Error: Type[_E]) -> _ErrHelper[_E]:
    """
    Factory function which can be used to initialize a helper function for
    returning Err types.
    """

    def err_helper(*args: Any, **kwargs: Any) -> Err[_E]:
        e = Error(*args, **kwargs)  # type: ignore
        return Err(e)

    return err_helper


class BugyiError(Exception):
    def __init__(self, emsg, **kwargs):
        # type: (str, Any) -> None
        cause = kwargs.get("cause", None)
        assert issubclass(type(cause), (type(None), Exception))

        up = kwargs.get("up", 0) + 1
        assert up >= 1

        if cause is not None and not hasattr(cause, "__cause__"):
            chain_errors(cause, None)

        chain_errors(self, cause)

        self.inspector = Inspector(up=up)

        super().__init__(emsg)

    def __repr__(self):
        # type: () -> str
        return self._repr()

    def _repr(self, width=80):
        # type: (Optional[int]) -> str
        """
        Format error to width.  If width is None, return string suitable for traceback.
        """
        super_str = super().__str__()

        if width is None:
            return 'At "{}", line {}, in {}:\n  {}\n{}'.format(
                self.inspector.file_name,
                self.inspector.line_number,
                self.inspector.function_name,
                self.inspector.lines.strip(),
                super_str,
            )

        emsg = efill(super_str, width, indent=2)
        return "{}::{}::{}::{}{{\n{}\n}}".format(
            cname(self),
            self.inspector.module_name,
            self.inspector.function_name,
            self.inspector.line_number,
            emsg,
        )

    def __iter__(self):
        # type: () -> Iterator[BaseException]
        yield self

        e = self.__cause__
        while e:
            yield e
            e = e.__cause__

    def report(self, width=80):
        # type: (int) -> ErrorReport
        """
        Return an ErrorReport object formatting the current state of this BugyiError
        """
        TITLE = cname(self)
        MIDDLE_MSG = "was the direct cause of"

        H_CH = "-"  # Horizontal Character
        V_CH = "|"  # Vertical Character
        S_CH = "*"  # Special Character

        nleft_spaces, rem = divmod(width - len(TITLE), 2)
        if rem == 0:
            nright_spaces = nleft_spaces
        else:
            nright_spaces = nleft_spaces + 1

        header = "{0}{1}{2}{3}{0}".format(
            V_CH, " " * nleft_spaces, TITLE, " " * nright_spaces
        )

        minibar_length, rem = divmod(width - len(MIDDLE_MSG), 4)
        left_minibar = (H_CH + S_CH) * minibar_length
        right_minibar = (S_CH + H_CH) * minibar_length

        if rem >= 2:
            left_minibar += H_CH
            right_minibar = S_CH + right_minibar

        if rem % 2 != 0:
            right_minibar = H_CH + right_minibar

        middle_header = "{0} {1} {2}".format(left_minibar, MIDDLE_MSG, right_minibar)

        dashes = "-" * len(header)

        # >>> Put everything together into a ErrorReport object.
        report = ErrorReport("\n", border_ch=V_CH)
        report += "{0}\n{1}\n{0}\n".format(dashes, header)
        for i, error in enumerate(reversed(list(self))):
            w = width - 2
            error_string = _tb_or_repr(error, width=w)
            if i != 0:
                report += "{0}\n{1}\n{0}\n".format(dashes, middle_header)

            for line in ewrap(error_string, w):
                right_spaces = " " * (width - len(line) - 2)
                report += "{0} {1}{2} {0}\n".format(V_CH, line, right_spaces)

        report += dashes
        return report


BErr = init_err_helper(BugyiError)
BResult = Result[_T, BugyiError]


class ErrorReport:
    def __init__(self, chunk=None, border_ch="|"):
        # type: (str, str) -> None
        self.report_lines = []  # type: List[_ErrorReportLine]
        self.border_ch = border_ch
        if chunk is not None:
            self._add_chunk(chunk)

    def __str__(self):
        # type: () -> str
        self._close_borders()
        return "".join(rl.line + rl.newlines for rl in self.report_lines)

    def __iadd__(self, chunk):
        # type: (str) -> ErrorReport
        self._add_chunk(chunk)
        return self

    def _add_chunk(self, chunk):
        # type: (str) -> None
        if not chunk:
            return

        chunk_split = chunk.split("\n")
        for i, line in enumerate(chunk_split):
            if len(chunk_split) == 1 or i < len(chunk_split) - 1:
                if self.report_lines:
                    self.report_lines[-1].newlines += "\n"
                else:
                    rline = _ErrorReportLine("", "")
                    self.report_lines.append(rline)

            if line:
                rline = _ErrorReportLine(line, "")
                self.report_lines.append(rline)

    def _close_borders(self):
        # type: () -> None
        for i, rline in enumerate(self.report_lines[:]):
            V_CH = self.border_ch
            if not rline.line:
                continue

            self.report_lines[i].line = V_CH + rline.line[1:-1] + V_CH

        V_CH = "+"  # report box corners
        for i, inc in [(0, 1), (-1, -1)]:
            j = i
            while 0 <= j < len(self.report_lines) and not self.report_lines[j].line:
                j += inc

            rline = self.report_lines[j]
            self.report_lines[j].line = V_CH + rline.line[1:-1] + V_CH


class _ErrorReportLine:
    def __init__(self, line, newlines):
        # type: (str, str) -> None
        self.line = line
        self.newlines = newlines

    def __str__(self):
        # type: () -> str
        return "{}(line={!r}, newlines={!r})".format(
            cname(self), self.line, self.newlines
        )


def _tb_or_repr(e, width):
    # type: (BaseException, Optional[int]) -> str
    if isinstance(e, BugyiError):
        return e._repr(width=width)
    else:
        tb = getattr(e, "__traceback__", None)
        if tb is not None:
            estring = "".join(traceback.format_exception(type(e), e, tb))
        else:
            estring = repr(e)
        return estring


def chain_errors(e1, e2):
    # type: (_E, Optional[Exception]) -> _E
    e = e1
    while getattr(e, "__cause__", None):
        e = getattr(e, "__cause__")
    setattr(e, "__cause__", e2)
    return e1
