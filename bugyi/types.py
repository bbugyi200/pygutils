from pathlib import Path
from typing import Union


try:
    from typing import Protocol as protocol_type
except ImportError:
    protocol_type = object  # type: ignore


PathLike = Union[str, Path]
Protocol = protocol_type
