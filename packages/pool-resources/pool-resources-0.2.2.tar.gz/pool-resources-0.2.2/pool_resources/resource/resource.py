from abc import ABC, abstractmethod
from typing import Union, TypeVar

T1 = TypeVar("T1")
T2 = TypeVar("T2")

class Resource(ABC):
    @abstractmethod
    def enable(self, item: Union[T1, T2]) -> Union[T1, T2]:
        """Enables the resource"""

    @abstractmethod
    def disable(self, item: Union[T1, T2]) -> Union[T1, T2]:
        """Disables the resource"""
