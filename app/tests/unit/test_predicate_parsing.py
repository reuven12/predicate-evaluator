import pytest
from predicate.parser.operation_parser import parse_operation
from predicate.operations.operator_types import OperatorType
from predicate.operations.unary import IsNone, IsNotNone
from predicate.operations.binary import EqTo
from predicate.exceptions import InvalidOperatorError, PredicateError


def test_parse_simple_operator():
    op_dict = {"operator": OperatorType.IS_NONE.value}
    op = parse_operation(op_dict)
    assert isinstance(op, IsNone)

    op_dict = {"operator": OperatorType.IS_NOT_NONE.value}
    op = parse_operation(op_dict)
    assert isinstance(op, IsNotNone)


def test_parse_eq_to_operator():
    op_dict = {"operator": OperatorType.EQ_TO.value, "operand": 42}
    op = parse_operation(op_dict)
    assert isinstance(op, EqTo)
    assert op._operand == 42


def test_invalid_operator_raises():
    with pytest.raises(InvalidOperatorError):
        parse_operation({"operator": "non_existing"})


def test_missing_factory_raises():
    class FakeEnum:
        value = "invalid"

    with pytest.raises(PredicateError):
        parse_operation({"operator": FakeEnum.value})
