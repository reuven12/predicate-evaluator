import pytest
from types import SimpleNamespace
from predicate.feature_resolver import compile_feature


class Dummy:
    def __init__(self):
        self.a = SimpleNamespace(b=SimpleNamespace(c=123))
        self._private = 999
        self.d1 = 5
        self.x = SimpleNamespace(_bad=1)
        self.a1foo = 2


def test_resolve_valid_feature():
    obj = Dummy()
    assert compile_feature(obj, "a.b.c") == 123


def test_resolve_empty_string_returns_root():
    obj = Dummy()
    assert compile_feature(obj, "") == obj


def test_resolve_invalid_path_returns_none():
    obj = Dummy()
    assert compile_feature(obj, "non.existent.path") is None


def test_resolve_invalid_feature_format():
    obj = Dummy()

    # dot followed by underscore = invalid
    with pytest.raises(ValueError):
        compile_feature(obj, "x._bad")

    # dot followed by digit = invalid
    with pytest.raises(ValueError):
        compile_feature(obj, "a.1foo")
