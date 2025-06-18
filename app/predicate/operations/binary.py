from operator import eq, ne, gt, lt
from typing import Callable, TypeVar, Any

from .base import Operation
from .operator_types import OperatorType

T = TypeVar("T")


class _SafeBinaryOperation(Operation[T]):
    __slots__ = ("_func", "_operand")

    def __init__(self, func: Callable[[T, T], bool], operand: T) -> None:
        self._func = func
        self._operand = operand

    # ------------------------------------------------------------------ #
    # main logic                                                         #
    # ------------------------------------------------------------------ #
    def evaluate(self, value: T) -> bool:
        try:
            return self._func(value, self._operand)
        except Exception:
            # Any comparison failure (TypeError, etc.) → treated as False
            return False

    # ------------------------------------------------------------------ #
    # serialisation helper                                               #
    # ------------------------------------------------------------------ #
    @property
    def operator_type(self) -> OperatorType:     # overridden downstream
        raise NotImplementedError

    def to_dict(self) -> dict:
        return {
            "operator": self.operator_type.value,
            "operand":  self._operand,
        }


class EqTo(_SafeBinaryOperation[T]):
    __slots__ = ()
    operator_type = OperatorType.EQ_TO          # for Enum serialisation

    def __init__(self, operand: T) -> None:
        super().__init__(eq, operand)


class NotEqualTo(_SafeBinaryOperation[T]):
    __slots__ = ()
    operator_type = OperatorType.NOT_EQ_TO

    def __init__(self, operand: T) -> None:
        super().__init__(ne, operand)


class IsGreaterThan(_SafeBinaryOperation[T]):
    __slots__ = ()
    operator_type = OperatorType.GT

    def __init__(self, operand: T) -> None:
        super().__init__(gt, operand)


class IsLessThan(_SafeBinaryOperation[T]):
    __slots__ = ()
    operator_type = OperatorType.LT

    def __init__(self, operand: T) -> None:
        super().__init__(lt, operand)
