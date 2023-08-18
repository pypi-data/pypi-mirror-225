"""Dummy resource implementation"""
from typing import Union
from overrides import overrides

from .resource import Resource, T1, T2


class DummyResource(Resource):
    def __init__(self, index: int):
        self.index = index

    @overrides
    def enable(self, item: Union[T1, T2]) -> Union[T1, T2]:
        print(f"Enabling resource {self} to item {item}")
        return item

    @overrides
    def disable(self, item: Union[T1, T2]) -> Union[T1, T2]:
        print(f"Disabling resource {self} to item {item}")
        return item

    def __str__(self):
        return f"Dummy Resource (id: {self.index})"

    def __repr__(self):
        return str(self)
