from typing import Dict, List, Generic, TypeVar

T = TypeVar("T")

class Register(Generic[T]):
    def __init__(self, to_register: List[T] = None, ids: List[str] = None):
        self._registry: Dict[str, T] = {}

        if to_register is not None:
            self.register(to_register, ids)

    @property
    def Registry(self) -> Dict[str, T]:
        return self._registry

    def register(self, to_register: List[T], ids: List[str]):
        self._registry = {**self._registry, **{ids[ii]: x for ii, x in enumerate(to_register)}}

    def unregister(self, ids: List[str]):
        self._registry = {k: v for k, v in self._registry.items() if k not in ids}
