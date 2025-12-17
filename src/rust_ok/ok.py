"""Implementation of the Ok variant."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal, TypeVar, cast, overload

from .exceptions import IsNotError, UnwrapError
from .result import Result

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")
F = TypeVar("F")


class Ok(Result[T, E]):
    """Success result containing a value."""

    __slots__ = ("value",)
    __match_args__ = ("value",)

    value: T

    @overload
    def __init__(self: Ok[Any, Any]) -> None: ...

    @overload
    def __init__(self: Ok[None, E], value: Literal[None]) -> None: ...

    @overload
    def __init__(self: Ok[T, E], value: T) -> None: ...

    def __init__(self, value: T | None = None) -> None:
        self.value = cast(T, value)

    def __repr__(self) -> str:
        return f"Ok({self.value!r})"

    def __str__(self) -> str:
        return f"Ok({self.value})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ok):
            return bool(self.value == other.value)
        return False

    def __hash__(self) -> int:
        return hash(("Ok", self.value))

    def __bool__(self) -> bool:
        return True

    def unwrap(self) -> T:
        return self.value

    def unwrap_err(self) -> E:
        raise UnwrapError("Called unwrap_err on Ok")

    def unwrap_or(self, default: T) -> T:
        return self.value

    def unwrap_or_else(self, func: Callable[[E], T]) -> T:
        return self.value

    def expect(self, msg: str) -> T:
        return self.value

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def map(self, func: Callable[[T], U]) -> Result[U, E]:
        return Ok(func(self.value))

    def map_err(self, func: Callable[[E], F]) -> Result[T, F]:
        return cast(Result[T, F], Ok(self.value))

    def and_then(self, func: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return func(self.value)

    def or_else(self, func: Callable[[E], Result[T, F]]) -> Result[T, F]:
        return cast(Result[T, F], Ok(self.value))

    def ok(self) -> T:
        return self.value

    def err(self) -> E:
        raise IsNotError

    def unwrap_or_raise(
        self,
        exc_type: type[BaseException] = Exception,
        context: str | None = None,
    ) -> T:
        return self.value
