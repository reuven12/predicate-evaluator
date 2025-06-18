from typing import Any, Dict
from ..exceptions import InvalidOperatorError, PredicateError
from ..operations.operator_types import OperatorType
from ..operations.unary import IsNone, IsNotNone
from ..operations.binary import (
    EqTo, NotEqualTo, IsGreaterThan, IsLessThan
)
from ..operations.group import And, Or
from ..operations.base import Operation

# ---------------- factory map ----------------
_OPERATION_FACTORY: dict[OperatorType, callable] = {
    OperatorType.IS_NONE:      lambda d: IsNone(),
    OperatorType.IS_NOT_NONE:  lambda d: IsNotNone(),
    OperatorType.EQ_TO:        lambda d: EqTo(d["operand"]),
    OperatorType.NOT_EQ_TO:    lambda d: NotEqualTo(d["operand"]),
    OperatorType.GT:           lambda d: IsGreaterThan(d["operand"]),
    OperatorType.LT:           lambda d: IsLessThan(d["operand"]),
    OperatorType.AND:          lambda d: And([parse_operation(x) for x in d["operations"]]),
    OperatorType.OR:           lambda d: Or([parse_operation(x) for x in d["operations"]]),
}


def parse_operation(op_dict: Dict[str, Any]) -> Operation:
    """Convert an *operation* JSON dict into a concrete `Operation` object."""
    try:
        op_type = OperatorType(op_dict["operator"])
    except ValueError as exc:
        raise InvalidOperatorError(op_dict.get("operator")) from exc

    try:
        return _OPERATION_FACTORY[op_type](op_dict)
    except KeyError:                       # should never occur
        raise PredicateError(f"No factory for operator {op_type}")
