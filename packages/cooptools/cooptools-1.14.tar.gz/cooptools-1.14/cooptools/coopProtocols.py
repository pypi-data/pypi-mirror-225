from typing import Protocol, Dict

class Dict_able(Protocol):
    def to_dict(self) -> Dict:
        raise NotImplementedError()

class Json_able(Protocol):
    def to_json(self) -> str:
        raise NotImplementedError()

class Id_able(Protocol):
    id: str
