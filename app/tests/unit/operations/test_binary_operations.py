import pytest
from predicate.operations.binary import EqTo, NotEqualTo, IsGreaterThan, IsLessThan


def test_eq_to():
    op = EqTo(10)
    assert op.evaluate(10)
    assert not op.evaluate(5)


def test_not_equal_to():
    op = NotEqualTo(10)
    assert op.evaluate(5)
    assert not op.evaluate(10)


def test_greater_than():
    op = IsGreaterThan(10)
    assert op.evaluate(15)
    assert not op.evaluate(5)


def test_less_than():
    op = IsLessThan(10)
    assert op.evaluate(5)
    assert not op.evaluate(15)
