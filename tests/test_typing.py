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


def test_ok_return_type_inference_without_cast() -> None:
    """Test that Ok can be returned as Result[T, differentE] without cast.

    This test will FAIL initially (red) with current implementation because
    Ok[int, ValueError] is not compatible with Result[int, str] due to
    invariance. After fixing variance, it should PASS (green).
    """

    def returns_string_error_result() -> Result[int, str]:
        # This should work without cast, but currently requires cast
        return Ok(42)  # Type error: Ok[int, ???] incompatible with Result[int, str]

    result = returns_string_error_result()
    assert result.unwrap() == 42


def test_err_return_type_inference_without_cast() -> None:
    """Test that Err can be returned as Result[differentT, E] without cast.

    This test will FAIL initially (red) with current implementation.
    After fixing variance, it should PASS (green).
    """

    def returns_int_value_result() -> Result[int, str]:
        # This should work without cast, but currently requires cast
        return Err("failure")  # Type error: Err[???, str] incompatible with Result[int, str]

    result = returns_int_value_result()
    assert result.unwrap_err() == "failure"


def test_map_err_return_type() -> None:
    """Test that map_err returns correctly typed Result.

    Verifies that Ok(...).map_err(...) returns Result[T, NewE] without cast.
    """
    ok_val: Result[int, ValueError] = Ok(10)
    # map_err should return Result[int, str], not require cast
    result: Result[int, str] = ok_val.map_err(lambda e: str(e))
    assert result.unwrap() == 10


def test_ok_covariant_subtyping_value() -> None:
    """Test that Ok[T, E] is covariant in T (subclass → superclass)."""

    class Animal:
        pass

    class Dog(Animal):
        pass

    def returns_animal_result() -> Result[Animal, str]:
        dog_result: Result[Dog, str] = Ok(Dog())
        return dog_result  # Should work without cast due to covariance

    result = returns_animal_result()
    assert result.is_ok()


def test_err_covariant_in_error_type() -> None:
    """Test that Err[T, E] is covariant in E (specific → general)."""

    def returns_exception_result() -> Result[int, Exception]:
        value_error_result: Err[int, ValueError] = Err(ValueError("oops"))
        return value_error_result  # Should work without cast due to covariance

    result = returns_exception_result()
    assert result.is_err()


def test_union_error_with_map_err() -> None:
    """Test union error type handling with map_err converter."""

    def get_value_error() -> Result[int, ValueError]:
        return Err(ValueError("bad"))

    def process() -> Result[int, ValueError | RuntimeError]:
        # Convert to union error type using map_err
        result = get_value_error()
        return result.map_err(lambda e: e)  # Type widens naturally

    result = process()
    assert result.is_err()


def test_optional_result_type() -> None:
    """Test Result[Optional[T], E] compatibility."""

    def returns_optional_result() -> Result[int | None, str]:
        return Ok(None)  # Should work with covariance

    result = returns_optional_result()
    assert result.unwrap() is None


def test_ok_none_result_type() -> None:
    """Test Ok with None value returns correct type."""
    result: Result[None, str] = Ok(None)
    assert result.unwrap() is None
    assert result.is_ok()


def test_result_subtyping_chain() -> None:
    """Test chaining operations with covariant types."""

    class Animal:
        name: str

        def __init__(self, name: str):
            self.name = name

    class Dog(Animal):
        pass

    def get_dog() -> Result[Dog, ValueError]:
        return Ok(Dog("Buddy"))

    def get_animal() -> Result[Animal, Exception]:
        dog_result = get_dog()
        return dog_result  # Type widens due to covariance

    result = get_animal()
    assert result.is_ok()
    assert result.unwrap().name == "Buddy"


def test_ok_type_value_in_nested_control_flow() -> None:
    """Test that Ok with type value works inside nested try/for blocks.

    This replicates a ty error where returning Ok(some_type) inside
    a try block within a for loop causes ty to infer Ok[None, Unknown]
    instead of the correct Result[type, TypeError].

    See: https://github.com/astral-sh/ty/issues/...
    """
    import importlib

    _cache: dict[str, type] = {}

    def resolve_type(type_name: str) -> Result[type, TypeError]:
        """Resolve a type name to a class from known modules."""
        if type_name in _cache:
            return Ok(_cache[type_name])

        modules = ["builtins", "collections"]
        for module_name in modules:
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, type_name):
                    component_type: type = getattr(module, type_name)
                    _cache[type_name] = component_type
                    return Ok(component_type)
            except ImportError:
                continue

        return Err(TypeError(f"Unknown type: {type_name}"))

    # Test resolving a builtin type
    result = resolve_type("str")
    assert result.is_ok()
    assert result.unwrap() is str

    # Test resolving from collections
    result2 = resolve_type("OrderedDict")
    assert result2.is_ok()

    # Test error case
    result3 = resolve_type("NonExistentType")
    assert result3.is_err()
    assert isinstance(result3.unwrap_err(), TypeError)
