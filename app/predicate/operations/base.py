from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any

T = TypeVar("T")

class Operation(ABC, Generic[T]):
    @abstractmethod
    def evaluate(self, value: T) -> bool:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass
