import pytest
from predicate.operations.unary import IsNone, IsNotNone


def test_is_none():
    op = IsNone()
    assert op.evaluate(None)
    assert not op.evaluate(0)
    assert not op.evaluate("text")


def test_is_not_none():
    op = IsNotNone()
    assert op.evaluate(123)
    assert not op.evaluate(None)


def test_to_dict_is_none():
    op = IsNone()
    assert op.to_dict() == {"operator": "isNone"}


def test_to_dict_is_not_none():
    op = IsNotNone()
    assert op.to_dict() == {"operator": "isNotNone"}
