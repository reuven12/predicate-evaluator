import json
from typing import Any
from .feature_resolver import compile_feature
from .parser.operation_parser import parse_operation


class Predicate:
    def __init__(self, feature: str, operation: Any) -> None:
        self.feature = feature
        self.operation = operation

    @classmethod
    def from_json(cls, json_string: str) -> "Predicate":
        parsed = json.loads(json_string)
        feature = parsed.get("feature", "")
        operation_data = parsed["operation"]
        operation = parse_operation(operation_data)
        return cls(feature, operation)

    def evaluate(self, root: object) -> bool:
        value = compile_feature(root, self.feature)
        return self.operation.evaluate(value)

    def to_dict(self) -> dict:
        return {
            "feature": self.feature,
            "operation": self.operation.to_dict()
        }
