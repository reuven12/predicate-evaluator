import logging
from typing import Any
from .base import Operation
from .operator_types import OperatorType

log = logging.getLogger(__name__)

class IsNone(Operation[Any]):
    __slots__ = ()
    operator_type = OperatorType.IS_NONE

    def evaluate(self, value: Any) -> bool:
        try:
            return value is None
        except Exception as e:
            log.warning(f"IsNone: Evaluation failed with error: {e}")
            return False

    def to_dict(self) -> dict:
        return {"operator": self.operator_type.value}

class IsNotNone(Operation[Any]):
    __slots__ = ()
    operator_type = OperatorType.IS_NOT_NONE

    def evaluate(self, value: Any) -> bool:
        try:
            return value is not None
        except Exception as e:
            log.warning(f"IsNotNone: Evaluation failed with error: {e}")
            return False
        
    def to_dict(self) -> dict:
        return {"operator": self.operator_type.value}
