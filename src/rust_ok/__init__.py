"""Public API for rust-ok."""

from .exceptions import IsNotError, RustOkError, UnwrapError
from .err import Err
from .ok import Ok
from .guards import is_err, is_ok
from .result import Result
from .trace import format_exception_chain, iter_causes

__all__ = [
    "Err",
    "IsNotError",
    "Ok",
    "Result",
    "RustOkError",
    "UnwrapError",
    "format_exception_chain",
    "iter_causes",
    "is_err",
    "is_ok",
]
