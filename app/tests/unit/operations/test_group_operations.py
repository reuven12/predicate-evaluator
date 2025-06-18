import pytest
from predicate.operations.group import And, Or
from predicate.operations.unary import IsNotNone
from predicate.operations.binary import EqTo, IsGreaterThan


def test_and_all_true():
    op = And([IsNotNone(), IsGreaterThan(5)])
    assert op.evaluate(10)


def test_and_one_false():
    op = And([IsNotNone(), IsGreaterThan(10)])
    assert not op.evaluate(5)


def test_or_one_true():
    op = Or([EqTo("a"), EqTo("b")])
    assert op.evaluate("b")


def test_or_all_false():
    op = Or([EqTo("a"), EqTo("b")])
    assert not op.evaluate("c")


def test_group_operations_with_exceptions():
    class ErrorOp:
        def evaluate(self, _): raise ValueError("fail")
        def to_dict(self): return {"operator": "error"}

    op_and = And([IsNotNone(), ErrorOp()])
    assert not op_and.evaluate("value")

    op_or = Or([ErrorOp(), EqTo("ok")])
    assert op_or.evaluate("ok")
