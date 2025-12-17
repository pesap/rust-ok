from __future__ import annotations

from typing import Any, assert_type

from rust_ok import Err, Ok, Result, is_ok


def returns_any_result() -> Result[Any, str]:
    return Ok()


def test_bare_ok_satisfies_result_any() -> None:
    success: Result[Any, str] = Ok()

    assert is_ok(success)
    if is_ok(success):
        _ = success.value  # value is Any when constructed with Ok()


def test_ok_none_preserves_none_payload() -> None:
    res: Result[None, str] = Ok(None)
    assert is_ok(res)
    assert res.value is None


def test_function_returning_any_result_type_checks() -> None:
    res = returns_any_result()
    assert_type(res, Result[Any, str])
    assert is_ok(res)


def returns_result_with_any_error() -> Result[int, Any]:
    return Err("boom")


def test_err_with_any_error_type_checks() -> None:
    err_res = returns_result_with_any_error()
    assert not err_res
