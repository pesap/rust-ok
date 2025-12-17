"""Implementation of the Err variant."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar, cast, overload

from .exceptions import UnwrapError
from .result import Result

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")
F = TypeVar("F")


class Err(Result[T, E]):
    """Error result containing an error value."""

    __slots__ = ("_error_value",)
    __match_args__ = ("error",)

    @overload
    def __init__(self: Err[T, E], error: E) -> None: ...

    @overload
    def __init__(self: Err[T, Any], error: Any) -> None: ...

    def __init__(self, error: E | Any) -> None:
        self._error_value = cast(E, error)

    def __repr__(self) -> str:
        return f"Err({self._error_value!r})"

    def __str__(self) -> str:
        return f"Err({self._error_value})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Err):
            return bool(self._error_value == other._error_value)
        return False

    def __hash__(self) -> int:
        return hash(("Err", self._error_value))

    def __bool__(self) -> bool:
        return False

    def unwrap(self) -> T:
        raise UnwrapError(f"Called unwrap on Err: {self._error_value}")

    def unwrap_err(self) -> E:
        return self._error_value

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, func: Callable[[E], T]) -> T:
        return func(self._error_value)

    def expect(self, msg: str) -> T:
        raise UnwrapError(f"{msg}: {self._error_value}")

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def map(self, func: Callable[[T], U]) -> Result[U, E]:
        return Err(self._error_value)

    def map_err(self, func: Callable[[E], F]) -> Result[T, F]:
        return Err(func(self._error_value))

    def and_then(self, func: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return Err(self._error_value)

    def or_else(self, func: Callable[[E], Result[T, F]]) -> Result[T, F]:
        return func(self._error_value)

    def ok(self) -> T | None:
        return None

    def err(self) -> E:
        return self._error_value

    def unwrap_or_raise(
        self,
        exc_type: type[BaseException] = Exception,
        context: str | None = None,
    ) -> T:
        payload = self._error_value
        msg = context if context is not None else str(payload)

        if isinstance(payload, BaseException):
            raise exc_type(msg) from payload

        raise exc_type(f"{msg}: {payload!r}")
