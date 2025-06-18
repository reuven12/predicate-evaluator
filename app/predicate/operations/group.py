from typing import List, Any
import logging

from .base import Operation
from .operator_types import OperatorType

log = logging.getLogger(__name__)


class And(Operation[Any]):
    __slots__ = ("_operations",)
    operator_type = OperatorType.AND

    def __init__(self, operations: List[Operation[Any]]) -> None:
        self._operations = operations

    def evaluate(self, value: Any) -> bool:
        for op in self._operations:
            try:
                if not op.evaluate(value):
                    return False
            except Exception as e:
                log.warning(f"[And] inner op {op} raised: {e}")
                return False
        return True

    def to_dict(self) -> dict:
        return {
            "operator": self.operator_type.value,
            "operations": [op.to_dict() for op in self._operations],
        }


class Or(Operation[Any]):
    __slots__ = ("_operations",)
    operator_type = OperatorType.OR

    def __init__(self, operations: List[Operation[Any]]) -> None:
        self._operations = operations

    def evaluate(self, value: Any) -> bool:
        for op in self._operations:
            try:
                if op.evaluate(value):
                    return True
            except Exception as e:
                log.warning(f"[Or] inner op {op} raised: {e}")
                # treat exception as False, continue
        return False

    def to_dict(self) -> dict:
        return {
            "operator": self.operator_type.value,
            "operations": [op.to_dict() for op in self._operations],
        }
