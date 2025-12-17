"""Base Result primitives and helpers."""

from __future__ import annotations

from collections.abc import Callable
from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")
F = TypeVar("F")


class Result(Generic[T, E]):
    """Base type for Ok/Err results."""

    __slots__ = ()

    def unwrap(self) -> T:
        """Return the contained value if successful, else raise in subclass."""
        raise NotImplementedError  # pragma: no cover

    def unwrap_err(self) -> E:
        """Return the contained error if Err, else raise in subclass."""
        raise NotImplementedError  # pragma: no cover

    def unwrap_or(self, default: T) -> T:
        """Return the contained value if Ok, otherwise return the default."""
        raise NotImplementedError  # pragma: no cover

    def unwrap_or_else(self, func: Callable[[E], T]) -> T:
        """Return the contained value if Ok, otherwise compute a default."""
        raise NotImplementedError  # pragma: no cover

    def expect(self, msg: str) -> T:
        """Return the contained value if Ok, otherwise raise with custom message."""
        raise NotImplementedError  # pragma: no cover

    def is_ok(self) -> bool:  # pragma: no cover
        """Return True if this is Ok."""
        from .ok import Ok

        return isinstance(self, Ok)

    def is_err(self) -> bool:  # pragma: no cover
        """Return True if this is Err."""
        from .err import Err

        return isinstance(self, Err)

    def map(self, func: Callable[[T], U]) -> Result[U, E]:
        """Apply func to the contained value if Ok, returning a new Result."""
        raise NotImplementedError  # pragma: no cover

    def map_err(self, func: Callable[[E], F]) -> Result[T, F]:
        """Apply func to the error if Err, returning a new Result."""
        raise NotImplementedError  # pragma: no cover

    def and_then(self, func: Callable[[T], Result[U, E]]) -> Result[U, E]:
        """Chain another computation on the contained value if Ok."""
        raise NotImplementedError  # pragma: no cover

    def or_else(self, func: Callable[[E], Result[T, F]]) -> Result[T, F]:
        """Handle the error by calling func if Err, returning a new Result."""
        raise NotImplementedError  # pragma: no cover

    def ok(self) -> T | None:
        """Return the success value if Ok, otherwise None."""
        raise NotImplementedError  # pragma: no cover

    def err(self) -> E:
        """Return the error value if Err, otherwise raise in subclass."""
        raise NotImplementedError  # pragma: no cover

    @property
    def error(self) -> E | None:
        """Return the error value if Err, otherwise None."""
        return self.err()

    def unwrap_or_raise(
        self,
        exc_type: type[BaseException] = Exception,
        context: str | None = None,
    ) -> T:
        """Return the Ok value or raise `exc_type`."""
        raise NotImplementedError  # pragma: no cover
